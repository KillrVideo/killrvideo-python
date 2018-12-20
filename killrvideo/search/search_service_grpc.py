from search_service_pb2 import SearchVideosResponse, GetQuerySuggestionsResponse, SearchResultsVideoPreview
import search_service_pb2_grpc
from common.common_types_conversions import UUID_to_grpc, grpc_to_UUID, datetime_to_Timestamp

def Video_to_SearchResultsVideoPreview(video):
    return SearchResultsVideoPreview(video_id=UUID_to_grpc(video.video_id),
                                 added_date=datetime_to_Timestamp(video.added_date),
                                 name=video.name, preview_image_location=video.preview_image_location,
                                 user_id=UUID_to_grpc(video.user_id))


def VideoList_to_SearchVideosResponse(video_list):
    response = SearchVideosResponse(query=video_list.query, paging_state=video_list.paging_state)
    if isinstance(video_list.videos, (list,)):    # most preferred way to check if it's list
        response.videos.extend(map(Video_to_SearchResultsVideoPreview, video_list.videos))
    elif video_list.videos is not None: # single result
        response.videos.extend([Video_to_SearchResultsVideoPreview(video_list.videos)])
    return response


def Suggestions_to_GetQuerySuggestionsResponse(suggestions):
    response = GetQuerySuggestionsResponse()
    if isinstance(suggestions, (list,)):    # most preferred way to check if it's list
        response.suggestions.extend(suggestions)
    elif suggestions is not None: # single result
        response.suggestions.extend([suggestions])
    return response


class SearchServiceServicer(search_service_pb2_grpc.SearchServiceServicer):
    """Provides methods that implement functionality of the Search Service."""

    def __init__(self, grpc_server, search_service):
        print "SearchServiceServicer started"
        self.search_service = search_service
        search_service_pb2_grpc.add_SearchServiceServicer_to_server(self, grpc_server)


    def SearchVideos(self, request, context):
        """Searches for videos by a given query term
        """
        print ">>> SearchService:SearchVideos: "
        print request
        result = self.search_service.search_videos(request.query, request.page_size, request.paging_state)
        return VideoList_to_SearchVideosResponse(result)


    def GetQuerySuggestions(self, request, context):
        """Gets the current rating stats for a video
        """
        print ">>> SearchService:GetQuerySuggestions: "
        print request
        result = self.search_service.get_query_suggestions(request.query, request.page_size)
        return Suggestions_to_GetQuerySuggestionsResponse(result)

