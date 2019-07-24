import os
from kafka import KafkaProducer
from .comments_events_pb2 import UserCommentedOnVideo
from common.common_types_conversions import UUID_to_grpc, datetime_to_Timestamp, TimeUUID_to_grpc

USER_COMMENT_ADDED_TOPIC = 'topic-kv-commentCreation'

class CommentsPublisher(object):
    """Provides methods that publish events associated with the Comments Service."""

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=os.getenv('KILLRVIDEO_KAFKA', 'kafka:9092'),
                                      client_id='killrvideo-python:CommentsService')


    def publish_user_comment_added_event(self, video_id, user_id, comment_id):
        
        event = UserCommentedOnVideo(video_id=UUID_to_grpc(video_id),
                                      user_id=UUID_to_grpc(user_id),
                                      comment_id=TimeUUID_to_grpc(comment_id))

        self.producer.send(USER_COMMENT_ADDED_TOPIC, event.SerializeToString())
