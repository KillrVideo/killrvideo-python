#!/bin/sh

# run this script from the root directory of the repo, i.e.
#   scripts/generate-grpc-stubs.sh

# helps the imports work correctly
cd lib/killrvideo-service-protos/src

python -m grpc_tools.protoc -I. --python_out=../../../killrvideo --grpc_python_out=../../../killrvideo comments/*.proto common/*.proto ratings/*.proto search/*.proto statistics/*.proto suggested-videos/*.proto uploads/*.proto user-management/*.proto video-catalog/*.proto
