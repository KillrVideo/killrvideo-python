import logging
import os
from kafka import KafkaProducer
from .ratings_events_pb2 import UserRatedVideo
from common.common_types_conversions import UUID_to_grpc, grpc_to_UUID, datetime_to_Timestamp, Timestamp_to_datetime

USER_RATED_VIDEO_TOPIC = 'topic-kv-videoRating'

class RatingPublisher(object):
    """Provides methods that publish events associated with the Ratings Service."""

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=os.getenv('KILLRVIDEO_KAFKA', 'kafka'),
                                      client_id='killrvideo-python:RatingsService')


    def publish_user_rated_video_event(self, video_id, user_id, rating, timestamp):
        event = UserRatedVideo(video_id=UUID_to_grpc(video_id), user_id=UUID_to_grpc(user_id), rating=rating,
                               rating_timestamp=datetime_to_Timestamp(timestamp))

        serialized_event = event.SerializeToString()
        #logging.debug('(' + str(type(serialized_event)) + ') ' + str(serialized_event))

        self.producer.send(topic=USER_RATED_VIDEO_TOPIC, value=serialized_event)

