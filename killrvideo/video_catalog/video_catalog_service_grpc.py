import grpc
import logging
from common.common_types_conversions import UUID_to_grpc, grpc_to_UUID, datetime_to_Timestamp, Timestamp_to_datetime
from video_catalog_service_pb2 import SubmitYouTubeVideoResponse, GetVideoResponse, \
    VideoPreview, GetVideoPreviewsResponse, GetLatestVideoPreviewsResponse, GetUserVideoPreviewsResponse
import video_catalog_service_pb2_grpc

def VideoModel_to_GetVideoResponse(video):
    response = GetVideoResponse(video_id=UUID_to_grpc(video.video_id), user_id=UUID_to_grpc(video.user_id),
                                name=video.name, description=video.description, location=video.location,
                                location_type=video.location_type, added_date=datetime_to_Timestamp(video.added_date))
    if isinstance(video.tags, (set,)):    # most preferred way to check if it's a set
        response.tags.extend(video.tags)
    elif video.tags is not None:  # single result
        response.tags.extend([video.tags])
    return response


def VideoModel_to_VideoPreview(video):
    return VideoPreview(video_id=UUID_to_grpc(video.video_id), user_id=UUID_to_grpc(video.user_id),
                        name=video.name, preview_image_location=video.preview_image_location,
                        added_date=datetime_to_Timestamp(video.added_date))


def VideoModels_to_GetVideoPreviewsResponse(videos):
    response = GetVideoPreviewsResponse()
    if isinstance(videos, (list,)):    # most preferred way to check if it's list
        response.video_previews.extend(map(VideoModel_to_VideoPreview, videos))
    elif videos is not None:  # single result
        response.video_previews.extend([VideoModel_to_VideoPreview(videos)])
    return response


def LatestVideosModel_to_VideoPreview(video):
    return VideoPreview(video_id=UUID_to_grpc(video.video_id), user_id=UUID_to_grpc(video.user_id),
                        name=video.name, preview_image_location=video.preview_image_location,
                        added_date=datetime_to_Timestamp(video.added_date))


def LatestVideoPreviews_to_GetLatestVideoPreviewsResponse(previews):
    response = GetLatestVideoPreviewsResponse(paging_state=previews.paging_state)
    if isinstance(previews.videos, (list,)):    # most preferred way to check if it's list
        response.video_previews.extend(map(LatestVideosModel_to_VideoPreview, previews.videos))
    elif previews.videos is not None:  # single result
        response.video_previews.extend([LatestVideosModel_to_VideoPreview(previews.videos)])
    return response


def UserVideosModel_to_VideoPreview(video):
    return VideoPreview(video_id=UUID_to_grpc(video.video_id), user_id=UUID_to_grpc(video.user_id),
                        name=video.name, preview_image_location=video.preview_image_location,
                        added_date=datetime_to_Timestamp(video.added_date))


def UserVideoPreviews_to_GetUserVideoPreviewsResponse(previews):
    response = GetUserVideoPreviewsResponse(paging_state=previews.paging_state)
    if isinstance(previews.videos, (list,)):    # most preferred way to check if it's list
        response.video_previews.extend(map(UserVideosModel_to_VideoPreview, previews.videos))
    elif previews.videos is not None:  # single result
        response.video_previews.extend([LatestVideosModel_to_VideoPreview(previews.videos)])
    return response


class VideoCatalogServiceServicer(video_catalog_service_pb2_grpc.VideoCatalogServiceServicer):
    """Provides methods that implement functionality of the VideoCatalog Service."""

    def __init__(self, grpc_server, video_catalog_service):
        logging.debug("VideoCatalogServiceServicer started")
        self.video_catalog_service = video_catalog_service
        video_catalog_service_pb2_grpc.add_VideoCatalogServiceServicer_to_server(self, grpc_server)

    def SubmitUploadedVideo(self, request, context):
        """Submit an uploaded video to the catalog
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubmitYouTubeVideo(self, request, context):
        """Submit a YouTube video to the catalog
        """
        logging.debug(">>> VideoCatalogService:SubmitYouTubeVideo: ")
        logging.debug(request)
        video_id = grpc_to_UUID(request.video_id)
        user_id = grpc_to_UUID(request.user_id)
        self.video_catalog_service.submit_youtube_video(video_id=video_id,
                                                        user_id=user_id,
                                                        name=request.name,
                                                        description=request.description,
                                                        tags=request.tags,
                                                        you_tube_video_id=request.you_tube_video_id)

        return SubmitYouTubeVideoResponse()

    def GetVideo(self, request, context):
        """Gets a video from the catalog
        """
        logging.debug(">>> VideoCatalogService:GetVideo: ")
        logging.debug(request)
        result = self.video_catalog_service.get_video(video_id=grpc_to_UUID(request.video_id))
        logging.debug(result)
        return VideoModel_to_GetVideoResponse(result)

    def GetVideoPreviews(self, request, context):
        """Gets video previews for a limited number of videos from the catalog
        """
        logging.debug(">>> VideoCatalogService:GetVideoPreviews: ")
        logging.debug(request)
        result = self.video_catalog_service.get_video_previews(video_ids=map(grpc_to_UUID, request.video_ids))
        logging.debug(result)
        return VideoModels_to_GetVideoPreviewsResponse(result)

    def GetLatestVideoPreviews(self, request, context):
        """Gets video previews for the latest (i.e. newest) videos from the catalog
        """
        logging.debug(">>> VideoCatalogService:GetLatestVideoPreviews: ")
        logging.debug(request)
        starting_video_id = None
        starting_added_date = None
        if request.starting_video_id.value:
            starting_video_id = grpc_to_UUID(request.starting_video_id)
        if long(request.starting_added_date.seconds) != 0:
            starting_added_date = Timestamp_to_datetime(request.starting_added_date)
        result = self.video_catalog_service.get_latest_video_previews(page_size=request.page_size,
                                                                      starting_added_date=starting_added_date,
                                                                      starting_video_id=starting_video_id,
                                                                      paging_state=request.paging_state)
        logging.debug(result)
        return LatestVideoPreviews_to_GetLatestVideoPreviewsResponse(result)

    def GetUserVideoPreviews(self, request, context):
        """Gets video previews for videos added to the site by a particular user
        """
        logging.debug(">>> VideoCatalogService:GetUserVideoPreviews: ")
        logging.debug(request)
        starting_video_id = None
        if request.starting_video_id.value:
            starting_video_id = grpc_to_UUID(request.starting_video_id)
        starting_added_date = None
        if long(request.starting_added_date.seconds) != 0:
            starting_added_date = Timestamp_to_datetime(request.starting_added_date)
        result = self.video_catalog_service.get_user_video_previews(user_id=grpc_to_UUID(request.user_id),
                                                                    page_size=request.page_size,
                                                                    starting_added_date=starting_added_date,
                                                                    starting_video_id=starting_video_id,
                                                                    paging_state=request.paging_state)
        logging.debug(result)
        return UserVideoPreviews_to_GetUserVideoPreviewsResponse(result)
