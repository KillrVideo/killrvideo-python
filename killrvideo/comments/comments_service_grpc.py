import grpc

import comments_service_pb2
import comments_service_pb2_grpc

class CommentsServiceServicer(comments_service_pb2_grpc.CommentsServiceServicer):
    """Provides methods that implement functionality of the Comments Service."""

    def __init__(self, grpc_server, comments_service):
        print "CommentsServiceServicer started"
        self.comments_service = comments_service
        comments_service_pb2_grpc.add_CommentsServiceServicer_to_server(self, grpc_server)

    def CommentOnVideo(self, request, context):
        """Add a new comment to a video
        """
        print ">>> CommentsService:CommentOnVideo: "
        print request
        # TODO: implement service call
        #self.comments_service.comment_on_video(UUID(request.video_id.value), UUID(request.user_id.value), request.comment)
        # TODO: publish UserCommentedOnVideo event
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserComments(self, request, context):
        """Get comments made by a user
        """
        print ">>> CommentsService:GetUserComments: "
        print request
        # TODO: implement service call
        #self.comments_service.get_user_comments(UUID(request.user_id.value), page_size, UUID(request.starting_comment_id.value), paging_state)
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
        #self.comments_service.get_video_comments(UUID(request.video_id.value), page_size, UUID(request.starting_comment_id.value), paging_state)
        #iterate to build results
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

