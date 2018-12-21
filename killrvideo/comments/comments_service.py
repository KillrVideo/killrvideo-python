from dse.cqlengine import columns
from dse.cqlengine.models import Model

class CommentsByVideoModel(Model):
    """Model class that maps to the comments_by_video table"""
    __table_name__ = 'comments_by_video'
    video_id = columns.UUID(db_field='videoid', primary_key=True)
    comment_id = columns.UUID(db_field='commentid', primary_key=True, clustering_order='DESC')
    user_id = columns.UUID(db_field='userid')
    comment = columns.Text()

class CommentsByUserModel(Model):
    """Model class that maps to the comments_by_user table"""
    __table_name__ = 'comments_by_user'
    user_id = columns.UUID(db_field='videoid', primary_key=True)
    comment_id = columns.UUID(db_field='commentid', primary_key=True, clustering_order='DESC')
    video_id = columns.UUID(db_field='userid')
    comment = columns.Text()

class CommentsService(object):
    """Provides methods that implement functionality of the Comments Service."""

    def __init__(self):
        print "here"
        return

    def comment_on_video(self, video_id, user_id, comment_id, comment): 
        CommentsByVideoModel.create(video_id=video_id, comment_id=comment_id, user_id=user_id, comment=comment)
        CommentsByUserModel.create(user_id=user_id, comment_id=comment_id, video_id=video_id, comment=comment)
        return
           

    def get_user_comments(self, user_id, page_size, starting_comment_id, paging_state):
        # TODO: implement method
        return

    def get_video_comments(self, video_id, page_size, starting_comment_id, paging_state):
        # TODO: implement method
        return

