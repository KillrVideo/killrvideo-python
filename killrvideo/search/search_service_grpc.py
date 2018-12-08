import grpc

import search_service_pb2
import search_service_pb2_grpc

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
        # TODO: implement service call
        #result = self.search_service.search_videos(request.query, request.page_size, request.paging_state)
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetQuerySuggestions(self, request, context):
        """Gets the current rating stats for a video
        """
        print ">>> SearchService:GetQuerySuggestions: "
        print request
        # TODO: implement service call
        #result = self.search_service.get_query_suggestions(request.query, request.page_size)
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

