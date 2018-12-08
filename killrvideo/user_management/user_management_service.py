from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.query import LWTException
import hashlib
import validate_email

from user_management.user_management_service_test import test


class User(Model):
    """Model class that maps to the user table"""
    __table_name__ = 'user'
    user_id = columns.UUID(primary_key=True)
    first_name  = columns.Text()
    last_name = columns.Text()
    email = columns.Text()
    created_date = columns.Date()

class UserCredentials(Model):
    """Model class that maps to the user_credentials table"""
    __table_name__ = 'user_credentials'
    email = columns.Text(primary_key=True)
    user_id = columns.UUID()
    password  = columns.Text()

def trim_and_hash_password(password):
    return hashlib.md5().update(password.strip()).digest()

class UserManagementService(object):
    """Provides methods that implement functionality of the UserManagement Service."""

    def __init__(self, session):
        self.session = session

    def create_user(self, user_id, first_name, last_name, email, password):
        # validate inputs
        if not validate_email.validate_email(email): raise ValueError('Invalid email address')

        # trim and hash the password
        hashed_password = trim_and_hash_password(password)

        # insert into user_credentials table first so we can ensure uniqueness with LWT
        user_credentials = UserCredentials(user_id=user_id, email=email, password=hashed_password)
        try:
            user_credentials.create()
        except LWTException:
            return ValueError("User with this email already exists")

        # insert into users table
        user = User(user_id=user_id, first_name=first_name, last_name=last_name, email=email)
        user.create()


    def verify_credentials(self, email, password):
        # validate email is not empty or null
        if not email: raise ValueError('No email address provided')

        # retrieve the credentials for provided email from user_credentials table
        user_credentials = UserCredentials.get(email)
        if not user_credentials: raise ValueError('No such user')

        # compare hashed password values
        hashed_password = trim_and_hash_password(password)
        if not (hashed_password == user_credentials.password): raise ValueError('Authentication error')

        return user_credentials.user_id


    def get_user_profile(self, user_ids):
        if not user_ids: raise ValueError('No user IDs provided')
        return
        # TODO: implement
        # for user_id in user_ids:
