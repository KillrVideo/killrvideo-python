from concurrent import futures
import time

import grpc

import suggested_videos_service_pb2
import suggested_videos_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class SuggestedVideosServiceServicer(suggested_videos_service_pb2_grpc.SuggestedVideosServiceServicer):
    """Provides methods that implement functionality of the SuggestedVideos Service."""

    def __init__(self):
        print "started"
        return

    def GetRelatedVideos(self, request, context):
        """Gets videos related to another video
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSuggestedForUser(self, request, context):
        """Gets personalized video suggestions for a user
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

# TODO: remove code for running this single service
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    suggested_videos_service_pb2_grpc.add_SuggestedVideosServiceServicer_to_server(
        SuggestedVideosServiceServicer(), server)
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

