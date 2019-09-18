from dse.cqlengine.query import LWTException
import logging
from dse.cluster import Cluster

from datetime import datetime
import hashlib
import validate_email
from .user_management_events_kafka import UserManagementPublisher

class UserModel():
    def __init__(self, user_id, first_name, last_name, email, created_date):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.created_date = created_date


class UserCredentialsModel():
    def __init__(self, email, user_id, password):
        self.email = email
        self.user_id = user_id
        self.password = password


def trim_and_hash_password(password):
    md5_hashlib = hashlib.md5()
    md5_hashlib.update(password.strip().encode('utf-8'))
    return md5_hashlib.hexdigest()


class UserManagementService(object):
    """Provides methods that implement functionality of the UserManagement Service."""
    def __init__(self, session):
        self.session = session

        self.user_management_publisher = UserManagementPublisher()

    def create_user(self, user_id, first_name, last_name, email, password):

        # validate inputs
        if not validate_email.validate_email(email):
            raise ValueError('Invalid email address')

        # trim and hash the password
        hashed_password = trim_and_hash_password(password)

        # insert into user_credentials table first so we can ensure uniqueness with LWT
        try:
            self.session.execute('INSERT INTO killrvideo.user_credentials (email, password, userid) VALUES (%s, %s, %s) IF NOT EXISTS ',
                                 (email, hashed_password, user_id))
        except LWTException:
            # Exact string in this message is expected by integration test
            raise ValueError('Exception creating user because it already exists for ' + email)

        self.session.execute('INSERT INTO killrvideo.users (userid, firstname, lastname, email, created_date) VALUES (%s, %s, %s, %s, %s)',
                             (user_id, first_name, last_name, email, datetime.utcnow()))

    def verify_credentials(self, email, password):
        # validate email is not empty or null
        if not email:
            raise ValueError('No email address provided')

        result = self.session.execute('SELECT * FROM killrvideo.user_credentials where email=%s',[email]).one()
        print(type(result))
        user_credentials = UserCredentialsModel(result['email'], result['userid'], result['password'])
        if not user_credentials:
            raise ValueError('No such user')

        # compare hashed password values
        hashed_password = trim_and_hash_password(password)
        if not (hashed_password == user_credentials.password):
            raise ValueError('Authentication error')

        return user_credentials.user_id

    def get_user_profile(self, user_ids):
        if not user_ids:
            raise ValueError('No user IDs provided')
        users = list()
        for user_id in user_ids:
            result = self.session.execute('SELECT * FROM killrvideo.users where userid = %s',[user_id]).one()
            user = UserModel(result['userid'], result['firstname'], result['lastname'], result['email'], result['created_date'])
            users.append(user)

        return users
