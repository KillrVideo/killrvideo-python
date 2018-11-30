from concurrent import futures
import time

import grpc

import search_service_pb2
import search_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

#TODO refactor service implementation to separate class
def search_videos(video_id, user_id, rating):
    return

def get_rating(video_id):
    return #response body: video_id, ratings_count, ratings_total

def get_user_rating(video_id, user_id):
    return #response body: video_id, user_id, rating


class SearchServiceServicer(search_service_pb2_grpc.SearchServiceServicer):
    """Provides methods that implement functionality of the Search Service."""

    def __init__(self):
        print "started"
        return

    def SearchVideos(self, request, context):
        """Searches for videos by a given query term
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')
        # return search_videos(request.query, request.page_size, request.paging_state)

    def GetQuerySuggestions(self, request, context):
        """Gets the current rating stats for a video
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')
        # return search_videos(request.query, request.page_size)

    def GetUserRating(self, request, context):
        """Gets a user's rating of a specific video and returns 0 if the user hasn't rated the video
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

# TODO: remove code for running this single service
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    search_service_pb2_grpc.add_SearchServiceServicer_to_server(
        SearchServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    # only need this temporarily until such time as we're running multiple services?
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

