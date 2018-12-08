import grpc

import ratings_service_pb2
import ratings_service_pb2_grpc

class RatingsServiceServicer(ratings_service_pb2_grpc.RatingsServiceServicer):
    """Provides methods that implement functionality of the Ratings Service."""

    def __init__(self, grpc_server, ratings_service):
        print "RatingsServiceServicer started"
        self.ratings_service = ratings_service
        ratings_service_pb2_grpc.add_RatingsServiceServicer_to_server(self, grpc_server)

    def RateVideo(self, request, context):
        """Rate a video
        """
        print ">>> RatingsService:RateVideo: "
        print request
        # TODO: implement service call
        #self.ratings_service.rate_video(UUID(request.video_id), UUID(user_id), rating):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')
        # TODO: publish UserRatedVideo event

    def GetRating(self, request, context):
        """Gets the current rating stats for a video
        """
        print ">>> RatingsService:GetRating: "
        print request
        # TODO: implement service call
        #self.ratings_service.get_rating(UUID(request.video_id))
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserRating(self, request, context):
        """Gets a user's rating of a specific video and returns 0 if the user hasn't rated the video
        """
        print ">>> RatingsService:GetUserRating: "
        print request
        # TODO: implement service call
        #self.ratings_service.get_user_rating(UUID(request.video_id), request.(user_id))
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

