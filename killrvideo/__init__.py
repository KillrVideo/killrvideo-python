from concurrent import futures
import grpc
import etcd
import time
import logging

from dse.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from dse import ConsistencyLevel
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

# TODO: replace hardcoded values with properties
_SERVICE_PORT = "8899"
_SERVICE_HOST = "10.0.75.1"
_ETCD_PORT = 2379

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def serve():

    service_address = _SERVICE_HOST + ":" + _SERVICE_PORT
    etcd_client = etcd.Client(host=_SERVICE_HOST, port=_ETCD_PORT)

    # Wait for Cassandra (DSE) to be up, aka registered in etcd
    while True:
        try:
            etcd_client.read('/killrvideo/services/cassandra')
            break # if we get here, Cassandra is registered and should be available
        except etcd.EtcdKeyNotFound:
            logging.info('Waiting for Cassandra to be registered in etcd, sleeping 10s')
            time.sleep(10)

    # Initialize Cassandra Driver and Mapper
    profile = ExecutionProfile(consistency_level = ConsistencyLevel.LOCAL_QUORUM)
    cluster = Cluster(contact_points=['10.0.75.1'], execution_profiles={EXEC_PROFILE_DEFAULT: profile})
    session = cluster.connect("killrvideo")
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
    UserManagementServiceServicer(grpc_server, UserManagementService())
    VideoCatalogServiceServicer(grpc_server, VideoCatalogService(session=session))

    # Start GRPC Server
    grpc_server.add_insecure_port('[::]:' + _SERVICE_PORT)
    grpc_server.start()

    # Register Services with etcd
    etcd_client.write('/killrvideo/services/CommentsService/killrvideo-python', service_address)
    etcd_client.write('/killrvideo/services/RatingsService/killrvideo-python', service_address)
    etcd_client.write('/killrvideo/services/SearchService/killrvideo-python', service_address)
    etcd_client.write('/killrvideo/services/StatisticsService/killrvideo-python', service_address)
    etcd_client.write('/killrvideo/services/SuggestedVideoService/killrvideo-python', service_address)
    #etcd_client.write('/killrvideo/services/UploadsService/killrvideo-python', service_address)
    etcd_client.write('/killrvideo/services/UserManagementService/killrvideo-python', service_address)
    etcd_client.write('/killrvideo/services/VideoCatalogService/killrvideo-python', service_address)

    # Keep application alive
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        grpc_server.stop(0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    serve()
