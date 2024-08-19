# NOTE : using bullseye to have an up-to-date python version
# The official image is using buster which has python 3.7
FROM debian:bullseye-slim AS orthanc

WORKDIR /root/

# COPIED AND MODIFIED from the official image
ADD ./orthanc/scripts/setup-locales.sh ./setup-locales.sh
RUN bash ./setup-locales.sh

ARG ORTHANC_VERSION=latest
ADD ./orthanc/scripts/download-orthanc.sh ./download-orthanc.sh
RUN bash ./download-orthanc.sh ${ORTHANC_VERSION}

ADD ./orthanc/scripts/create-config.sh ./create-config.sh
RUN bash ./create-config.sh

RUN rm ./setup-locales.sh ./download-orthanc.sh ./create-config.sh

VOLUME [ "/var/lib/orthanc/db" ]
EXPOSE 4242
EXPOSE 8042

ENTRYPOINT [ "Orthanc" ]
CMD [ "/etc/orthanc/" ]

# https://groups.google.com/d/msg/orthanc-users/qWqxpvCPv8g/Z8huoA5FDAAJ
ENV MALLOC_ARENA_MAX 5

FROM orthanc AS orthanc-awesomme

RUN apt update && apt install -y gettext && rm -rf /var/lib/apt/lists/*

# Copy scripts to install dependencies
COPY ./scripts/with_yaml_config.sh ./with_yaml_config.sh
COPY ./orthanc/scripts/install_python.sh ./install_python.sh
COPY ./orthanc/scripts/install_plugins.sh ./install_plugins.sh
RUN chmod u+x ./with_yaml_config.sh ./install_plugins.sh ./install_python.sh

# Install Python
RUN ./install_python.sh

# Copy Orthanc plugin config files
ARG CONFIGFILE=./orthanc_config.yml
COPY ${CONFIGFILE} ./orthanc.config

# Install Orthanc plugins
RUN ./with_yaml_config.sh ./orthanc.config ./install_plugins.sh

# Clean installation scripts
RUN rm ./install_python.sh ./install_plugins.sh ./with_yaml_config.sh ./orthanc.config

# Set environment variables to replace in configuration file
#ARG ORTHANC_ROOT_URI=/orthanc_external
ARG OHIF_ROOT_URI=/ohif
ARG DEPLOYMENT_HOST=localhost
#ENV ORTHANC_ROOT_URI=${ORTHANC_ROOT_URI}
ENV OHIF_ROOT_URI=${OHIF_ROOT_URI}
ENV DEPLOYMENT_HOST=${DEPLOYMENT_HOST}

# Copy Orthanc configuration file and fill with env
# This isn't really necessary, Orthanc would have filled env variables
# https://orthanc.uclouvain.be/book/users/configuration.html
ARG ORTHANC_CONFIG=./orthanc/Configuration.json
COPY ${ORTHANC_CONFIG} /tmp/orthanc.json.tmpl
RUN envsubst < "/tmp/orthanc.json.tmpl" > "/etc/orthanc/orthanc.json"

FROM orthanc-awesomme AS orthanc-girder

RUN python3.9 -m pip install girder-client cryptography
