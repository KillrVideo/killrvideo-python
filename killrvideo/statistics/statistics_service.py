from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class VideoPlaybackStatsModel(Model):
    """Model class that maps to the video_playback_stats table"""
    __table_name__ = 'video_playback_stats'
    video_id = columns.UUID(primary_key=True)
    views = columns.Counter()

class StatisticsService(object):
    """Provides methods that implement functionality of the Statistics Service."""

    def __init__(self):
        # TODO: implement method
        return

    def record_playback_started(self, video_id):
        # TODO: implement method
        return

    def get_number_of_plays(self, video_id):
        # TODO: implement method
        return
