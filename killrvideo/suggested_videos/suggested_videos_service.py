from suggested_videos_events_kafka import SuggestedVideosConsumer

class VideoPreview():
    def __init__(self, video_id, added_date, name, preview_image_location, user_id):
        self.video_id = video_id
        self.added_date = added_date
        self.name = name
        self.preview_image_location = preview_image_location
        self.user_id = user_id

class RelatedVideosResponse():
    def __init__(self, video_id, videos, paging_state):
        self.video_id = video_id
        self.videos = videos
        self.paging_state = paging_state

class SuggestedVideosResponse():
    def __init__(self, user_id, videos, paging_state):
        self.user_id = user_id
        self.videos = videos
        self.paging_state = paging_state


class SuggestedVideosService(object):
    """Provides methods that implement functionality of the Suggested Videos Service."""

    def __init__(self, session):
        self.session = session
        self.suggested_videos_consumer = SuggestedVideosConsumer(self)


    def get_related_videos(self, video_id, page_size, paging_state):
        # TODO: implement method
        return RelatedVideosResponse(video_id=video_id, videos=None, paging_state=None)


    def get_suggested_for_user(self, user_id, page_size, paging_state):
        # TODO: implement method
        return SuggestedVideosResponse(user_id=user_id, videos=None, paging_state=None)


    def handle_youtube_video_added(self, video_id, user_id, name, description, location, preview_image_location,
                                   tags, added_date, timestamp):
        # TODO: implement method
        return


    def handle_user_created(self, user_id, first_name, last_name, email, timestamp):
        # TODO: implement method
        return


    def handle_user_rated_video(self, video_id, user_id, rating, timestamp):
        # TODO: implement method
        return
