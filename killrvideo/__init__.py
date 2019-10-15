from concurrent import futures
import grpc
import time
import logging
import json
import os

from dse import ConsistencyLevel
from dse.auth import PlainTextAuthProvider
from dse.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT, EXEC_PROFILE_GRAPH_DEFAULT, NoHostAvailable
from dse_graph import DseGraph
from dse.policies import TokenAwarePolicy, DCAwareRoundRobinPolicy
import dse.cqlengine.connection

from comments.comments_service_grpc import CommentsServiceServicer
from ratings.ratings_service_grpc import RatingsServiceServicer
from search.search_service_grpc import SearchServiceServicer
from statistics.statistics_service_grpc import StatisticsServiceServicer
from suggested_videos.suggested_videos_service_grpc import SuggestedVideosServiceServicer
#from uploads.uploads_service_grpc import UploadsServiceServicer
from user_management.user_management_service_grpc import UserManagementServiceServicer
from video_catalog.video_catalog_service_grpc import VideoCatalogServiceServicer

from comments.comments_service import CommentsService
from ratings.ratings_service import RatingsService
from search.search_service import SearchService
from statistics.statistics_service import StatisticsService
from suggested_videos.suggested_videos_service import SuggestedVideosService
#from uploads.uploads_service import UploadsService
from user_management.user_management_service import UserManagementService
from video_catalog.video_catalog_service import VideoCatalogService

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def serve():

    dse_username = os.getenv('KILLRVIDEO_DSE_USERNAME')
    dse_password = os.getenv('KILLRVIDEO_DSE_PASSWORD')
    dse_contact_points = os.getenv('KILLRVIDEO_DSE_CONTACT_POINTS', 'dse').split(',')
    service_port = os.getenv('KILLRVIDEO_SERVICE_PORT', '50101')

    file = open('config.json', 'r')
    config = json.load(file)

    default_consistency_level = config['DEFAULT_CONSISTENCY_LEVEL']

    # Initialize Cassandra Driver and Mapper
    load_balancing_policy = TokenAwarePolicy(DCAwareRoundRobinPolicy())
    profile = ExecutionProfile(consistency_level=ConsistencyLevel.name_to_value[default_consistency_level],
                               load_balancing_policy=load_balancing_policy)
    graph_profile = DseGraph.create_execution_profile('killrvideo_video_recommendations')

    auth_provider = None
    if dse_username:
        auth_provider = PlainTextAuthProvider(username=dse_username, password=dse_password)

    # Wait for Cassandra (DSE) to be up
    session = None
    while not session:
        try:
            session = Cluster(contact_points=dse_contact_points,
                              execution_profiles={EXEC_PROFILE_DEFAULT: profile, EXEC_PROFILE_GRAPH_DEFAULT: graph_profile},
                              auth_provider = auth_provider).connect("killrvideo")
        except (NoHostAvailable):
            logging.info('Waiting for Cassandra (DSE) to be available')
            time.sleep(10)

    # Additional retry loop to check if dummy keyspace exists
    while True:
        logging.info('Checking for schema to be created...')
        result = session.execute('select * from killrvideo.kv_init_done')
        if result.one(): # any result indicates keyspace has been created
            break
        time.sleep(10)

    dse.cqlengine.connection.set_session(session)

    # Initialize GRPC Server
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Initialize Services (GRPC servicers with reference to GRPC Server and appropriate service reference
    CommentsServiceServicer(grpc_server, CommentsService(session=session))
    RatingsServiceServicer(grpc_server, RatingsService())
    SearchServiceServicer(grpc_server, SearchService(session=session))
    StatisticsServiceServicer(grpc_server, StatisticsService())
    SuggestedVideosServiceServicer(grpc_server, SuggestedVideosService(session=session))
    #UploadsServiceServicer(grpc_server, UploadsService())
    UserManagementServiceServicer(grpc_server, UserManagementService(session=session))
    VideoCatalogServiceServicer(grpc_server, VideoCatalogService(session=session))

    # Start GRPC Server
    grpc_server.add_insecure_port('[::]:' + service_port)
    grpc_server.start()

    # Keep application alive
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpc_server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('kafka').setLevel(logging.ERROR)
    serve()
