#!/bin/bash

set -e
set -o pipefail

if [ $# -lt 2 ]
then 
    echo "Usage: with_secrets.sh <SECRET_FILE> <YOUR_COMMAND>"
    exit 1
fi

while IFS= read -ra c || [ -n "$c" ]; do eval export $c; done < $1

${@:2}