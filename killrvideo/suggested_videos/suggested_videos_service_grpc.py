import grpc

import suggested_videos_service_pb2
import suggested_videos_service_pb2_grpc

class SuggestedVideosServiceServicer(suggested_videos_service_pb2_grpc.SuggestedVideoServiceServicer):
    """Provides methods that implement functionality of the SuggestedVideos Service."""

    def __init__(self, grpc_server, suggested_videos_service):
        print "SuggestedVideosServiceServicer started"
        self.suggested_videos_service = suggested_videos_service
        suggested_videos_service_pb2_grpc.add_SuggestedVideoServiceServicer_to_server(self, grpc_server)

    def GetRelatedVideos(self, request, context):
        """Gets videos related to another video
        """
        print ">>> SuggestedVideosService:GetRelatedVideos: "
        print request
        # TODO: implement service call
        #result = self.suggested_videos_service.get_related_videos(UUID(request.video_id), request.page_size, request.paging_state)
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSuggestedForUser(self, request, context):
        """Gets personalized video suggestions for a user
        """
        print ">>> SuggestedVideosService:GetSuggestedForUser: "
        print request
        # TODO: implement service call
        #result = self.suggested_videos_service.get_suggested_for_user(UUID(requestuser_id, request.page_size, request.paging_state):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

