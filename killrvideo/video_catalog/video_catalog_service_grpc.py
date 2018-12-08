import grpc

import video_catalog_service_pb2
import video_catalog_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


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
        # TODO: implement service call
        #video_catalog_service.submit_uploaded_video(UUID(request.video_id), UUID(request.user_id), request.name,
        # request.description, request.tags, request.upload_url)
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubmitYouTubeVideo(self, request, context):
        """Submit a YouTube video to the catalog
        """
        print ">>> VideoCatalogService:SubmitYouTubeVideo: "
        print request
        # TODO: implement service call
        #video_catalog_service.submit_youtube_video(request.video_id, request.user_id, request.name,
        # request.description, request.tags, request.you_tube_video_id)
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

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

