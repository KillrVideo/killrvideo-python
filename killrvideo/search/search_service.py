import logging
import re
from sortedcontainers import SortedSet
from dse.cqlengine import columns
from dse.cqlengine.models import Model
from nltk.corpus import stopwords


class SearchVideo():
    def __init__(self, user_id, added_date, video_id, name, preview_image_location):
        self.user_id = user_id
        self.added_date = added_date
        self.video_id = video_id
        self.name = name
        self.preview_image_location = preview_image_location

class SearchVideoResults():
    def __init__(self, query, paging_state, videos):
        self.query = query
        self.paging_state = paging_state
        self.videos = videos

class TagsByLetterModel(Model):
    """Model class that maps to the tags_by_letter table"""
    __table_name__ = 'tags_by_letter'
    first_letter = columns.Text(primary_key=True)
    tag = columns.Text(primary_key=True)

class SearchService(object):
    """Provides methods that implement functionality of the Search Service."""

    def __init__(self, session):
        self.session = session

        # Prepared statements for search_videos() and get_query_suggestions()
        self.search_videos_prepared = \
            session.prepare('SELECT * FROM videos WHERE solr_query = ?')

        self.get_query_suggestions_prepared = \
            session.prepare('SELECT name, tags, description FROM videos WHERE solr_query = ?')

        self.stop_words = set(stopwords.words('english'))

    def search_videos(self, query, page_size, paging_state):
        if not query:
            raise ValueError('No query string provided')
        if page_size <= 0:
            raise ValueError('Page size should be strictly positive for video search')

        results = list()
        next_page_state = ''

        # https://docs.datastax.com/en/dse/6.0/cql/cql/cql_using/search_index/cursorsDeepPaging.html
        solr_query = '{"q":"name:(' + query + ')^4 OR tags:(' + query + ')^2 OR description:(' + query + ')", "paging":"driver"}'

        bound_statement = self.search_videos_prepared.bind([solr_query])
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
            logging.debug('next search video is: ' + video_row['name'])
            results.append(SearchVideo(user_id=video_row['userid'], added_date=video_row['added_date'],
                                       video_id=video_row['videoid'], name=video_row['name'],
                                       preview_image_location=video_row['preview_image_location']))

            # ensure we don't continue asking and pull another page
            remaining -= 1
            if (remaining == 0):
                break

        if len(results) == page_size:
            # Use hex encoding since paging state is raw bytes that won't encode to UTF-8
            next_page_state = result_set.paging_state.encode('hex')

        return SearchVideoResults(query=query, paging_state=next_page_state, videos=results)

    def get_query_suggestions(self, query, page_size):
        if not query:
            raise ValueError('No query string provided')
        if page_size <= 0:
            raise ValueError('Page size should be strictly positive for search suggestions')

        results = list()
        next_page_state = ''

        solr_query = '{"q":"name:(' + query + '*) OR tags:(' + query + '*) OR description:(' + query + '*)", "paging":"driver"}'

        bound_statement = self.get_query_suggestions_prepared.bind([solr_query])

        # TODO: not sure we're interpreting page size correctly here.
        #  Should it be a limit on our database query, or a limit on the number of terms returned?
        bound_statement.fetch_size = page_size

        result_set = self.session.execute(bound_statement)

        # deliberately avoiding paging in background
        current_rows = result_set.current_rows

        remaining = len(current_rows)

        suggestions = SortedSet()
        pattern = re.compile(r'\b' + re.escape(query) + r'[a-z]*\b')

        for video_row in current_rows:
            logging.debug('next video used for suggestions is: ' + video_row['name'])

            for name_term in re.findall(pattern, video_row['name']):
                logging.debug('Name term: ' + name_term)
                suggestions.add(name_term)
            for tag in video_row['tags']:
                for tag_term in re.findall(pattern, tag):
                    logging.debug('Tag term: ' + tag_term)
                    suggestions.add(tag_term)
            for desc_term in re.findall(pattern, video_row['description']):
                logging.debug('Description term: ' + desc_term)
                suggestions.add(desc_term)

            # ensure we don't continue asking and pull another page
            remaining -= 1
            if (remaining == 0):
                break

        # remove stop words
        suggestions.difference_update(self.stop_words)

        return list(suggestions)

