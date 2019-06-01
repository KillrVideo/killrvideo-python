import logging
from ratings_service_pb2 import RateVideoResponse, GetRatingResponse, GetUserRatingResponse
from ratings_events_pb2 import UserRatedVideo
import ratings_service_pb2_grpc
from common.common_types_conversions import UUID_to_grpc, grpc_to_UUID


class RatingsServiceServicer(ratings_service_pb2_grpc.RatingsServiceServicer):
    """Provides methods that implement functionality of the Ratings Service."""

    def __init__(self, grpc_server, ratings_service):
        logging.debug("RatingsServiceServicer started")
        self.ratings_service = ratings_service
        ratings_service_pb2_grpc.add_RatingsServiceServicer_to_server(self, grpc_server)

    def RateVideo(self, request, context):
        """Rate a video
        """
        logging.debug(">>> RatingsService:RateVideo: ")
        logging.debug(request)
        video_id = grpc_to_UUID(request.video_id)
        user_id = grpc_to_UUID(request.user_id)

        self.ratings_service.rate_video(video_id=video_id, user_id=user_id, rating=request.rating)

        return RateVideoResponse()

    def GetRating(self, request, context):
        """Gets the current rating stats for a video
        """
        logging.debug(">>> RatingsService:GetRating: ")
        logging.debug(request)
        result = self.ratings_service.get_rating(grpc_to_UUID(request.video_id))
        logging.debug(result)
        response = GetRatingResponse(video_id=UUID_to_grpc(result.video_id), ratings_count=result.rating_counter,
                                 ratings_total=result.rating_total)
        logging.debug(response)
        return response

    def GetUserRating(self, request, context):
        """Gets a user's rating of a specific video and returns 0 if the user hasn't rated the video
        """
        logging.debug(">>> RatingsService:GetUserRating: ")
        logging.debug(request)
        result = self.ratings_service.get_user_rating(grpc_to_UUID(request.video_id), grpc_to_UUID(request.user_id))
        logging.debug(result)
        response = GetUserRatingResponse(video_id=UUID_to_grpc(result.video_id), user_id=UUID_to_grpc(result.user_id),
                                     rating=result.rating)
        logging.debug(response)
        return response
