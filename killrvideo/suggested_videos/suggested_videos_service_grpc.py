from concurrent import futures
import time

import grpc
import etcd

import suggested_videos_service_pb2
import suggested_videos_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class SuggestedVideosServiceServicer(suggested_videos_service_pb2_grpc.SuggestedVideoServiceServicer):
    """Provides methods that implement functionality of the SuggestedVideos Service."""

    def __init__(self):
        print "SuggestedVideosServiceServicer started"
        return

    def GetRelatedVideos(self, request, context):
        """Gets videos related to another video
        """
        print ">>> SuggestedVideosService:GetRelatedVideos: "
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSuggestedForUser(self, request, context):
        """Gets personalized video suggestions for a user
        """
        print ">>> SuggestedVideosService:GetSuggestedForUser: "
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def init(server):
    suggested_videos_service_pb2_grpc.add_SuggestedVideoServiceServicer_to_server(
        SuggestedVideosServiceServicer(), server)

# TODO: remove code for running this single service
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    init(server)
    server.add_insecure_port('[::]:8899')
    server.start()

    # TODO: Fix hardcoded values
    etcd_client = etcd.Client(host='10.0.75.1', port=2379)
    etcd_client.write('/killrvideo/services/SuggestedVideosService/killrvideo-python', "10.0.75.1:8899")

    # only need this temporarily until such time as we're running multiple services?
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

