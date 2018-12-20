from cassandra.cluster import Cluster
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.query import LWTException
import cassandra.cqlengine.connection
from uuid import UUID

class VideoRecommendation():
    user_id = columns.UUID(primary_key=True)
    added_date = columns.DateTime(primary_key=True, clustering_order='DESC')
    video_id = columns.UUID(primary_key=True, clustering_order='ASC')
    rating = columns.Float()
    authorid = columns.UUID()
    name = columns.Text()
    preview_image_location = columns.Text()

    def __init__(self, user_id, added_date, video_id, rating, author_id, name, preview_image_location):
        self.paging_state = paging_state
        self.videos = videos

class SuggestedVideosService(object):
    """Provides methods that implement functionality of the Suggested Videos Service."""

    def __init__(self, session):
        self.session = session

    def get_related_videos(self, video_id, page_size, paging_state):
        # TODO: implement method
        return

    def get_suggested_for_user(self, user_id, page_size, paging_state):
        # TODO: implement method
        return

