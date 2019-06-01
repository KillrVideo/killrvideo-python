from datetime import datetime
from dse.cqlengine import columns
from dse.cqlengine.models import Model
from dse.cqlengine.query import BatchQuery, DoesNotExist
from .ratings_events_kafka import RatingPublisher

class VideoRatingsModel(Model):
    """Model class that maps to the video_ratings table"""
    __table_name__ = 'video_ratings'
    video_id = columns.UUID(primary_key=True, db_field='videoid')
    rating_counter = columns.Counter()
    rating_total = columns.Counter()

class VideoRatingsByUserModel(Model):
    """Model class that maps to the video_ratings_by_user table"""
    __table_name__ = 'video_ratings_by_user'
    video_id = columns.UUID(primary_key=True, db_field='videoid')
    user_id = columns.UUID(primary_key=True, db_field='userid')
    rating = columns.Integer()

class RatingsService(object):
    """Provides methods that implement functionality of the Ratings Service."""

    def __init__(self):
        self.rating_publisher = RatingPublisher()


    def rate_video(self, video_id, user_id, rating):
        # validate inputs
        if not video_id:
            raise ValueError('video_id should be provided for rate video request')
        elif not user_id:
            raise ValueError('user_id should be provided for rate video request')
        elif not rating:
            raise ValueError('rating should be provided for rate video request')

        now = datetime.utcnow()

        # create and execute batch statement to insert into multiple tables
        batch_query = BatchQuery(timestamp=now)
        VideoRatingsByUserModel.batch(batch_query).create(video_id=video_id, user_id=user_id, rating=rating)
        # updating counter columns rating_counter and rating_total - values are interpreted as amount to increment
        VideoRatingsModel(video_id=video_id).update(rating_counter=1, rating_total=rating).batch(batch_query)

        batch_query.execute()

        # Publish UserRatedVideo event
        self.rating_publisher.publish_user_rated_video_event(video_id=video_id, user_id=user_id, rating=rating,
                                                             timestamp=now)


    def get_rating(self, video_id):
        if not video_id:
            raise ValueError('No Video ID provided')

        try:
            return VideoRatingsModel.get(video_id=video_id)
        except DoesNotExist:
            # If no value is returned, we should still build a response with 0 as rating value
            return VideoRatingsModel(video_id=video_id, rating_counter=0, rating_total=0)


    def get_user_rating(self, video_id, user_id):
        if not video_id:
            raise ValueError('No Video ID provided')
        elif not user_id:
            raise ValueError('No User ID provided')

        try:
            return VideoRatingsByUserModel.get(video_id=video_id, user_id=user_id)
        except DoesNotExist:
            # If no value is returned, we should still build a response with 0 as rating value
            return VideoRatingsByUserModel(video_id=video_id, user_id=user_id, rating=0)

