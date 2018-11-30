from concurrent import futures
import time

import grpc

import video_catalog_service_pb2
import video_catalog_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class VideoCatalogServiceServicer(video_catalog_service_pb2_grpc.VideoCatalogServiceServicer):
    """Provides methods that implement functionality of the VideoCatalog Service."""

    def __init__(self):
        print "started"
        return

    def SubmitUploadedVideo(self, request, context):
        """Submit an uploaded video to the catalog
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubmitYouTubeVideo(self, request, context):
        """Submit a YouTube video to the catalog
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetVideo(self, request, context):
        """Gets a video from the catalog
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetVideoPreviews(self, request, context):
        """Gets video previews for a limited number of videos from the catalog
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLatestVideoPreviews(self, request, context):
        """Gets video previews for the latest (i.e. newest) videos from the catalog
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserVideoPreviews(self, request, context):
        """Gets video previews for videos added to the site by a particular user
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

# TODO: remove code for running this single service
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    video_catalog_service_pb2_grpc.add_VideoCatalogServiceServicer_to_server(
        VideoCatalogServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    # only need this temporarily until such time as we're running multiple services?
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

