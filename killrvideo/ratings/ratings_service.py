from cassandra.cluster import Cluster
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.query import LWTException
import cassandra.cqlengine.connection
from uuid import UUID

class VideoRatingsModel(Model):
    """Model class that maps to the video_ratings table"""
    __table_name__ = 'video_ratings'
    video_id = columns.UUID(primary_key=True)
    rating_counter = columns.Counter()
    rating_total = columns.Counter()

class VideoRatingsByUserModel(Model):
    """Model class that maps to the video_ratings_by_user table"""
    __table_name__ = 'video_ratings_by_user'
    video_id = columns.UUID(primary_key=True)
    user_id = columns.UUID(primary_key=True)
    rating = columns.Integer()

class RatingsService(object):
    """Provides methods that implement functionality of the Ratings Service."""

    def __init__(self):
        # TODO: implement method
        return

    def rate_video(self, video_id, user_id, rating):
        # TODO: implement method
        return

    def get_rating(self, video_id):
        # TODO: implement method
        return

    def get_user_rating(self, video_id, user_id):
        # TODO: implement method
        return
