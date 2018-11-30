from concurrent import futures
import grpc
import etcd
import time

from comments import comments_service_grpc
from ratings import ratings_service_grpc
from search import search_service_grpc
from statistics import statistics_service_grpc
from suggested_videos import suggested_videos_service_grpc
from uploads import uploads_service_grpc
from user_management import user_management_service_grpc
from video_catalog import video_catalog_service_grpc

# TODO: replace hardcoded values with properties
_SERVICE_PORT = "8899"
_SERVICE_HOST = "10.0.75.1"
_ETCD_PORT = 2379

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    comments_service_grpc.init(server)
    ratings_service_grpc.init(server)
    search_service_grpc.init(server)
    statistics_service_grpc.init(server)
    suggested_videos_service_grpc.init(server)
    uploads_service_grpc.init(server)
    user_management_service_grpc.init(server)
    video_catalog_service_grpc.init(server)

    server.add_insecure_port('[::]:' + _SERVICE_PORT)
    server.start()

    service_address = _SERVICE_HOST + ":" + _SERVICE_PORT
    etcd_client = etcd.Client(host=_SERVICE_HOST, port=_ETCD_PORT)
    etcd_client.write('/killrvideo/services/CommentService/killrvideo-python', service_address)
    etcd_client.write('/killrvideo/services/RatingsService/killrvideo-python', service_address)
    etcd_client.write('/killrvideo/services/SearchService/killrvideo-python', service_address)
    etcd_client.write('/killrvideo/services/StatisticsService/killrvideo-python', service_address)
    etcd_client.write('/killrvideo/services/SuggestedVideosService/killrvideo-python', service_address)
    etcd_client.write('/killrvideo/services/UploadsService/killrvideo-python', service_address)
    etcd_client.write('/killrvideo/services/UserManagementService/killrvideo-python', service_address)
    etcd_client.write('/killrvideo/services/VideoCatalogService/killrvideo-python', service_address)

    # keep application alive
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()