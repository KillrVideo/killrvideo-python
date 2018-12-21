from dse.cqlengine import columns
from dse.cqlengine.models import Model
from dse.cqlengine.query import BatchQuery

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
    user_id = columns.UUID(db_field='userid', primary_key=True)
    comment_id = columns.UUID(db_field='commentid', primary_key=True, clustering_order='DESC')
    video_id = columns.UUID(db_field='videoid')
    comment = columns.Text()


class GetUserComments():
   def __init__(self, paging_state, comments):
       self.paging_state = paging_state
       self.comments = comments

class CommentsService(object):
    """Provides methods that implement functionality of the Comments Service."""

    def __init__(self, session):
        self.session = session

        # Prepared statements for get_user_comments()
        self.userComments_startingPointPrepared = \
            session.prepare('SELECT * FROM comments_by_user WHERE userid = ? AND (commentid) <= (?)')
        self.userComments_noStartingPointPrepared = \
            session.prepare('SELECT * FROM comments_by_user WHERE userid = ?')

        # Prepared statements for get_video_comments()
        self.videoComments_startingPointPrepared = \
            session.prepare('SELECT * FROM comments_by_video WHERE videoid = ? AND (commentid) <= (?)')
        self.videoComments_noStartingPointPrepared = \
            session.prepare('SELECT * FROM comments_by_video WHERE videoid = ?')


    def comment_on_video(self, video_id, user_id, comment_id, comment):
        #Checking values have been provided 
        if not video_id:
            raise ValueError('video_id should be provided to submit a comment')
        elif not user_id:
            raise ValueError('user_id should be provided to submit a comment')
        elif not comment_id:
            raise ValueError('comment_id should be provided to submit a comment')
        elif not comment:
            raise ValueError('comment should be provided to submit a comment')

        #Needs to insert into both tables to be successful
        batch_query = BatchQuery() 
        CommentsByVideoModel.batch(batch_query).create(video_id=video_id, comment_id=comment_id, user_id=user_id, comment=comment)
        CommentsByUserModel.batch(batch_query).create(user_id=user_id, comment_id=comment_id, video_id=video_id, comment=comment)
        batch_query.execute()
        return
           

    def get_user_comments(self, user_id, page_size, starting_comment_id, paging_state):
        if page_size <= 0:
            raise ValueError('Page size should be strictly positive for get user preview video request')
        
        results = list()
        next_page_state = ''

        bound_statement = None

        if starting_comment_id:
            bound_statement = self.userComments_startingPointPrepared.bind([user_id,
                                                                                starting_comment_id])
        else:
            bound_statement = self.userComments_noStartingPointPrepared.bind([user_id])

        print 'Current query is: ' + str(bound_statement)

        bound_statement.fetch_size = page_size
        result_set = None
        
        if paging_state:
            # see below where we encode paging state to hex before returning
            result_set = self.session.execute(bound_statement, paging_state=paging_state.decode('hex'))
        else:
            result_set = self.session.execute(bound_statement)

        # deliberately avoiding paging in background
        current_rows = result_set.current_rows

        remaining = len(current_rows)

        for comment_row in current_rows:
            print 'next user comment is: ' + comment_row['comment']
            results.append(CommentsByUserModel(user_id=comment_row['userid'],
                                           comment_id=comment_row['commentid'], video_id=comment_row['videoid'],
                                           comment=comment_row['comment']))

            # ensure we don't continue asking and pull another page
            remaining -= 1
            if (remaining == 0):
                break

        if len(results) == page_size:
            # Use hex encoding since paging state is raw bytes that won't encode to UTF-8
            next_page_state = result_set.paging_state.encode('hex')

        return GetUserComments(paging_state=next_page_state, comments=results)





        return

    def get_video_comments(self, video_id, page_size, starting_comment_id, paging_state):
        # TODO: implement method
        return

