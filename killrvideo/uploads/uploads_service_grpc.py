from concurrent import futures
import time

import grpc
import etcd

import uploads_service_pb2
import uploads_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class UploadsServiceServicer(uploads_service_pb2_grpc.UploadsServiceServicer):
    """Provides methods that implement functionality of the Uploads Service."""

    def __init__(self):
        print "UploadsServiceServicer started"
        return

    def GetUploadDestination(self, request, context):
        """Gets an upload destination for a user to upload a video
        """
        print ">>> UploadsService:GetUploadDestination: "
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MarkUploadComplete(self, request, context):
        """Marks an upload as complete
        """
        print ">>> UploadsService:MarkUploadComplete: "
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStatusOfVideo(self, request, context):
        """Gets the status of an uploaded video
        """
        print ">>> UploadsService:GetStatusOfVideo: "
        print request
        # TODO: implement service call
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def init(server):
    uploads_service_pb2_grpc.add_UploadsServiceServicer_to_server(
        UploadsServiceServicer(), server)

# TODO: remove code for running this single service
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    init(server)
    server.add_insecure_port('[::]:8899')
    server.start()

    # TODO: Fix hardcoded values
    etcd_client = etcd.Client(host='10.0.75.1', port=2379)
    etcd_client.write('/killrvideo/services/UploadsService/killrvideo-python', "10.0.75.1:8899")

    # only need this temporarily until such time as we're running multiple services?
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()

