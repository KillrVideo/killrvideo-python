import logging
import os
import threading
from kafka import KafkaConsumer
from user_management.user_management_events_pb2 import UserCreated
from video_catalog.video_catalog_events_pb2 import YouTubeVideoAdded
from ratings.ratings_events_pb2 import UserRatedVideo
from common.common_types_conversions import grpc_to_UUID, Timestamp_to_datetime

USER_CREATED_TOPIC = 'topic-kv-userCreation'
USER_RATED_VIDEO_TOPIC = 'topic-kv-videoRating'
YOUTUBE_VIDEO_ADDED_TOPIC = 'topic-kv-videoCreation'

class SuggestedVideoKafkaConsumer(threading.Thread):
    def __init__(self, suggested_videos_consumer):
        threading.Thread.__init__(self)
        self.suggested_videos_consumer = suggested_videos_consumer

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers=os.getenv('KILLRVIDEO_KAFKA_BOOTSTRAP_SERVERS', 'kafka'),
                                 client_id='killrvideo-python:SuggestedVideosService',
                                 fetch_max_wait_ms=10000) # poll every 10 seconds for new events

        consumer.subscribe([USER_CREATED_TOPIC, USER_RATED_VIDEO_TOPIC, YOUTUBE_VIDEO_ADDED_TOPIC])

        for event in consumer:
            logging.debug(event)
            try:
                if event.topic == USER_CREATED_TOPIC:
                    self.suggested_videos_consumer.process_user_created(event.value)
                elif event.topic == USER_RATED_VIDEO_TOPIC:
                    self.suggested_videos_consumer.process_user_rated_video(event.value)
                elif event.topic == YOUTUBE_VIDEO_ADDED_TOPIC:
                    self.suggested_videos_consumer.process_youtube_video_added(event.value)
            except Exception as e:
                logging.debug("Error processing event: " + str(e))


class SuggestedVideosConsumer(object):
    """Provides methods that consume events needed by the Suggested Videos Service."""

    def __init__(self, suggested_videos_service):
        self.suggested_videos_service = suggested_videos_service
        self.consumer = SuggestedVideoKafkaConsumer(self)
        self.consumer.start()

    def process_user_created(self, value):
        user_created = UserCreated()
        user_created.ParseFromString(value)
        logging.debug(">>> SuggestedVideosService:HandleUserCreated: ")
        logging.debug(user_created)
        self.suggested_videos_service.handle_user_created(user_id=grpc_to_UUID(user_created.user_id),
                                                          first_name=user_created.first_name,
                                                          last_name=user_created.last_name,
                                                          email=user_created.email,
                                                          timestamp=Timestamp_to_datetime(user_created.timestamp))

    def process_user_rated_video(self, value):
        user_rated_video = UserRatedVideo()
        user_rated_video.ParseFromString(value)
        logging.debug(">>> SuggestedVideosService:HandleUserRatedVideo: ")
        logging.debug(user_rated_video)
        self.suggested_videos_service.handle_user_rated_video(video_id=grpc_to_UUID(user_rated_video.video_id),
                                                              user_id=grpc_to_UUID(user_rated_video.user_id),
                                                              rating=user_rated_video.rating,
                                                              timestamp=Timestamp_to_datetime(user_rated_video.rating_timestamp))

    def process_youtube_video_added(self, value):
        video_added = YouTubeVideoAdded()
        video_added.ParseFromString(value)
        logging.debug(">>> SuggestedVideosService:HandleVideoAdded: ")
        logging.debug(video_added)
        self.suggested_videos_service.handle_youtube_video_added(video_id=grpc_to_UUID(video_added.video_id),
                                                                 user_id=grpc_to_UUID(video_added.user_id),
                                                                 name=video_added.name,
                                                                 description=video_added.description,
                                                                 location=video_added.location,
                                                                 preview_image_location=video_added.preview_image_location,
                                                                 tags=video_added.tags,
                                                                 added_date=Timestamp_to_datetime(video_added.added_date),
                                                                 timestamp=Timestamp_to_datetime(video_added.timestamp))
