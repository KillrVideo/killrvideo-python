from cassandra.cluster import Cluster
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.query import LWTException
import cassandra.cqlengine.connection
from uuid import UUID

class VideoRecommendationsModel(Model):
    """Model class that maps to the video_recommendations table"""
    __table_name__ = 'video_recommendations'
    user_id = columns.UUID(primary_key=True)
    added_date = columns.DateTime(primary_key=True, clustering_order='DESC')
    video_id = columns.UUID(primary_key=True, clustering_order='ASC')
    rating = columns.Float()
    authorid = columns.UUID()
    name = columns.Text()
    preview_image_location = columns.Text()

class VideoRecommendationsByVideoModel(Model):
    """Model class that maps to the video_recommendations_by_video table"""
    __table_name__ = 'video_recommendations_by_video'
    video_id = columns.UUID(primary_key=True)
    user_id = columns.UUID(primary_key=True, clustering_order='ASC')
    rating = columns.Float()
    added_date = columns.DateTime(static=True)
    authorid = columns.UUID(static=True)
    name = columns.Text(static=True)
    preview_image_location = columns.Text(static=True)

class SuggestedVideosService(object):
    """Provides methods that implement functionality of the Suggested Videos Service."""

    def __init__(self):
        # TODO: implement method
        return

    def get_related_videos(self, video_id, page_size, paging_state):
        # TODO: implement method
        return

    def get_suggested_for_user(self, user_id, page_size, paging_state):
        # TODO: implement method
        return

