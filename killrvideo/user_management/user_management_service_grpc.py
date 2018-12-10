from common.common_types_conversions import uuid_to_grpc,grpc_to_uuid
from user_management_service_pb2 import CreateUserResponse, VerifyCredentialsResponse, GetUserProfileResponse, \
    UserProfile
import user_management_service_pb2_grpc


def user_to_user_profile(user):
    return UserProfile(user_id=uuid_to_grpc(user.user_id), first_name=user.first_name, last_name=user.last_name,
                       email=user.email)

def users_to_user_profile_response(users):
    response = GetUserProfileResponse()

    if isinstance(users,(list,)):    # most preferred way to check if it's list
        for user in users:
            response.profiles.extend([user_to_user_profile(user)])
    elif users is not None: # single result
        response.profiles.extend([user_to_user_profile(users)])

    return response

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
        self.user_management_service.create_user(user_id=grpc_to_uuid(request.user_id),
                                                 first_name=request.first_name,last_name=request.last_name,
                                                 email=request.email,password=request.password)
        return CreateUserResponse()

    def VerifyCredentials(self, request, context):
        """Verify a user's username and password
        """
        print ">>> UserManagementService:VerifyCredentials: "
        print request
        result = self.user_management_service.verify_credentials(request.email, request.password)
        if result:
            return VerifyCredentialsResponse(user_id=uuid_to_grpc(result))
        else:
            return VerifyCredentialsResponse()

    def GetUserProfile(self, request, context):
        """Gets a user or group of user's profiles
        """
        print ">>> UserManagementService:GetUserProfile: "
        print request
        result = self.user_management_service.get_user_profile(map(grpc_to_uuid,request.user_ids))
        print result
        return users_to_user_profile_response(result)


