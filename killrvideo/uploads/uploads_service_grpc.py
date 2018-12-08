import grpc

import uploads_service_pb2
import uploads_service_pb2_grpc

class UploadsServiceServicer(uploads_service_pb2_grpc.UploadsServiceServicer):
    """Provides methods that implement functionality of the Uploads Service."""

    def __init__(self, grpc_server, uploads_service):
        print "UploadsServiceServicer started"
        self.uploads_service = uploads_service
        uploads_service_pb2_grpc.add_UploadsServiceServicer_to_server(self, grpc_server)

    def GetUploadDestination(self, request, context):
        """Gets an upload destination for a user to upload a video
        """
        print ">>> UploadsService:GetUploadDestination: "
        print request
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MarkUploadComplete(self, request, context):
        """Marks an upload as complete
        """
        print ">>> UploadsService:MarkUploadComplete: "
        print request
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStatusOfVideo(self, request, context):
        """Gets the status of an uploaded video
        """
        print ">>> UploadsService:GetStatusOfVideo: "
        print request
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')



