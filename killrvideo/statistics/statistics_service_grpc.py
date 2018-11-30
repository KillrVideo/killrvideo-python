from concurrent import futures
import time

import grpc
import etcd

import statistics_service_pb2
import statistics_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class StatisticsServiceServicer(statistics_service_pb2_grpc.StatisticsServiceServicer):
    """Provides methods that implement functionality of the Statistics Service."""

    def __init__(self):
        print "StatisticsServiceServicer started"
        return

    def RecordPlaybackStarted(self, request, context):
        """Record that playback started for a given video
        """
        print ">>> StatisticsService:RecordPlaybackStarted: "
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetNumberOfPlays(self, request, context):
        """Get the number of plays for a given video or set of videos
        """
        print ">>> StatisticsService:GetNumberOfPlays: "
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def init(server):
    statistics_service_pb2_grpc.add_StatisticsServiceServicer_to_server(
        StatisticsServiceServicer(), server)

# TODO: remove code for running this single service
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    init(server)
    server.add_insecure_port('[::]:8899')
    server.start()

    # TODO: Fix hardcoded values
    etcd_client = etcd.Client(host='10.0.75.1', port=2379)
    etcd_client.write('/killrvideo/services/StatisticsService/killrvideo-python', "10.0.75.1:8899")

    # only need this temporarily until such time as we're running multiple services?
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

