import grpc
import logging
from common.common_types_conversions import UUID_to_grpc, grpc_to_UUID
from comments_service_pb2 import CommentOnVideoResponse
import comments_service_pb2_grpc

class CommentsServiceServicer(comments_service_pb2_grpc.CommentsServiceServicer):
    """Provides methods that implement functionality of the Comments Service."""

    def __init__(self, grpc_server, comments_service):
        logging.debug("CommentsServiceServicer started")
        self.comments_service = comments_service
        comments_service_pb2_grpc.add_CommentsServiceServicer_to_server(self, grpc_server)

    def CommentOnVideo(self, request, context):
        """Add a new comment to a video
        """
        print ">>> CommentsService:CommentOnVideo: "
        print request
        self.comments_service.comment_on_video(grpc_to_UUID(request.video_id.value),
                                               grpc_to_UUID(request.user_id.value), request.comment)
        return CommentOnVideoResponse()

    def GetUserComments(self, request, context):
        """Get comments made by a user
        """
        print ">>> CommentsService:GetUserComments: "
        print request
        # TODO: implement service call
        #self.comments_service.get_user_comments(grpc_to_UUID(request.user_id.value), page_size,
        #                                        grpc_to_UUID(request.starting_comment_id.value), paging_state)
        #iterate to build results
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetVideoComments(self, request, context):
        """Get comments made on a video
        """
        print ">>> CommentsService:GetVideoComments: "
        print request
        # TODO: implement service call
        #self.comments_service.get_video_comments(grpc_to_UUID(request.video_id.value), page_size,
        #                                         grpc_to_UUID(request.starting_comment_id.value), paging_state)
        #iterate to build results
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

