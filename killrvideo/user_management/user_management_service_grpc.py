import logging
from common.common_types_conversions import UUID_to_grpc, grpc_to_UUID
from user_management_service_pb2 import CreateUserResponse, VerifyCredentialsResponse, GetUserProfileResponse, \
    UserProfile
from user_management_events_pb2 import UserCreated
import user_management_service_pb2_grpc


def UserModel_to_UserProfile(user):
    return UserProfile(user_id=UUID_to_grpc(user.user_id),first_name=user.first_name,last_name=user.last_name,
                       email=user.email)

def UserModelList_to_GetUserProfileResponse(users):
    response = GetUserProfileResponse()
    if isinstance(users, (list,)):    # most preferred way to check if it's list
        response.profiles.extend(map(UserModel_to_UserProfile, users))
    elif users is not None: # single result
        response.profiles.extend([UserModel_to_UserProfile(users)])
    return response

class UserManagementServiceServicer(user_management_service_pb2_grpc.UserManagementServiceServicer):
    """Provides methods that implement functionality of the UserManagement Service."""

    def __init__(self, grpc_server, user_management_service):
        logging.debug("UserManagementServiceServicer started")
        self.user_management_service = user_management_service
        user_management_service_pb2_grpc.add_UserManagementServiceServicer_to_server(self, grpc_server)

    def CreateUser(self, request, context):
        """Creates a new user
        """
        logging.debug(">>> UserManagementService:CreateUser: ")
        logging.debug(request)
        user_id = grpc_to_UUID(request.user_id)

        self.user_management_service.create_user(user_id=user_id,
                                                 first_name=request.first_name,last_name=request.last_name,
                                                 email=request.email,password=request.password)
        # TODO: Publish UserCreated event
        #event = UserCreated(user_id=request.user_id, first_name=request.first_name, last_name=request.last_name,
        #                    email=request.email)

        return CreateUserResponse()

    def VerifyCredentials(self, request, context):
        """Verify a user's username and password
        """
        logging.debug(">>> UserManagementService:VerifyCredentials: ")
        logging.debug(request)
        result = self.user_management_service.verify_credentials(request.email, request.password)
        if result:
            return VerifyCredentialsResponse(user_id=UUID_to_grpc(result))
        else:
            return VerifyCredentialsResponse()

    def GetUserProfile(self, request, context):
        """Gets a user or group of user's profiles
        """
        logging.debug(">>> UserManagementService:GetUserProfile: ")
        logging.debug(request)
        result = self.user_management_service.get_user_profile(map(grpc_to_UUID,request.user_ids))
        logging.debug(result)
        return UserModelList_to_GetUserProfileResponse(result)


