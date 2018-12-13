from datetime import datetime
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.query import BatchQuery

YOUTUBE = 0
UPLOAD = 1

class VideosModel(Model):
    """Model class that maps to the videos table"""
    __table_name__ = 'videos'
    video_id = columns.UUID(primary_key=True, db_field='videoid')
    user_id = columns.UUID(db_field='userid')
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
    video_id = columns.UUID(primary_key=True, clustering_order='ASC', db_field='videoid')
    user_id = columns.UUID(db_field='userid')
    name  = columns.Text()
    preview_image_location = columns.Text()

class UserVideosModel(Model):
    """Model class that maps to the user_videos table"""
    __table_name__ = 'user_videos'
    user_id = columns.UUID(primary_key=True, db_field='userid')
    added_date = columns.DateTime(primary_key=True, clustering_order='DESC')
    video_id = columns.UUID(primary_key=True, clustering_order='ASC', db_field='videoid')
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

    def __init__(self, session):
        self.session = session

        # Prepared statements for GetLatestVideoPreviews()
        self.latestVideoPreview_startingPointPrepared = \
            session.prepare("SELECT * FROM latest_videos WHERE yyyymmdd = ? AND (added_date, videoid) <= (?, ?)")
        self.latestVideoPreview_noStartingPointPrepared = \
            session.prepare("SELECT * FROM latest_videos WHERE yyyymmdd = ?")

        # Prepared statements for GetUserVideoPreviews()
        self.userVideoPreview_startingPointPrepared = \
            session.prepare("SELECT * FROM user_videos WHERE userid = ? AND (added_date, videoid) <= (?, ?)")
        self.userVideoPreview_noStartingPointPrepared = \
            session.prepare("SELECT * FROM user_videos WHERE userid = ?")


    def submit_youtube_video(self, video_id, user_id, name, description, tags, you_tube_video_id):
        # validate inputs
        if not video_id:
            raise ValueError('video_id should be provided for submit youtube video request')
        elif not user_id:
            raise ValueError('user_id should be provided for submit youtube video request')
        elif not name:
            raise ValueError('video name should be provided for submit youtube video request')
        elif not description:
            raise ValueError('video description should be provided for submit youtube video request')
        elif not you_tube_video_id:
            raise ValueError('video YouTube id should be provided for submit youtube video request')

        # formulate the preview location
        preview_image_location = ''

        # formulate the time-based values
        now = datetime.today()
        yyyymmdd = now.strftime('%Y%m%d')

        # create and execute batch statement to insert into multiple tables
        batch_query = BatchQuery()
        VideosModel.batch(batch_query).create(video_id=video_id, user_id=user_id, name=name, description=description,
                                              location=you_tube_video_id, location_type=YOUTUBE,
                                              preview_image_location=preview_image_location, tags=tags,
                                              added_date=now)
        LatestVideosModel.batch(batch_query).create(yyyymmdd=yyyymmdd, added_date=now, video_id=video_id,
                                                    user_id=user_id, name=name,
                                                    preview_image_location=preview_image_location)
        UserVideosModel.batch(batch_query).create(user_id=user_id, added_date=now, video_id=video_id,
                                                  name=name, preview_image_location=preview_image_location)
        batch_query.execute()


    def get_video(self, video_id):
        if not video_id:
            raise ValueError('No Video ID provided')

        return VideosModel.get(video_id=video_id)


    def get_video_previews(self, video_ids):
        if not video_ids:
            raise ValueError('No Video IDs provided')

        # see: https://datastax.github.io/python-driver/cqlengine/queryset.html#retrieving-objects-with-filters
        return VideosModel.filter(video_id__in=video_ids).get()


    def get_latest_video_previews(self, page_size, starting_added_date, starting_video_id, paging_state):
        if page_size <= 0:
            raise ValueError('Page size should be strictly positive for get latest preview video request')

        result = LatestVideoPreviews(None, None)
        return result

    def get_user_video_previews(self, user_id, page_size, starting_added_date, starting_video_id, paging_state):
        if page_size <= 0:
            raise ValueError('Page size should be strictly positive for get user preview video request')

        result = UserVideoPreviews(None, None)
        return result





