ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN apt-get update && apt-get install -y python3 python3-pip

# Install requirements for add-on
# Системні залежності для Python, Playwright, Chromium
RUN apk add --no-cache \
    python3 \
    py3-pip \
    bash \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ttf-freefont \
    udev \
    dumb-init

# Встановлення Python-пакетів
RUN pip3 install --no-cache-dir playwright fastapi uvicorn

# Завантаження браузерів для Playwright
RUN playwright install --with-deps

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
