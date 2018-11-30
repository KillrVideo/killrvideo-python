from concurrent import futures
import time

import grpc

import uploads_service_pb2
import uploads_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class UploadsServiceServicer(uploads_service_pb2_grpc.UploadsServiceServicer):
    """Provides methods that implement functionality of the Uploads Service."""

    def __init__(self):
        print "started"
        return

    def GetUploadDestination(self, request, context):
        """Gets an upload destination for a user to upload a video
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MarkUploadComplete(self, request, context):
        """Marks an upload as complete
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStatusOfVideo(self, request, context):
        """Gets the status of an uploaded video
        """
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

# TODO: remove code for running this single service
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    uploads_service_pb2_grpc.add_UploadsServiceServicer_to_server(
        UploadsServiceServicer(), server)
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

