import logging
from .suggested_videos_service_pb2 import GetRelatedVideosResponse, GetSuggestedForUserResponse, SuggestedVideoPreview
from . import suggested_videos_service_pb2_grpc
from common.common_types_conversions import UUID_to_grpc, grpc_to_UUID, datetime_to_Timestamp

def VideoPreview_to_SuggestedVideoPreview(video):
    return SuggestedVideoPreview(video_id=UUID_to_grpc(video.video_id),
                                 added_date=datetime_to_Timestamp(video.added_date),
                                 name=video.name, preview_image_location=video.preview_image_location,
                                 user_id=UUID_to_grpc(video.user_id))


def RelatedVideos_to_GetRelatedVideosResponse(related_videos):
    response = GetRelatedVideosResponse(video_id=UUID_to_grpc(related_videos.video_id),
                                        paging_state=related_videos.paging_state)
    if isinstance(related_videos.videos, (list,)):    # most preferred way to check if it's list
        response.videos.extend(map(VideoPreview_to_SuggestedVideoPreview,related_videos.videos))
    elif related_videos.videos is not None: # single result
        response.videos.extend([VideoPreview_to_SuggestedVideoPreview(related_videos.videos)])
    return response


def SuggestedVideos_to_GetSuggestedForUserResponse(suggested_videos):
    response = GetSuggestedForUserResponse(user_id=UUID_to_grpc(suggested_videos.user_id),
                                           paging_state=suggested_videos.paging_state)
    if isinstance(suggested_videos.videos, (list,)):    # most preferred way to check if it's list
        response.videos.extend(map(VideoPreview_to_SuggestedVideoPreview,suggested_videos.videos))
    elif suggested_videos.videos is not None: # single result
        response.videos.extend([VideoPreview_to_SuggestedVideoPreview(suggested_videos.videos)])
    return response


class SuggestedVideosServiceServicer(suggested_videos_service_pb2_grpc.SuggestedVideoServiceServicer):
    """Provides methods that implement functionality of the SuggestedVideos Service."""

    def __init__(self, grpc_server, suggested_videos_service):
        logging.debug("SuggestedVideosServiceServicer started")
        self.suggested_videos_service = suggested_videos_service
        suggested_videos_service_pb2_grpc.add_SuggestedVideoServiceServicer_to_server(self, grpc_server)


    def GetRelatedVideos(self, request, context):
        """Gets videos related to another video
        """
        logging.debug(">>> SuggestedVideosService:GetRelatedVideos: ")
        logging.debug(request)
        result = self.suggested_videos_service.get_related_videos(grpc_to_UUID(request.video_id), request.page_size,
                                                                  request.paging_state)
        return RelatedVideos_to_GetRelatedVideosResponse(result)


    def GetSuggestedForUser(self, request, context):
        """Gets personalized video suggestions for a user
        """
        logging.debug(">>> SuggestedVideosService:GetSuggestedForUser: ")
        logging.debug(request)
        result = self.suggested_videos_service.get_suggested_for_user(grpc_to_UUID(request.user_id), request.page_size,
                                                                      request.paging_state)
        return SuggestedVideos_to_GetSuggestedForUserResponse(result)

