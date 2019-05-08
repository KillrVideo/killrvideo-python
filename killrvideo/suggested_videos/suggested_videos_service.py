from suggested_videos_events_kafka import SuggestedVideosConsumer
from dse_graph import DseGraph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.traversal import gte, neq, within, Scope, Operator, Order, Column
import logging
import dateutil.parser

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

# constants
MIN_RATING = 4
NUM_RATINGS_TO_SAMPLE = 1000
LOCAL_USER_RATINGS_TO_SAMPLE = 5
NUM_RECOMMENDATIONS = 5

class SuggestedVideosService(object):
    """Provides methods that implement functionality of the Suggested Videos Service."""


    def __init__(self, session):
        self.session = session
        self.graph = DseGraph.traversal_source(session=self.session, graph_name='killrvideo_video_recommendations')
        logging.debug('Graph traversal source: ' + str(self.graph) + ' verts' + str(self.graph.V()))
        self.suggested_videos_consumer = SuggestedVideosConsumer(self)


    def get_related_videos(self, video_id, page_size, paging_state):
        # TODO: implement method

        # Uses similar algorithm to get_suggested_for_user, but starts with a video instead of a user
        # find users that watched (rated) this video highly
        # for those users, grab N highly rated videos and assemble results 

        traversal = self.graph.V().has('video', 'videoId', video_id).as_('^video') \
            .inE('rated').has('rating', gte(MIN_RATING)) \
            .sample(NUM_RATINGS_TO_SAMPLE).by('rating').outV() \
            .where(neq('^video')) \
            .local(__.outE('rated').has('rating', gte(MIN_RATING)).limit(LOCAL_USER_RATINGS_TO_SAMPLE)) \
            .sack(Operator.assign).by('rating').inV() \
            .filter(__.in_('uploaded').hasLabel('user')) \
            .group().by().by(__.sack().sum()) \
            .order(Scope.local).by(Column.values, Order.decr) \
            .limit(Scope.local, NUM_RECOMMENDATIONS).select(Column.keys).unfold() \
            .project('video', 'video_id', 'added_date', 'name', 'preview_image_location', 'user_id') \
            .by().by('videoId').by('added_date').by('name').by('preview_image_location').by(__.in_('uploaded').values('userId'))

        logging.debug('Traversal: ' + str(traversal.bytecode))

        results = traversal.toList()
        logging.debug('Traversal generated ' + str(len(results)) + ' results')

        videos = list()
        for result in results:
            logging.debug('Traversal Result: ' + str(result))
            videos.append(VideoPreview(video_id=result['video_id'],
                                       added_date=dateutil.parser.parse(result['added_date'], ignoretz=True),
                                       user_id=result['user_id'], name=result['name'],
                                       preview_image_location=result['preview_image_location']))

        return RelatedVideosResponse(video_id=video_id, videos=videos, paging_state=None)


    def get_suggested_for_user(self, user_id, page_size, paging_state):

        # Note: we're building a single graph traversal, but describing in three parts for readability

        # Part 1: finding "similar users"
        # - find the vertex for the user
        # - get all of the videos the user watched and store them
        # - go back to our current user
        # - for the video's I rated highly...
        # - what other users rated those videos highly? (this is like saying "what users share my taste")
        # - but don't grab too many, or this won't work OLTP, and "by('rating')" favors the higher ratings
        # - (except the current user)

        # Part 2: finding videos that were highly rated by similar users
        # - For those users who share my taste, grab N highly rated videos.
        # - Save the rating so we can sum the scores later, and use sack()
        # - because it does not require path information. (as()/select() was slow)
        # - excluding the videos the user has already watched
        # - Filter out the video if for some reason there is no uploaded edge to a user
        # - what are the most popular videos as calculated by the sum of all their ratings

        # Part 3: now that we have that big map of [video: score], let's order it
        # - then grab properties of the video and the user who uploaded each video using project()

        traversal = self.graph.V().has('user', 'userId', user_id).as_('^user') \
            .map(__.out('rated').dedup().fold()).as_('^watchedVideos') \
            .select('^user') \
            .outE('rated').has('rating', gte(MIN_RATING)).inV() \
            .inE('rated').has('rating', gte(MIN_RATING)) \
            .sample(NUM_RATINGS_TO_SAMPLE).by('rating').outV() \
            .where(neq('^user')) \
            .local(__.outE('rated').has('rating', gte(MIN_RATING)).limit(LOCAL_USER_RATINGS_TO_SAMPLE)) \
            .sack(Operator.assign).by('rating').inV() \
            .filter(__.in_('uploaded').hasLabel('user')) \
            .group().by().by(__.sack().sum()) \
            .order(Scope.local).by(Column.values, Order.decr) \
            .limit(Scope.local, NUM_RECOMMENDATIONS).select(Column.keys).unfold() \
            .project('video', 'video_id', 'added_date', 'name', 'preview_image_location', 'user_id') \
            .by().by('videoId').by('added_date').by('name').by('preview_image_location').by(__.in_('uploaded').values('userId'))

        # TODO: this step needs to be reinserted after .sack and before .filter
        #.not_(__.where(within('^watchedVideos'))) \

        logging.debug('Traversal: ' + str(traversal.bytecode))

        results = traversal.toList()
        logging.debug('Traversal generated ' + str(len(results)) + ' results')

        videos = list()
        for result in results:
            logging.debug('Traversal Result: ' + str(result))
            videos.append(VideoPreview(video_id=result['video_id'],
                                       added_date=dateutil.parser.parse(result['added_date'], ignoretz=True),
                                       user_id=result['user_id'], name=result['name'],
                                       preview_image_location=result['preview_image_location']))

        return SuggestedVideosResponse(user_id=user_id, videos=videos, paging_state=None)


    def handle_user_created(self, user_id, first_name, last_name, email, timestamp):
        logging.debug('SuggestedVideosService:handle_user_created, id is: ' + str(user_id) +
                      ', first name: ' + first_name +
                      ', last name: ' + last_name + ', email: ' + email +
                      ', timestamp: ' + str(timestamp) + ', graph: ' + str(self.graph))

        self.graph.addV('user').property('userId', user_id).property('email', email) \
            .property('added_date', timestamp).next()


    def handle_youtube_video_added(self, video_id, user_id, name, description, location, preview_image_location,
                                   tags, added_date, timestamp):
        logging.debug('SuggestedVideosService:handle_youtube_video_added, video ID: ' + str(video_id) +
                      ', user ID: ' + str(user_id) + ', name: ' + name + ', description: ' + description +
                      ', location: ' + location + ', preview_image_location: ' + preview_image_location +
                      ', tags: ' + str(tags) + ', timestamp: ' + str(timestamp))

        # Note: building a single traversal, but broken into several steps for readability

        # locate user vertex
        traversal = self.graph.V().has('user', 'userId', user_id).as_('^user')

        # add video vertex
        traversal = traversal.addV('video').property('videoId', video_id)\
            .property('added_date', added_date) \
            .property('description', description) \
            .property('name', name) \
            .property('preview_image_location', preview_image_location) \
            .as_('^video')

        # add edge from user to video vertex
        traversal = traversal.addE('uploaded').from_('^user').to('^video').property('added_date', added_date)

        # find vertices for tags and add edges from video vertex
        for tag in tags:
            traversal = traversal.addE('taggedWith').from_('^video').to(__.coalesce(
                __.V().has('tag', 'name', tag),
                __.addV('tag').property('name', tag).property('tagged_date', added_date)))

        # execute the traversal
        traversal.iterate()


    def handle_user_rated_video(self, video_id, user_id, rating, timestamp):

        logging.debug('SuggestedVideosService:handle_user_rated_video, video id: ' + str(video_id) +
                      ', user ID: ' + str(user_id) +
                      ', rating: ' + str(rating) +
                      ', timestamp: ' + str(timestamp))

        # locate the video and user vertices and add an edge to represent the rating
        self.graph.V().has('user', 'userId', user_id) \
            .addE('rated').to(__.V().has('video', 'videoId', video_id)) \
            .property('rating', rating) \
            .iterate()
