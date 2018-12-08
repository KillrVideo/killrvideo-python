from uuid import UUID

import cassandra.cqlengine
from cassandra.cluster import Cluster

from user_management.user_management_service import UserManagementService


def test():

    cluster = Cluster(['10.0.75.1'])
    session = cluster.connect("killrvideo")

    cassandra.cqlengine.connection.set_session(session)

    service = UserManagementService(session)

    new_user_id = UUID()
    new_email = "jeff@carpenter.com"
    service.create_user(user_id=new_user_id, first_name="Jeff", last_name="Carpenter", email=new_email, password="JEFF987")
    service.verify_credentials(new_user_id, "ABCDEFG") # should fail
    service.verify_credentials()

if __name__ == '__main__':
    test()