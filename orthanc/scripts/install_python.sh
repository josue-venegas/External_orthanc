#!/bin/bash

set -e
set -o pipefail

DEBIAN_FRONTEND=noninteractive apt-get -y clean
DEBIAN_FRONTEND=noninteractive apt-get update
DEBIAN_FRONTEND=noninteractive apt-get -y install python3.9 libpython3.9 python3-tk python3.9-distutils 
DEBIAN_FRONTEND=noninteractive apt-get clean

# Pip and Tkinter don't come out of the box apparently, so we have to install them manually
wget https://bootstrap.pypa.io/get-pip.py && python3.9 get-pip.py --user
rm get-pip.py

rm -rf /var/lib/apt/lists/*