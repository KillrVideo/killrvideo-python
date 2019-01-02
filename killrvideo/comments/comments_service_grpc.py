import grpc
<<<<<<< HEAD
from uuid import UUID
from time_uuid import TimeUUID
from common.common_types_conversions import UUID_to_grpc, grpc_to_UUID, grpc_totimeUUID
from comments_service_pb2 import CommentOnVideoRequest, CommentOnVideoResponse, GetUserCommentsRequest, GetUserCommentsResponse, GetVideoCommentsRequest, GetVideoCommentsResponse
=======
import logging
from common.common_types_conversions import UUID_to_grpc, grpc_to_UUID
from comments_service_pb2 import CommentOnVideoResponse
>>>>>>> 7512ee207effceb1ee60b329ed4c604b3820e528
import comments_service_pb2_grpc

def CommentsByUserModel_to_GetUserComments(result):
    return GetUserCommentsRequest(user_id=UUID_to_grpc(result.user_id), page_size=result.page_size, starting_comment_id=UUID_to_grpc(result.starting_comment_id), paging_state=result.paging_state)

def UserComments_to_GetUserCommentsResponse(results):
    response = GetUserCommentsResponse(paging_state=results.paging_state)
    if isinstance(results, (list,)):    # most preferred way to check if it's list
        response.comments.extend(map(CommentsByUserModel_to_GetUserComments, results.comments))
    elif results is not None:  # single result
        response.comments.extend([CommentsByUserModel_to_GetUserComments(results.comments)])
    return response

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
        starting_comment_id = None
        if request.starting_comment_id.value:
            starting_comment_id = grpc_to_UUID(request.starting_comment_id)
        print "here"
        result = self.comments_service.get_user_comments(user_id=grpc_to_UUID(request.user_id.value), page_size=request.page_size, starting_comment_id=grpc_toUUID(request.starting_comment_id.value), paging_state=request.paging_state)
        print result
        return UserComments_to_GetUserCommentsResponse(result)

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

