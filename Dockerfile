#FROM debian:stable
ARG BUILD_FROM=ubuntu:22.04
FROM $BUILD_FROM

RUN apt-get update && apt-get install -y python3 python3-pip

# Install basics
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy run script
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD ["/run.sh"]
