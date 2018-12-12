from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class VideosModel(Model):
    """Model class that maps to the videos table"""
    __table_name__ = 'videos'
    video_id = columns.UUID(primary_key=True)
    user_id = columns.UUID()
    name = columns.Text()
    description  = columns.Text()
    location = columns.Text()
    location_type = columns.Integer()
    preview_image_location = columns.Text()
    tags = columns.Set(columns.Text)
    added_date = columns.DateTime()

class LatestVideosModel(Model):
    """Model class that maps to the latest_videos table"""
    __table_name__ = 'latest_videos'
    yyyymmdd = columns.Text(primary_key=True)
    added_date = columns.DateTime(primary_key=True, clustering_order='DESC')
    video_id = columns.UUID(primary_key=True, clustering_order='ASC')
    user_id = columns.UUID()
    name  = columns.Text()
    preview_image_location = columns.Text()

class UserVideosModel(Model):
    """Model class that maps to the user_videos table"""
    __table_name__ = 'user_videos'
    user_id = columns.UUID(primary_key=True)
    added_date = columns.DateTime(primary_key=True, clustering_order='DESC')
    video_id = columns.UUID(primary_key=True, clustering_order='ASC')
    password  = columns.Text()
    name = columns.Text()
    preview_image_location = columns.Text()

class LatestVideoPreviews():
    def __init__(self, paging_state, videos):
        self.paging_state = paging_state
        self.videos = videos

class UserVideoPreviews():
    def __init__(self, paging_state, videos):
        self.paging_state = paging_state
        self.videos = videos

class VideoCatalogService(object):
    """Provides methods that implement functionality of the Video Catalog Service."""

    def __init__(self):
        return

    def submit_uploaded_video(self, video_id, user_id, name, description, tags, upload_url):
        # TODO: implement method
        return

    def submit_youtube_video(self, video_id, user_id, name, description, tags, you_tube_video_id):
        # TODO: implement method
        return

    def get_video(self, video_id):
        # TODO: implement method
        return

    def get_video_previews(self, video_ids):
        # TODO: implement method
        return

    def get_latest_video_previews(self, page_size, starting_added_date, starting_video_id, paging_state):
        # TODO: implement method
        return

    def get_user_video_previews(self, user_id, page_size, starting_added_date, starting_video_id, paging_state):
        # TODO: implement method
        return





