# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: uploads/uploads_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from common import common_types_pb2 as common_dot_common__types__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='uploads/uploads_service.proto',
  package='killrvideo.uploads',
  syntax='proto3',
  serialized_options=_b('\252\002\022KillrVideo.Uploads'),
  serialized_pb=_b('\n\x1duploads/uploads_service.proto\x12\x12killrvideo.uploads\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x19\x63ommon/common_types.proto\"0\n\x1bGetUploadDestinationRequest\x12\x11\n\tfile_name\x18\x01 \x01(\t\"2\n\x1cGetUploadDestinationResponse\x12\x12\n\nupload_url\x18\x01 \x01(\t\"/\n\x19MarkUploadCompleteRequest\x12\x12\n\nupload_url\x18\x01 \x01(\t\"\x1c\n\x1aMarkUploadCompleteResponse\"D\n\x17GetStatusOfVideoRequest\x12)\n\x08video_id\x18\x01 \x01(\x0b\x32\x17.killrvideo.common.Uuid\"b\n\x18GetStatusOfVideoResponse\x12/\n\x0bstatus_date\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x15\n\rcurrent_state\x18\x02 \x01(\t2\xef\x02\n\x0eUploadsService\x12y\n\x14GetUploadDestination\x12/.killrvideo.uploads.GetUploadDestinationRequest\x1a\x30.killrvideo.uploads.GetUploadDestinationResponse\x12s\n\x12MarkUploadComplete\x12-.killrvideo.uploads.MarkUploadCompleteRequest\x1a..killrvideo.uploads.MarkUploadCompleteResponse\x12m\n\x10GetStatusOfVideo\x12+.killrvideo.uploads.GetStatusOfVideoRequest\x1a,.killrvideo.uploads.GetStatusOfVideoResponseB\x15\xaa\x02\x12KillrVideo.Uploadsb\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,common_dot_common__types__pb2.DESCRIPTOR,])




_GETUPLOADDESTINATIONREQUEST = _descriptor.Descriptor(
  name='GetUploadDestinationRequest',
  full_name='killrvideo.uploads.GetUploadDestinationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_name', full_name='killrvideo.uploads.GetUploadDestinationRequest.file_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=113,
  serialized_end=161,
)


_GETUPLOADDESTINATIONRESPONSE = _descriptor.Descriptor(
  name='GetUploadDestinationResponse',
  full_name='killrvideo.uploads.GetUploadDestinationResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='upload_url', full_name='killrvideo.uploads.GetUploadDestinationResponse.upload_url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=163,
  serialized_end=213,
)


_MARKUPLOADCOMPLETEREQUEST = _descriptor.Descriptor(
  name='MarkUploadCompleteRequest',
  full_name='killrvideo.uploads.MarkUploadCompleteRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='upload_url', full_name='killrvideo.uploads.MarkUploadCompleteRequest.upload_url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=215,
  serialized_end=262,
)


_MARKUPLOADCOMPLETERESPONSE = _descriptor.Descriptor(
  name='MarkUploadCompleteResponse',
  full_name='killrvideo.uploads.MarkUploadCompleteResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=264,
  serialized_end=292,
)


_GETSTATUSOFVIDEOREQUEST = _descriptor.Descriptor(
  name='GetStatusOfVideoRequest',
  full_name='killrvideo.uploads.GetStatusOfVideoRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='video_id', full_name='killrvideo.uploads.GetStatusOfVideoRequest.video_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=294,
  serialized_end=362,
)


_GETSTATUSOFVIDEORESPONSE = _descriptor.Descriptor(
  name='GetStatusOfVideoResponse',
  full_name='killrvideo.uploads.GetStatusOfVideoResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='status_date', full_name='killrvideo.uploads.GetStatusOfVideoResponse.status_date', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='current_state', full_name='killrvideo.uploads.GetStatusOfVideoResponse.current_state', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=364,
  serialized_end=462,
)

_GETSTATUSOFVIDEOREQUEST.fields_by_name['video_id'].message_type = common_dot_common__types__pb2._UUID
_GETSTATUSOFVIDEORESPONSE.fields_by_name['status_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['GetUploadDestinationRequest'] = _GETUPLOADDESTINATIONREQUEST
DESCRIPTOR.message_types_by_name['GetUploadDestinationResponse'] = _GETUPLOADDESTINATIONRESPONSE
DESCRIPTOR.message_types_by_name['MarkUploadCompleteRequest'] = _MARKUPLOADCOMPLETEREQUEST
DESCRIPTOR.message_types_by_name['MarkUploadCompleteResponse'] = _MARKUPLOADCOMPLETERESPONSE
DESCRIPTOR.message_types_by_name['GetStatusOfVideoRequest'] = _GETSTATUSOFVIDEOREQUEST
DESCRIPTOR.message_types_by_name['GetStatusOfVideoResponse'] = _GETSTATUSOFVIDEORESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetUploadDestinationRequest = _reflection.GeneratedProtocolMessageType('GetUploadDestinationRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETUPLOADDESTINATIONREQUEST,
  __module__ = 'uploads.uploads_service_pb2'
  # @@protoc_insertion_point(class_scope:killrvideo.uploads.GetUploadDestinationRequest)
  ))
_sym_db.RegisterMessage(GetUploadDestinationRequest)

GetUploadDestinationResponse = _reflection.GeneratedProtocolMessageType('GetUploadDestinationResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETUPLOADDESTINATIONRESPONSE,
  __module__ = 'uploads.uploads_service_pb2'
  # @@protoc_insertion_point(class_scope:killrvideo.uploads.GetUploadDestinationResponse)
  ))
_sym_db.RegisterMessage(GetUploadDestinationResponse)

MarkUploadCompleteRequest = _reflection.GeneratedProtocolMessageType('MarkUploadCompleteRequest', (_message.Message,), dict(
  DESCRIPTOR = _MARKUPLOADCOMPLETEREQUEST,
  __module__ = 'uploads.uploads_service_pb2'
  # @@protoc_insertion_point(class_scope:killrvideo.uploads.MarkUploadCompleteRequest)
  ))
_sym_db.RegisterMessage(MarkUploadCompleteRequest)

MarkUploadCompleteResponse = _reflection.GeneratedProtocolMessageType('MarkUploadCompleteResponse', (_message.Message,), dict(
  DESCRIPTOR = _MARKUPLOADCOMPLETERESPONSE,
  __module__ = 'uploads.uploads_service_pb2'
  # @@protoc_insertion_point(class_scope:killrvideo.uploads.MarkUploadCompleteResponse)
  ))
_sym_db.RegisterMessage(MarkUploadCompleteResponse)

GetStatusOfVideoRequest = _reflection.GeneratedProtocolMessageType('GetStatusOfVideoRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETSTATUSOFVIDEOREQUEST,
  __module__ = 'uploads.uploads_service_pb2'
  # @@protoc_insertion_point(class_scope:killrvideo.uploads.GetStatusOfVideoRequest)
  ))
_sym_db.RegisterMessage(GetStatusOfVideoRequest)

GetStatusOfVideoResponse = _reflection.GeneratedProtocolMessageType('GetStatusOfVideoResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETSTATUSOFVIDEORESPONSE,
  __module__ = 'uploads.uploads_service_pb2'
  # @@protoc_insertion_point(class_scope:killrvideo.uploads.GetStatusOfVideoResponse)
  ))
_sym_db.RegisterMessage(GetStatusOfVideoResponse)


DESCRIPTOR._options = None

_UPLOADSSERVICE = _descriptor.ServiceDescriptor(
  name='UploadsService',
  full_name='killrvideo.uploads.UploadsService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=465,
  serialized_end=832,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetUploadDestination',
    full_name='killrvideo.uploads.UploadsService.GetUploadDestination',
    index=0,
    containing_service=None,
    input_type=_GETUPLOADDESTINATIONREQUEST,
    output_type=_GETUPLOADDESTINATIONRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='MarkUploadComplete',
    full_name='killrvideo.uploads.UploadsService.MarkUploadComplete',
    index=1,
    containing_service=None,
    input_type=_MARKUPLOADCOMPLETEREQUEST,
    output_type=_MARKUPLOADCOMPLETERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetStatusOfVideo',
    full_name='killrvideo.uploads.UploadsService.GetStatusOfVideo',
    index=2,
    containing_service=None,
    input_type=_GETSTATUSOFVIDEOREQUEST,
    output_type=_GETSTATUSOFVIDEORESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_UPLOADSSERVICE)

DESCRIPTOR.services_by_name['UploadsService'] = _UPLOADSSERVICE

# @@protoc_insertion_point(module_scope)
