from suggested_videos_events_kafka import SuggestedVideosConsumer
from dse_graph import DseGraph
import logging

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
        self.graph = DseGraph.traversal_source(session=self.session, graph_name='killrvideo_video_recommendations')
        logging.debug('Graph traversal source: ' + str(self.graph) + ' verts' + str(self.graph.V()))
        self.suggested_videos_consumer = SuggestedVideosConsumer(self)

    def get_related_videos(self, video_id, page_size, paging_state):
        # TODO: implement method
        return RelatedVideosResponse(video_id=video_id, videos=None, paging_state=None)

    def get_suggested_for_user(self, user_id, page_size, paging_state):
        # TODO: implement method
        return SuggestedVideosResponse(user_id=user_id, videos=None, paging_state=None)

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

        # add Video vertex
        video = self.graph.addV('video').property('videoId', video_id)\
            .property('added_date', added_date)\
            .property('description', description) \
            .property('name', name)\
            .property('preview_image_location', preview_image_location)\
            .next()
        logging.debug('video vertex added: ' + str(video))

        # find User vertex and add edge to Video vertex
        # TODO: this works but read after write seems like a bad practice
        video = self.graph.V().has('video', 'videoId', video_id)
        self.graph.V().has('user', 'userId', user_id).addE('uploaded').to(video) \
            .property('added_date', added_date).iterate()

        # TODO: find vertices for Tags and add edges from Video vertex
        #self.graph.V(video).addE("taggedWith").to(coalesce(
        #    __.V().has("tag", "name", "cassandra"),
        #    __.addV("tag").property("name", "cassandra")
        #)).iterate()


    def handle_user_rated_video(self, video_id, user_id, rating, timestamp):

        logging.debug('SuggestedVideosService:handle_user_rated_video, video id: ' + str(video_id) +
                      ', user ID: ' + str(user_id) +
                      ', rating: ' + str(rating) +
                      ', timestamp: ' + str(timestamp) +
                      ', session: ' + str(self.session) + ', graph: ' + str(self.graph))

        # TODO: implement method
        #self.graph.V().has('userId', user_id).addE('rated').to(video) \
        #    .property('rating', rating).next()

        video = self.graph.V().has('video', 'videoId', video_id)
        self.graph.V().has('user', 'userId', user_id).addE('rated').to(video) \
            .property('rating', rating).iterate()