import logging
from .statistics_service_pb2 import RecordPlaybackStartedResponse, GetNumberOfPlaysResponse, PlayStats
from . import statistics_service_pb2_grpc
from common.common_types_conversions import UUID_to_grpc, grpc_to_UUID


def VideoPlaybackStatsModel_to_PlayStats(stats):
    return PlayStats(video_id=UUID_to_grpc(stats.video_id), views=stats.views)

def VideoPlaybackStatsModelList_to_GetNumberOfPlaysResponse(stats):
    response = GetNumberOfPlaysResponse()
    if isinstance(stats, (list,)):    # most preferred way to check if it's list
        response.stats.extend(map(VideoPlaybackStatsModel_to_PlayStats, stats))
    elif stats is not None: # single result
        response.stats.extend([VideoPlaybackStatsModel_to_PlayStats(stats)])
    return response

class StatisticsServiceServicer(statistics_service_pb2_grpc.StatisticsServiceServicer):
    """Provides methods that implement functionality of the Statistics Service."""

    def __init__(self, grpc_server, statistics_service):
        logging.debug("StatisticsServiceServicer started")
        self.statistics_service = statistics_service
        statistics_service_pb2_grpc.add_StatisticsServiceServicer_to_server(self, grpc_server)

    def RecordPlaybackStarted(self, request, context):
        """Record that playback started for a given video
        """
        logging.debug(">>> StatisticsService:RecordPlaybackStarted: ")
        logging.debug(request)
        self.statistics_service.record_playback_started(grpc_to_UUID(request.video_id))
        return RecordPlaybackStartedResponse()


    def GetNumberOfPlays(self, request, context):
        """Get the number of plays for a given video or set of videos
        """
        logging.debug(">>> StatisticsService:GetNumberOfPlays: ")
        logging.debug(request)
        result = self.statistics_service.get_number_of_plays(list(map(grpc_to_UUID, request.video_ids)))
        return VideoPlaybackStatsModelList_to_GetNumberOfPlaysResponse(result)



