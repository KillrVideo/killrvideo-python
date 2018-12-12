import grpc
from uuid import UUID
from common.common_types_conversions import UUID_to_grpc, grpc_to_UUID
from video_catalog_service_pb2 import SubmitYouTubeVideoResponse, GetVideoResponse, VideoLocationType, \
    VideoPreview, GetVideoPreviewsResponse, GetLatestVideoPreviewsResponse, GetUserVideoPreviewsResponse
import video_catalog_service_pb2_grpc


def VideoModel_to_GetVideoResponse(video):
    response = GetVideoResponse(video_id=UUID_to_grpc(video.video_id), user_id=UUID_to_grpc(video.user_id),
                                name=video.name, description=video.description, location=video.location,
                                location_type=VideoLocationType.YOUTUBE, added_date=video.added_date)
    for tag in video.tags:
        response.tags.extend([tag])
    return response


def VideoModel_to_VideoPreview(video):
    return VideoPreview(video_id=UUID_to_grpc(video.video_id), user_id=UUID_to_grpc(video.user_id),
                        name=video.name, preview_image_location=video.preview_image_location,
                        added_date=video.added_date)


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
                        added_date=video.added_date)


def LatestVideoPreviews_to_GetLatestVideoPreviewsResponse(previews):
    response = GetLatestVideoPreviewsResponse(previews.paging_state)
    if isinstance(previews.videos, (list,)):    # most preferred way to check if it's list
        response.video_previews.extend(map(LatestVideosModel_to_VideoPreview, previews.videos))
    elif previews.previews is not None:  # single result
        response.video_previews.extend([LatestVideosModel_to_VideoPreview(previews.videos)])
    return response


def UserVideosModel_to_VideoPreview(video):
    return VideoPreview(video_id=UUID_to_grpc(video.video_id), user_id=UUID_to_grpc(video.user_id),
                        name=video.name, preview_image_location=video.preview_image_location,
                        added_date=video.added_date)


def UserVideoPreviews_to_GetUserVideoPreviewsResponse(previews):
    response = GetUserVideoPreviewsResponse()
    if isinstance(previews.videos, (list,)):    # most preferred way to check if it's list
        response.video_previews.extend(map(UserVideosModel_to_VideoPreview, previews.videos))
    elif previews.previews is not None:  # single result
        response.video_previews.extend([LatestVideosModel_to_VideoPreview(previews.videos)])
    return response


class VideoCatalogServiceServicer(video_catalog_service_pb2_grpc.VideoCatalogServiceServicer):
    """Provides methods that implement functionality of the VideoCatalog Service."""

    def __init__(self, grpc_server, video_catalog_service):
        print "VideoCatalogServiceServicer started"
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
        print ">>> VideoCatalogService:SubmitYouTubeVideo: "
        print request
        self.video_catalog_service.submit_youtube_video(video_id=grpc_to_UUID(request.video_id),
                                                        user_id=grpc_to_UUID(request.user_id),
                                                        name=request.name,
                                                        description=request.description,
                                                        tags=request.tags,
                                                        you_tube_video_id=request.you_tube_video_id)
        return SubmitYouTubeVideoResponse()

    def GetVideo(self, request, context):
        """Gets a video from the catalog
        """
        print ">>> VideoCatalogService:GetVideo: "
        print request
        result = self.video_catalog_service.get_video(video_id=UUID(request.video_id))
        print result
        return VideoModel_to_GetVideoResponse(result)

    def GetVideoPreviews(self, request, context):
        """Gets video previews for a limited number of videos from the catalog
        """
        print ">>> VideoCatalogService:GetVideoPreviews: "
        print request
        result = self.video_catalog_service.get_video_previews(video_ids=map(grpc_to_UUID, request.video_ids))
        print result
        return VideoModels_to_GetVideoPreviewsResponse(result)

    def GetLatestVideoPreviews(self, request, context):
        """Gets video previews for the latest (i.e. newest) videos from the catalog
        """
        print ">>> VideoCatalogService:GetLatestVideoPreviews: "
        print request
        result = self.video_catalog_service.get_latest_video_previews(page_size=request.page_size,
                                                                      starting_added_date=request.starting_added_date,
                                                                      starting_video_id=grpc_to_UUID(request.starting_video_id),
                                                                      paging_state=request.paging_state)
        print result
        return LatestVideoPreviews_to_GetLatestVideoPreviewsResponse(result)

    def GetUserVideoPreviews(self, request, context):
        """Gets video previews for videos added to the site by a particular user
        """
        print ">>> VideoCatalogService:GetUserVideoPreviews: "
        print request
        result = self.video_catalog_service.get_user_video_previews(user_id=grpc_to_UUID(request.user_id),
                                                                    page_size=request.page_size,
                                                                    starting_added_date=request.starting_added_date,
                                                                    starting_video_id=grpc_to_UUID(request.starting_video_id),
                                                                    paging_state=request.paging_state)
        print result
        return UserVideoPreviews_to_GetUserVideoPreviewsResponse(result)
