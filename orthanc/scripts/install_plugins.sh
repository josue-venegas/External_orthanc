#!/bin/bash

set -e
set -o pipefail

URL=https://orthanc.uclouvain.be/downloads/linux-standard-base

install_plugin () {
    PLUGIN=$1
    VERSION=$2

    echo "Installing $PLUGIN $VERSION..."

    PLUGIN_NAME=$(echo $1 | sed 's/-\([a-z0-9]\)/\u\1/g')
    PLUGIN_NAME=${PLUGIN_NAME^}

    FILENAME="lib$PLUGIN_NAME.so"
    [ $# -ge 3 ] && FILENAME=$3

    wget ${URL}/${PLUGIN}/${VERSION}/${FILENAME}

    mkdir -p /usr/local/share/orthanc/plugins
    mv ./$FILENAME /usr/local/share/orthanc/plugins/

    echo "$PLUGIN $VERSION installed !"
}

echo "$plugin_count plugins to install"

for ((i = 0; i < $plugin_count; i++)); do
    eval "install_plugin \$plugins_${i}_name \$plugins_${i}_version \$plugins_${i}_filename"
done
