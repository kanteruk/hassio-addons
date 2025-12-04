ARG BUILD_FROM
FROM ${BUILD_FROM}

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install requirements for add-on
# Системні залежності для Python, Playwright, Chromium
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    bash \
    curl \
    wget \
    gnupg \
    unzip \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    udev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Створюємо virtualenv
RUN python3 -m venv /opt/venv
# Активуємо середовище та встановлюємо пакети
RUN /opt/venv/bin/pip install --upgrade pip
RUN /opt/venv/bin/pip install playwright fastapi uvicorn
# Встановлення браузерів для Playwright
RUN /opt/venv/bin/playwright install --with-deps


# Copy data for add-on
#COPY run.sh /
#RUN chmod a+x /run.sh
#CMD [ "/run.sh" ]

# S6-Overlay
WORKDIR /root
ENTRYPOINT ["/init"]
COPY rootfs /
RUN chmod +x /etc/services.d/app/run && \
    chmod +x /etc/services.d/app/finish
