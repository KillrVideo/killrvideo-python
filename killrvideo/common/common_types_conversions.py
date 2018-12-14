from uuid import UUID
from google.protobuf.timestamp_pb2 import Timestamp
import common.common_types_pb2
from datetime import datetime

def UUID_to_grpc(uuid):
    return common.common_types_pb2.Uuid(value=str(uuid))


def grpc_to_UUID(uuid):
    return UUID(uuid.value)

def datetime_to_Timestamp(dt):
    timestamp = Timestamp()
    timestamp.FromDatetime(dt)
    return timestamp

def Timestamp_to_datetime(timestamp):
    dt = datetime.fromtimestamp(timestamp.seconds)