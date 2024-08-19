#!/bin/bash

set -e
set -o pipefail

if [ $# -lt 2 ]
then 
    echo "Usage: read_yaml_config.sh <PATH_TO_YAML> <YOUR_COMMAND>"
    exit 1
fi

# Installing yq if it isn't
if [ ! -f /usr/bin/yq ]; then
    echo "Installing yq..."
    wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64.tar.gz -O - | tar xz && mv yq_linux_amd64 /usr/bin/yq
    echo "yq installed !"
fi

CONFIG=$(yq -o=shell '.' $1)

# This will set some variables based on the data in the yaml
for c in ${CONFIG[@]}; do eval export $c; done

# This will set a variable containing the number of plugins
export plugin_count=$(yq '.plugins | length' $1)
export ohif_modes_count=$(yq '.ohif_modes | length' $1)
export ohif_extensions_count=$(yq '.ohif_extensions | length' $1)

echo "Executing ${@:2}"

${@:2}
