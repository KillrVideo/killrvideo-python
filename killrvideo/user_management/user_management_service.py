from dse.cqlengine import columns
from dse.cqlengine.models import Model
from dse.cqlengine.query import LWTException
import hashlib
import validate_email


class UserModel(Model):
    """Model class that maps to the user table"""
    __table_name__ = 'users'
    user_id = columns.UUID(db_field='userid', primary_key=True)
    first_name = columns.Text(db_field='firstname')
    last_name = columns.Text(db_field='lastname')
    email = columns.Text()
    created_date = columns.Date()


class UserCredentialsModel(Model):
    """Model class that maps to the user_credentials table"""
    __table_name__ = 'user_credentials'
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(db_field='userid')
    password = columns.Text()


def trim_and_hash_password(password):
    md5_hashlib = hashlib.md5()
    md5_hashlib.update(password.strip())
    return md5_hashlib.hexdigest()


class UserManagementService(object):
    """Provides methods that implement functionality of the UserManagement Service."""

    def __init__(self):
        return

    def create_user(self, user_id, first_name, last_name, email, password):
        # validate inputs
        if not validate_email.validate_email(email):
            raise ValueError('Invalid email address')

        # trim and hash the password
        hashed_password = trim_and_hash_password(password)

        # insert into user_credentials table first so we can ensure uniqueness with LWT
        try:
            UserCredentialsModel.if_not_exists().create(user_id=user_id, email=email, password=hashed_password)
        except LWTException:
            # Exact string in this message is expected by integration test
            raise ValueError('Exception creating user because it already exists for ' + email)

        # insert into users table
        UserModel.create(user_id=user_id, first_name=first_name, last_name=last_name, email=email)

    def verify_credentials(self, email, password):
        # validate email is not empty or null
        if not email:
            raise ValueError('No email address provided')

        # retrieve the credentials for provided email from user_credentials table
        user_credentials = UserCredentialsModel.get(email=email)
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

        # see: https://datastax.github.io/python-driver/cqlengine/queryset.html#retrieving-objects-with-filters
        # filter().all() returns a ModelQuerySet, we iterate over the query set to get the Model instances
        user_results = UserModel.filter(user_id__in=user_ids).all()
        users = list()
        for user in user_results:
            users.append(user)
        return users
