#!/bin/sh

# Pull the latest from projects that are git subtrees
git subtree pull --prefix lib/killrvideo-service-protos git@github.com:KillrVideo/killrvideo-service-protos.git master --squash

