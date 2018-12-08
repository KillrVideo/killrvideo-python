import grpc

import statistics_service_pb2
import statistics_service_pb2_grpc

class StatisticsServiceServicer(statistics_service_pb2_grpc.StatisticsServiceServicer):
    """Provides methods that implement functionality of the Statistics Service."""

    def __init__(self, grpc_server, statistics_service):
        print "StatisticsServiceServicer started"
        self.statistics_service = statistics_service
        statistics_service_pb2_grpc.add_StatisticsServiceServicer_to_server(self, grpc_server)

    def RecordPlaybackStarted(self, request, context):
        """Record that playback started for a given video
        """
        print ">>> StatisticsService:RecordPlaybackStarted: "
        print request
        # TODO: implement service call
        #statistics_service.record_playback_started(UUID(request.video_id))
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetNumberOfPlays(self, request, context):
        """Get the number of plays for a given video or set of videos
        """
        print ">>> StatisticsService:GetNumberOfPlays: "
        print request
        # TODO: implement service call
        #result = statistics_service.get_number_of_plays(UUID(request.video_id))
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

