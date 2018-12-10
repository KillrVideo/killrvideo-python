from uuid import UUID

import common.common_types_pb2


def uuid_to_grpc(uuid):
    return common.common_types_pb2.Uuid(value=str(uuid))


def grpc_to_uuid(uuid):
    return UUID(uuid.value)