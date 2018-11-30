from concurrent import futures
import time

import grpc
import etcd

import search_service_pb2
import search_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

#TODO refactor service implementation to separate class
def search_videos(video_id, user_id, rating):
    return

def get_query_suggestions(video_id):
    return #response body: video_id, ratings_count, ratings_total


class SearchServiceServicer(search_service_pb2_grpc.SearchServiceServicer):
    """Provides methods that implement functionality of the Search Service."""

    def __init__(self):
        print "SearchServiceServicer started"
        return

    def SearchVideos(self, request, context):
        """Searches for videos by a given query term
        """
        print ">>> SearchService:SearchVideos: "
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')
        # return search_videos(request.query, request.page_size, request.paging_state)

    def GetQuerySuggestions(self, request, context):
        """Gets the current rating stats for a video
        """
        print ">>> SearchService:GetQuerySuggestions: "
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')
        # return search_videos(request.query, request.page_size)

def init(server):
    search_service_pb2_grpc.add_SearchServiceServicer_to_server(
        SearchServiceServicer(), server)

# TODO: remove code for running this single service
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    init(server)
    server.add_insecure_port('[::]:8899')
    server.start()

    # TODO: Fix hardcoded values
    etcd_client = etcd.Client(host='10.0.75.1', port=2379)
    etcd_client.write('/killrvideo/services/SearchService/killrvideo-python', "10.0.75.1:8899")

    # only need this temporarily until such time as we're running multiple services?
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

