import grpc
from uuid import UUID

from video_catalog_service_pb2 import SubmitUploadedVideoResponse, SubmitYouTubeVideoResponse
import video_catalog_service_pb2_grpc
from common.common_types_conversions import uuid_to_grpc,grpc_to_uuid


class VideoCatalogServiceServicer(video_catalog_service_pb2_grpc.VideoCatalogServiceServicer):
    """Provides methods that implement functionality of the VideoCatalog Service."""

    def __init__(self, grpc_server, video_catalog_service):
        print "VideoCatalogServiceServicer started"
        self.video_catalog_service = video_catalog_service
        video_catalog_service_pb2_grpc.add_VideoCatalogServiceServicer_to_server(self, grpc_server)

    def SubmitUploadedVideo(self, request, context):
        """Submit an uploaded video to the catalog
        """
        print ">>> VideoCatalogService:SubmitUploadedVideo: "
        print request
        self.video_catalog_service.submit_uploaded_video(grpc_to_uuid(request.video_id), grpc_to_uuid(request.user_id),
                                                         request.name, request.description, request.tags,
                                                         request.upload_url)
        return SubmitUploadedVideoResponse()

    def SubmitYouTubeVideo(self, request, context):
        """Submit a YouTube video to the catalog
        """
        print ">>> VideoCatalogService:SubmitYouTubeVideo: "
        print request
        self.video_catalog_service.submit_youtube_video(grpc_to_uuid(request.video_id), grpc_to_uuid(request.user_id),
                                                        request.name, request.description, request.tags,
                                                        request.you_tube_video_id)
        return SubmitYouTubeVideoResponse()

    def GetVideo(self, request, context):
        """Gets a video from the catalog
        """
        print ">>> VideoCatalogService:GetVideo: "
        print request
        # TODO: implement service call
        #video_catalog_service.get_video(UUID(request.video_id))
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetVideoPreviews(self, request, context):
        """Gets video previews for a limited number of videos from the catalog
        """
        print ">>> VideoCatalogService:GetVideoPreviews: "
        print request
        # TODO: implement service call
        #video_catalog_service.get_video_previews(video_ids) #map to UUID
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLatestVideoPreviews(self, request, context):
        """Gets video previews for the latest (i.e. newest) videos from the catalog
        """
        print ">>> VideoCatalogService:GetLatestVideoPreviews: "
        print request
        # TODO: implement service call
        #video_catalog_service.get_latest_video_previews(page_size, starting_added_date,
        # UUID(starting_video_id), paging_state)
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserVideoPreviews(self, request, context):
        """Gets video previews for videos added to the site by a particular user
        """
        print ">>> VideoCatalogService:GetUserVideoPreviews: "
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

