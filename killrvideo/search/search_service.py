from cassandra.cluster import Cluster
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.query import LWTException
import cassandra.cqlengine.connection
from uuid import UUID


class VideosByTagModel(Model):
    """Model class that maps to the videos_by_tag table"""
    __table_name__ = 'videos_by_tag'
    tag = columns.Text(primary_key=True)
    video_id = columns.UUID(primary_key=True)
    added_date = columns.DateTime()
    user_id = columns.UUID()
    name = columns.Text()
    preview_image_location = columns.Text()
    tagged_date = columns.DateTime()

class TagsByLetterModel(Model):
    """Model class that maps to the tags_by_letter table"""
    __table_name__ = 'tags_by_letter'
    first_letter = columns.Text(primary_key=True)
    tag = columns.Text(primary_key=True)

class SearchService(object):
    """Provides methods that implement functionality of the Search Service."""

    def __init__(self):
        # TODO: implement method
        return

    def search_videos(self, query, page_size, paging_state):
        # TODO: implement method
        return

    def get_query_suggestions(self, query, page_size):
        # TODO: implement method
        return
