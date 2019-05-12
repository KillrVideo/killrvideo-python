import logging
from dse.cqlengine import columns
from dse.cqlengine.models import Model

class VideoPlaybackStatsModel(Model):
    """Model class that maps to the video_playback_stats table"""
    __table_name__ = 'video_playback_stats'
    video_id = columns.UUID(primary_key=True, db_field='videoid')
    views = columns.Counter()

class StatisticsService(object):
    """Provides methods that implement functionality of the Statistics Service."""

    def __init__(self):
        return

    def record_playback_started(self, video_id):
        # validate inputs
        if not video_id:
            raise ValueError('video_id should be provided for record/playback started request')

        # updating counter column 'views' - values are interpreted as amount to increment
        VideoPlaybackStatsModel(video_id=video_id).update(views=1)


    def get_number_of_plays(self, video_ids):
        if not video_ids:
            raise ValueError('No Video IDs provided')

        # see: https://datastax.github.io/python-driver/cqlengine/queryset.html#retrieving-objects-with-filters
        # filter().all() returns a ModelQuerySet, we iterate over the query set to get the Model instances
        stats_results = VideoPlaybackStatsModel.filter(video_id__in=video_ids).all()
        stats_list = list()
        results_video_ids = video_ids[:] # make a copy of requested video_ids to make sure we get a result for each

        for stats in stats_results:
            logging.debug(stats)
            stats_list.append(stats)
            results_video_ids.remove(stats.video_id) # got one of our requested videos

        # create zero-count view results for any requested video_id missing from the query results
        for missing_video_id in results_video_ids:
            stats_list.append(VideoPlaybackStatsModel(video_id=missing_video_id, views=0))

        return stats_list