# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: common/track.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'common/track.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x63ommon/track.proto\x12\x06\x63ommon\"\x9a\x01\n\x05Track\x12\x18\n\x10spotify_track_id\x18\x01 \x01(\t\x12\x12\n\ntrack_name\x18\x02 \x01(\t\x12\x0e\n\x06\x61rtist\x18\x03 \x01(\t\x12\r\n\x05genre\x18\x04 \x01(\t\x12\r\n\x05tempo\x18\x05 \x01(\x02\x12\x0e\n\x06\x65nergy\x18\x06 \x01(\x02\x12\x0f\n\x07valence\x18\x07 \x01(\x02\x12\x14\n\x0c\x64\x61nceability\x18\x08 \x01(\x02\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common.track_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TRACK']._serialized_start=31
  _globals['_TRACK']._serialized_end=185
# @@protoc_insertion_point(module_scope)
