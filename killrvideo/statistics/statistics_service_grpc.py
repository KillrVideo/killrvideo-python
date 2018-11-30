from concurrent import futures
import time

import grpc

import statistics_service_pb2
import statistics_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class StatisticsServiceServicer(statistics_service_pb2_grpc.StatisticsServiceServicer):
    """Provides methods that implement functionality of the Statistics Service."""

    def __init__(self):
        print "started"
        return

    def RecordPlaybackStarted(self, request, context):
        """Record that playback started for a given video
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetNumberOfPlays(self, request, context):
        """Get the number of plays for a given video or set of videos
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

# TODO: remove code for running this single service
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    statistics_service_pb2_grpc.add_StatisticsServiceServicer_to_server(
        StatisticsServiceServicer(), server)
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

