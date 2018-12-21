import logging
from datetime import datetime, timedelta
from dse.cqlengine import columns
from dse.cqlengine.models import Model
from dse.cqlengine.query import BatchQuery

YOUTUBE = 0
UPLOAD = 1
NUM_DAYS_FOR_PAGING = 7

class VideosModel(Model):
    """Model class that maps to the videos table"""
    __table_name__ = 'videos'
    video_id = columns.UUID(primary_key=True, db_field='videoid')
    user_id = columns.UUID(db_field='userid')
    name = columns.Text()
    description  = columns.Text()
    location = columns.Text()
    location_type = columns.Integer()
    preview_image_location = columns.Text()
    tags = columns.Set(columns.Text)
    added_date = columns.DateTime()

class LatestVideosModel(Model):
    """Model class that maps to the latest_videos table"""
    __table_name__ = 'latest_videos'
    yyyymmdd = columns.Text(primary_key=True)
    added_date = columns.DateTime(primary_key=True, clustering_order='DESC')
    video_id = columns.UUID(primary_key=True, clustering_order='ASC', db_field='videoid')
    user_id = columns.UUID(db_field='userid')
    name  = columns.Text()
    preview_image_location = columns.Text()

class UserVideosModel(Model):
    """Model class that maps to the user_videos table"""
    __table_name__ = 'user_videos'
    user_id = columns.UUID(primary_key=True, db_field='userid')
    added_date = columns.DateTime(primary_key=True, clustering_order='DESC')
    video_id = columns.UUID(primary_key=True, clustering_order='ASC', db_field='videoid')
    name = columns.Text()
    preview_image_location = columns.Text()

class LatestVideoPreviews():
    def __init__(self, paging_state, videos):
        self.paging_state = paging_state
        self.videos = videos

class UserVideoPreviews():
    def __init__(self, paging_state, videos):
        self.paging_state = paging_state
        self.videos = videos

class CustomPagingState():
    def __init__(self, buckets, current_bucket, cassandra_paging_state):
        self.buckets = buckets
        self.current_bucket = current_bucket
        self.cassandra_paging_state = cassandra_paging_state


def parse_custom_paging_state(paging_state):

    if not paging_state:
        return build_first_custom_paging_state()

    portions = paging_state.split(',')
    buckets = portions[0].split('_')
    current_bucket = int(portions[1])
    cassandra_paging_state = portions[2]

    return CustomPagingState(buckets=buckets, current_bucket=current_bucket,
                             cassandra_paging_state=cassandra_paging_state)


def create_custom_paging_state(buckets, bucket_index, cassandra_paging_state):

    # create a list of strings, then join them at the end for the final string
    strings = list()
    num_buckets = len(buckets)
    bucket_counter = 0

    # Build the buckets part of the string, i.e.:
    # yyyyMMdd_yyyyMMdd_yyyyMMdd_yyyyMMdd_yyyyMMdd_yyyyMMdd_yyyyMMdd_yyyyMMdd
    for bucket in buckets:
        strings.append(bucket)
        bucket_counter += 1
        # include separator unless last item
        if bucket_counter < num_buckets:
            strings.append('_')

    strings.append(',')
    strings.append(str(bucket_index))
    strings.append(',')
    strings.append(cassandra_paging_state)

    return ''.join(strings)


# Build the first paging state if one does not already exist and return an object containing 3 elements
# representing the initial state
def build_first_custom_paging_state():

    # formulate the time-based values
    buckets = list()
    date = datetime.utcnow()

    for bucket_num in range(0, NUM_DAYS_FOR_PAGING):
        buckets.append(date.strftime('%Y%m%d'))
        date = date - timedelta(days=1)

    return CustomPagingState(buckets=buckets, current_bucket=0, cassandra_paging_state='')


class VideoCatalogService(object):
    """Provides methods that implement functionality of the Video Catalog Service."""

    def __init__(self, session):
        self.session = session

        # Prepared statements for GetLatestVideoPreviews()
        self.latestVideoPreview_startingPointPrepared = \
            session.prepare('SELECT * FROM latest_videos WHERE yyyymmdd = ? AND (added_date, videoid) <= (?, ?)')
        self.latestVideoPreview_noStartingPointPrepared = \
            session.prepare('SELECT * FROM latest_videos WHERE yyyymmdd = ?')

        # Prepared statements for GetUserVideoPreviews()
        self.userVideoPreview_startingPointPrepared = \
            session.prepare('SELECT * FROM user_videos WHERE userid = ? AND (added_date, videoid) <= (?, ?)')
        self.userVideoPreview_noStartingPointPrepared = \
            session.prepare('SELECT * FROM user_videos WHERE userid = ?')


    def submit_youtube_video(self, video_id, user_id, name, description, tags, you_tube_video_id):
        # validate inputs
        if not video_id:
            raise ValueError('video_id should be provided for submit youtube video request')
        elif not user_id:
            raise ValueError('user_id should be provided for submit youtube video request')
        elif not name:
            raise ValueError('video name should be provided for submit youtube video request')
        elif not description:
            raise ValueError('video description should be provided for submit youtube video request')
        elif not you_tube_video_id:
            raise ValueError('video YouTube id should be provided for submit youtube video request')

        # Formulate the preview location
        preview_image_location = '//img.youtube.com/vi/' + you_tube_video_id + '/hqdefault.jpg'


    # formulate the time-based values
        now = datetime.utcnow()
        yyyymmdd = now.strftime('%Y%m%d')

        # create and execute batch statement to insert into multiple tables
        batch_query = BatchQuery()
        VideosModel.batch(batch_query).create(video_id=video_id, user_id=user_id, name=name, description=description,
                                              location=you_tube_video_id, location_type=YOUTUBE,
                                              preview_image_location=preview_image_location, tags=tags,
                                              added_date=now)
        LatestVideosModel.batch(batch_query).create(yyyymmdd=yyyymmdd, added_date=now, video_id=video_id,
                                                    user_id=user_id, name=name,
                                                    preview_image_location=preview_image_location)
        UserVideosModel.batch(batch_query).create(user_id=user_id, added_date=now, video_id=video_id,
                                                  name=name, preview_image_location=preview_image_location)
        batch_query.execute()


    def get_video(self, video_id):
        if not video_id:
            raise ValueError('No Video ID provided')

        return VideosModel.get(video_id=video_id)


    def get_video_previews(self, video_ids):
        if not video_ids:
            raise ValueError('No Video IDs provided')

        # see: https://datastax.github.io/python-driver/cqlengine/queryset.html#retrieving-objects-with-filters
        # filter().all() returns a ModelQuerySet, we iterate over the query set to get the Model instances
        video_results = VideosModel.filter(video_id__in=video_ids).all()
        videos = list()
        for video in video_results:
            videos.append(video)
        return videos


    def get_latest_video_previews(self, page_size, starting_added_date, starting_video_id, paging_state):
        if page_size <= 0:
            raise ValueError('Page size should be strictly positive for get latest preview video request')

        logging.debug('Page size is: ' + str(page_size) + ', starting date is: ' + str(starting_added_date) + \
              ', starting video ID is: ' + str(starting_video_id))

        custom_paging_state = parse_custom_paging_state(paging_state)

        results = list()
        next_page_state = ''

        buckets = custom_paging_state.buckets
        bucket_index = custom_paging_state.current_bucket
        # see below where we encode paging state to hex before returning
        cassandra_paging_state = custom_paging_state.cassandra_paging_state.decode('hex')

        logging.debug('Custom paging state is: buckets: ' + str(len(buckets)) + ' bucket index: ' + str(bucket_index) + \
              ' cassandra paging state: ' + cassandra_paging_state)

        while bucket_index < len(buckets):

            records_still_needed = page_size - len(results)

            logging.debug('records_still_needed is: ' + str(records_still_needed) + ' page_size is: ' + str(page_size) + \
                  ' results.size is: ' + str(len(results)))

            yyyymmdd = buckets[bucket_index]

            bound_statement = None

            if starting_added_date and starting_video_id:
                bound_statement = self.latestVideoPreview_startingPointPrepared.bind([yyyymmdd, starting_added_date,
                                                                                      starting_video_id])
            else:
                bound_statement = self.latestVideoPreview_noStartingPointPrepared.bind([yyyymmdd])

            logging.debug('Current query is: ' + str(bound_statement))

            bound_statement.fetch_size = records_still_needed
            logging.debug('FETCH SIZE is: ' + str(bound_statement.fetch_size) + ' added_date is: ' + yyyymmdd)

            result_set = None

            if cassandra_paging_state:
                result_set = self.session.execute(bound_statement, paging_state=cassandra_paging_state)
                cassandra_paging_state = None # clear paging state once used
            else:
                result_set = self.session.execute(bound_statement)

            # deliberately avoiding paging in background
            current_rows = result_set.current_rows

            remaining = len(current_rows)

            for video_row in current_rows:
                logging.debug('latest video is: ' + video_row['name'])
                # Add each row to results
                results.append(LatestVideosModel(yyyymmdd=video_row['yyyymmdd'], added_date=video_row['added_date'],
                               video_id=video_row['videoid'], user_id=video_row['userid'], name=video_row['name'],
                               preview_image_location=video_row['preview_image_location']))

                # ensure we don't continue asking and pull another page
                remaining -= 1
                if (remaining == 0):
                    break

            logging.debug('results size is: ' + str(len(results)) + ' request.getPageSize() is : ' + str(page_size))
            if len(results) == page_size:
                # Use hex encoding since paging state is raw bytes that won't encode to UTF-8
                next_cassandra_paging_state = result_set.paging_state.encode('hex')

                if next_cassandra_paging_state:
                    logging.debug('results size == page size')
                    # Start from where we left off in this bucket if we get the next page
                    next_page_state = create_custom_paging_state(buckets, bucket_index, next_cassandra_paging_state)
                    break

                # Start from the beginning of the next bucket since we're out of rows in this one
                elif bucket_index == len(buckets) - 1:
                    logging.debug('bucket_index == len(buckets) - 1)')
                    next_page_state = create_custom_paging_state(buckets, bucket_index + 1, '')

                logging.debug('buckets: ' + str(len(buckets)) + ' index: ' + str(bucket_index) + ' state: ' + \
                      next_page_state + ' results size: ' + str(len(results)) + ' page size: ' + str(page_size))

            bucket_index += 1

        return LatestVideoPreviews(paging_state=next_page_state, videos=results)


    def get_user_video_previews(self, user_id, page_size, starting_added_date, starting_video_id, paging_state):
        if page_size <= 0:
            raise ValueError('Page size should be strictly positive for get user preview video request')

        results = list()
        next_page_state = ''

        bound_statement = None

        # If starting_added_date and starting_video_id are provided, we do NOT use the paging state
        if starting_added_date and starting_video_id:
            bound_statement = self.userVideoPreview_startingPointPrepared.bind([user_id, starting_added_date,
                                                                                starting_video_id])
        else:
            bound_statement = self.userVideoPreview_noStartingPointPrepared.bind([user_id])

        logging.debug('Current query is: ' + str(bound_statement))

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

        for video_row in current_rows:
            logging.debug('next user video is: ' + video_row['name'])
            results.append(UserVideosModel(user_id=video_row['userid'], added_date=video_row['added_date'],
                                           video_id=video_row['videoid'], name=video_row['name'],
                                           preview_image_location=video_row['preview_image_location']))

            # ensure we don't continue asking and pull another page
            remaining -= 1
            if (remaining == 0):
                break

        if len(results) == page_size:
            # Use hex encoding since paging state is raw bytes that won't encode to UTF-8
            next_page_state = result_set.paging_state.encode('hex')

        return UserVideoPreviews(paging_state=next_page_state, videos=results)





