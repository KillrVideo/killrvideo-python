from concurrent import futures
from uuid import UUID
import time

import grpc
import etcd
import common.common_types_pb2

from user_management_service import UserManagementService
from user_management_service_pb2 import VerifyCredentialsResponse, GetUserProfileResponse
import user_management_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

def uuid_to_grpc(uuid):
    return common.common_types_pb2.Uuid(str(uuid))

def grpc_to_uuid(uuid):
    return UUID(uuid.value)

def user_to_user_profile_response(user):
    return GetUserProfileResponse(uuid_to_grpc(user.user_id), user.first_name, user.last_name, user.email)

class UserManagementServiceServicer(user_management_service_pb2_grpc.UserManagementServiceServicer):
    """Provides methods that implement functionality of the UserManagement Service."""

    def __init__(self, grpc_server, user_management_service):
        print "UserManagementServiceServicer started"
        self.user_management_service = user_management_service
        user_management_service_pb2_grpc.add_UserManagementServiceServicer_to_server(self, grpc_server)

    def CreateUser(self, request, context):
        """Creates a new user
        """
        print ">>> UserManagementService:CreateUser: "
        print request
        self.user_management_service.create_user(UUID(request.user_id.value), request.first_name, request.last_name, request.email, request.password)

    def VerifyCredentials(self, request, context):
        """Verify a user's username and password
        """
        print ">>> UserManagementService:VerifyCredentials: "
        print request
        # TODO: implement service call
        result = self.user_management_service.verify_credentials(request.email, request.password)
        if result: return VerifyCredentialsResponse(uuid_to_grpc(result))
        else: return VerifyCredentialsResponse()

    def GetUserProfile(self, request, context):
        """Gets a user or group of user's profiles
        """
        print ">>> UserManagementService:GetUserProfile: "
        print request
        # TODO: implement service call
        result = self.user_management_service.get_user_profile(map(grpc_to_uuid(), request.user_ids))
        return GetUserProfileResponse(profiles=map(user_to_user_profile_response(), result))


