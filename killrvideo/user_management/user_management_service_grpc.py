from concurrent import futures
import time

import grpc
import etcd

import user_management_service_pb2
import user_management_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class UserManagementServiceServicer(user_management_service_pb2_grpc.UserManagementServiceServicer):
    """Provides methods that implement functionality of the UserManagement Service."""

    def __init__(self):
        print "UserManagementServiceServicer started"
        return

    def CreateUser(self, request, context):
        """Creates a new user
        """
        print ">>> UserManagementService:CreateUser: "
        print request
        # TODO: implement service call
        #context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        #context.set_details('Method not implemented!')
        #raise NotImplementedError('Method not implemented!')

    def VerifyCredentials(self, request, context):
        """Verify a user's username and password
        """
        print ">>> UserManagementService:VerifyCredentials: "
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserProfile(self, request, context):
        """Gets a user or group of user's profiles
        """
        print ">>> UserManagementService:GetUserProfile: "
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def init(server):
    user_management_service_pb2_grpc.add_UserManagementServiceServicer_to_server(
        UserManagementServiceServicer(), server)

# TODO: remove code for running this single service
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    init(server)
    server.add_insecure_port('[::]:8899')
    server.start()

    # TODO: Fix hardcoded values
    etcd_client = etcd.Client(host='10.0.75.1', port=2379)
    etcd_client.write('/killrvideo/services/UserManagementService/killrvideo-python', "10.0.75.1:8899")

    # only need this temporarily until such time as we're running multiple services?
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

