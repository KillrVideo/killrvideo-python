import logging
import os
from kafka import KafkaProducer
from .video_catalog_events_pb2 import YouTubeVideoAdded
from common.common_types_conversions import UUID_to_grpc, datetime_to_Timestamp

YOUTUBE_VIDEO_ADDED_TOPIC = 'topic-kv-videoCreation'

class VideoCatalogPublisher(object):
    """Provides methods that publish events associated with the Video Catalog Service."""

    def __init__(self):
#        self.producer = KafkaProducer(bootstrap_servers=os.getenv('KILLRVIDEO_KAFKA_BOOTSTRAP_SERVERS', 'kafka'),
#                                      client_id='killrvideo-python:VideoCatalogService')
        pass

    def publish_youtube_video_added_event(self, video_id, user_id, name, description, tags, location,
                                          preview_image_location, added_date, timestamp):
#        event = YouTubeVideoAdded(video_id=UUID_to_grpc(video_id), user_id=UUID_to_grpc(user_id), name=name,
#                                  description=description, tags=tags, location=location,
#                                  preview_image_location=preview_image_location,
#                                  added_date=datetime_to_Timestamp(added_date),
#                                  timestamp=datetime_to_Timestamp(timestamp))
#
#        self.producer.send(YOUTUBE_VIDEO_ADDED_TOPIC, event.SerializeToString())
        pass
