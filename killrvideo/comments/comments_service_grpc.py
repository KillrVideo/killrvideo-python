from concurrent import futures
import time

import grpc
import etcd

import comments_service_pb2
import comments_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

#TODO refactor service implementation to separate class
def comment_on_video(video_id, user_id, comment_id, comment):
    return

def get_user_comments(user_id, page_size, starting_comment_id, paging_state):
    return

def user_comment(comment_id, video_id, comment, comment_timestamp):
    return


class CommentsServiceServicer(comments_service_pb2_grpc.CommentsServiceServicer):
    """Provides methods that implement functionality of the Comments Service."""

    def __init__(self):
        print "started"
        return

    def CommentOnVideo(self, request, context):
        """Add a new comment to a video
        """
        print request
        # TODO: implement service call
        #comment_on_video(request.video_id, request.user_id, request.comment)
        # TODO: publish UserCommentedOnVideo event
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserComments(self, request, context):
        """Get comments made by a user
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetVideoComments(self, request, context):
        """Get comments made on a video
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    comments_service_pb2_grpc.add_CommentsServiceServicer_to_server(
        CommentsServiceServicer(), server)
    server.add_insecure_port('[::]:8899')
    #port = server.add_insecure_port('[::]:0') # allow GRPC to choose port
    #print "Starting at port: ", port
    server.start()

    # TODO: Fix hardcoded values
    etcd_client = etcd.Client(host='10.0.75.1', port=2379)
    etcd_client.write('/killrvideo/services/UserManagementService/killrvideo-python', "10.0.75.1:8899")

    # only need this temporarily until such time as we're running multiple services?
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

