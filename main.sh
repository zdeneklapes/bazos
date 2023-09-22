#!/bin/bash
#set -x # log

RM="rm -rfd"
RED='\033[0;31m'
NC='\033[0m'
GREEN='\033[0;32m'
DEBUG=1

source ./scripts/docker.sh
source ./scripts/python.sh
source ./scripts/release.sh
source ./scripts/utils.sh
