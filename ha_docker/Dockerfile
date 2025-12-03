ARG BUILD_FROM
FROM $BUILD_FROM
#ARG BUILD_FROM=ubuntu:22.04
#FROM $BUILD_FROM

RUN apt-get update && apt-get install -y python3 python3-pip

# Install requirements for add-on
RUN \
    apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
