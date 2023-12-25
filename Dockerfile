FROM python:3.10 as base
MAINTAINER Zdenek Lapes

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Update the repositories
RUN apt-get -yqq update && apt-get -yqq upgrade

# install all packages for chromedriver: https://gist.github.com/varyonic/dea40abcf3dd891d204ef235c6e8dd79
RUN set -ex && \
    apt-get install -y \
    xvfb \
    gnupg \
    wget \
    curl \
    unzip \
    cron \
    vim \
    fish \
    python3-dev \
    bat \
    --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y

#    ca-certificates \
#    dnsutils \
#    man \
#    openssl \
#    xvfb \
#    fonts-ipafont-gothic \
#    xfonts-100dpi \
#    xfonts-75dpi \
#    xfonts-scalable \
#    xfonts-cyrillic \
#    fluxbox \

ARG CHROME_VERSION="116.0.5845.187-1"
RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
  && apt install -y /tmp/chrome.deb \
  && rm /tmp/chrome.deb

#ENV DISPLAY=:99

COPY requirements.txt setup.py README.md /app/
COPY bazos /app/bazos

WORKDIR /app
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /app/requirements.txt

RUN set -ex && \
    pip install -e /app

# Add user
# RUN useradd -ms /bin/bash user1 && echo 'user1:user1' | chpasswd
# USER user1

CMD ["fish"]
