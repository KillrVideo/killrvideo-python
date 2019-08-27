import logging
import os
from kafka import KafkaProducer
from .user_management_events_pb2 import UserCreated
from common.common_types_conversions import UUID_to_grpc, datetime_to_Timestamp

USER_CREATED_TOPIC = 'topic-kv-userCreation'

class UserManagementPublisher(object):
    """Provides methods that publish events associated with the User Management Service."""

    def __init__(self):
        # self.producer = KafkaProducer(bootstrap_servers='10.0.75.1:9092',
        #                               client_id='killrvideo-python:UserManagementService')



    def publish_user_created_event(self, user_id, first_name, last_name, email, timestamp):
        # event = UserCreated(user_id=UUID_to_grpc(user_id), first_name=first_name, last_name=last_name, email=email,
        #                           timestamp=datetime_to_Timestamp(timestamp))
        #
        # self.producer.send(USER_CREATED_TOPIC, event.SerializeToString())