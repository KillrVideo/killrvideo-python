from concurrent import futures
import time

import grpc

import user_management_service_pb2
import user_management_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class UserManagementServiceServicer(user_management_service_pb2_grpc.UserManagementServiceServicer):
    """Provides methods that implement functionality of the UserManagement Service."""

    def __init__(self):
        print "started"
        return

    def CreateUser(self, request, context):
        """Creates a new user
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def VerifyCredentials(self, request, context):
        """Verify a user's username and password
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserProfile(self, request, context):
        """Gets a user or group of user's profiles
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

# TODO: remove code for running this single service
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_management_service_pb2_grpc.add_UserManagementServiceServicer_to_server(
        UserManagementServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    # only need this temporarily until such time as we're running multiple services?
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

