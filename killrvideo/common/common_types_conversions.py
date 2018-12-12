from uuid import UUID

import common.common_types_pb2


def UUID_to_grpc(uuid):
    return common.common_types_pb2.Uuid(value=str(uuid))


def grpc_to_UUID(uuid):
    return UUID(uuid.value)