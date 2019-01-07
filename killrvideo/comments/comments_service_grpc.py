import grpc
import logging
from uuid import UUID
from time_uuid import TimeUUID
from common.common_types_conversions import UUID_to_grpc, grpc_to_UUID, grpc_totimeUUID, TimeUUID_to_grpc
from comments_service_pb2 import UserComment, CommentOnVideoRequest, CommentOnVideoResponse, GetUserCommentsRequest, GetUserCommentsResponse, GetVideoCommentsRequest, GetVideoCommentsResponse, VideoComment
import comments_service_pb2_grpc
from comments_events_pb2 import UserCommentedOnVideo

def CommentsByUserModel_to_GetUserComments(result):
    return UserComment(comment_id=TimeUUID_to_grpc(result.comment_id), 
                       video_id=UUID_to_grpc(result.video_id), 
                       comment=result.comment)

def UserComments_to_GetUserCommentsResponse(results):
    response = GetUserCommentsResponse(paging_state=results.paging_state)
    if isinstance(results.comments, (list,)):    # most preferred way to check if it's list
        response.comments.extend(map(CommentsByUserModel_to_GetUserComments, results.comments))
    elif results.comments is not None:  # single result
        response.comments.extend([CommentsByUserModel_to_GetUserComments(results.comments)])
    return response

def CommentsByVideoModel_to_GetVideoComments(result):
    return VideoComment(comment_id=TimeUUID_to_grpc(result.comment_id), 
                        user_id=UUID_to_grpc(result.user_id), 
                        comment=result.comment)

def VideoComments_to_GetVideoCommentsResponse(results):
    response = GetVideoCommentsResponse(paging_state=results.paging_state)
    if isinstance(results.comments, (list,)):    # most preferred way to check if it's list
        response.comments.extend(map(CommentsByVideoModel_to_GetVideoComments, results.comments))
    elif results.comments is not None:  # single result
        response.comments.extend([CommentsByVideoModel_to_GetVideoComments(results.comments)])
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
        logging.debug(">>> CommentsService:CommentOnVideo: ")
        logging.debug(request)
        self.comments_service.comment_on_video(UUID(request.video_id.value),
                                               UUID(request.user_id.value), 
                                               UUID (request.comment_id.value), 
                                               request.comment)
        #Publish UserCommentedOnVideo event
        event = UserCommentedOnVideo(video_id=request.video_id,
                                     user_id=request.user_id,
                                     comment_id=request.comment_id)
        return CommentOnVideoResponse()

    def GetUserComments(self, request, context):
        """Get comments made by a user
        """
        logging.debug(">>> CommentsService:GetUserComments: ")
        logging.debug(request)
        starting_comment_id = None
        if request.starting_comment_id.value:
            starting_comment_id = grpc_totimeUUID(request.starting_comment_id)
        result = self.comments_service.get_user_comments(user_id=grpc_to_UUID(request.user_id), 
                                                         page_size=request.page_size, 
                                                         starting_comment_id=starting_comment_id, 
                                                         paging_state=request.paging_state)
        logging.debug(result)
        return UserComments_to_GetUserCommentsResponse(result)

    def GetVideoComments(self, request, context):
        """Get comments made on a video
        """
        logging.debug(">>> CommentsService:GetVideoComments: ")
        logging.debug(request)
        starting_comment_id = None
        if request.starting_comment_id.value:
            starting_comment_id = grpc_totimeUUID(request.starting_comment_id)
        result = self.comments_service.get_video_comments(video_id=grpc_to_UUID(request.video_id), 
                                                          page_size=request.page_size, 
                                                          starting_comment_id=starting_comment_id, 
                                                          paging_state=request.paging_state)
        logging.debug(result)
        return VideoComments_to_GetVideoCommentsResponse(result)

