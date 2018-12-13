from uuid import UUID
from google.protobuf.timestamp_pb2 import Timestamp
import common.common_types_pb2


def UUID_to_grpc(uuid):
    return common.common_types_pb2.Uuid(value=str(uuid))


def grpc_to_UUID(uuid):
    return UUID(uuid.value)

def datetime_to_Timestamp(datetime):
    timestamp = Timestamp()
    timestamp.FromDatetime(datetime)
    return timestamp