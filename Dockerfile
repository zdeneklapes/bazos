FROM ubuntu:20.04
#FROM python:3.10
MAINTAINER Zdenek Lapes

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

# Update the repositories
RUN apt-get -yqq update

# Upgrade packages
RUN apt-get -yqq upgrade

# Set locale and reconfigure
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
RUN apt-get install -y locales language-pack-en tzdata
#RUN apt-get install -y locales tzdata
RUN locale-gen en_US.UTF-8
RUN dpkg-reconfigure --frontend noninteractive locales
RUN apt-get -yqq install language-pack-en

# Set timezone
ENV TZ "US/Eastern"
#RUN echo "US/Eastern" | sudo tee /etc/timezone
RUN echo "US/Eastern" | tee /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata

## Install utilities
RUN apt-get -yqq install ca-certificates curl dnsutils man openssl unzip wget

## Install xvfb and fonts
RUN apt-get -yqq install xvfb fonts-ipafont-gothic xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic

## Install Fluxbox (window manager)
RUN apt-get -yqq install fluxbox

# Install VNC
RUN apt-get -yqq install x11vnc
RUN mkdir -p ~/.vnc

# Install Supervisor
RUN apt-get -yqq install supervisor
RUN mkdir -p /var/log/supervisor

# Install Java
RUN apt-get -yqq install openjdk-11-jre-headless

# Install Selenium
RUN mkdir -p /opt/selenium
RUN wget --no-verbose -O /opt/selenium/selenium-server-standalone-2.43.1.jar http://selenium-release.storage.googleapis.com/2.43/selenium-server-standalone-2.43.1.jar
RUN ln -fs /opt/selenium/selenium-server-standalone-2.43.1.jar /opt/selenium/selenium-server-standalone.jar

# Install Chrome WebDriver
RUN wget --no-verbose -O /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/2.10/chromedriver_linux64.zip
RUN mkdir -p /opt/chromedriver-2.10
RUN unzip /tmp/chromedriver_linux64.zip -d /opt/chromedriver-2.10
RUN chmod +x /opt/chromedriver-2.10/chromedriver
RUN rm /tmp/chromedriver_linux64.zip
RUN ln -fs /opt/chromedriver-2.10/chromedriver /usr/local/bin/chromedriver

# Install Google Chrome
RUN apt-get -yqq install gnupg2
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -yqq update

RUN apt-get -yqq install google-chrome-stable
#ARG CHROME_VERSION="116.0.5845.187-1"
#RUN wget --no-verbose -O /tmp/chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
#  && apt install -y /tmp/chrome.deb \
#  && rm /tmp/chrome.deb

# Install Firefox
RUN apt-get -yqq install firefox

# Configure Supervisor
ADD ./etc/supervisor/conf.d /etc/supervisor/conf.d
#ADD ./etc/supervisord.conf /etc/supervisor/conf.d

# Configure VNC Password
RUN x11vnc -storepasswd selenium ~/.vnc/passwd

# Create a default user with sudo access
RUN useradd selenium --shell /bin/bash --create-home
RUN usermod -a -G sudo selenium
RUN echo "ALL ALL = (ALL) NOPASSWD: ALL" >> /etc/sudoers

# Default configuration
ENV SCREEN_GEOMETRY "1440x900x24"
ENV SELENIUM_PORT 4444
ENV DISPLAY :20.0

# Disable the SUID sandbox so that Chrome can launch without being in a privileged container.
# One unfortunate side effect is that `google-chrome --help` will no longer work.
RUN dpkg-divert --add --rename --divert /opt/google/chrome/google-chrome.real /opt/google/chrome/google-chrome
RUN echo "#!/bin/bash\nexec /opt/google/chrome/google-chrome.real --disable-setuid-sandbox \"\$@\"" > /opt/google/chrome/google-chrome
RUN chmod 755 /opt/google/chrome/google-chrome

RUN apt-get install -y \
    fish \
    bat \
    vim

# Install python3.10
RUN apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt install -y \
    python3-pip \
    python3-dev \
    python3.10 \
    python3.10-distutils \
    python3.10-venv \
    python3.10-dev

# PyCairo
RUN apt-get install -y \
    pkg-config \
    libcairo2-dev \
    libffi-dev

RUN ln -s /usr/bin/python3.10 /usr/local/bin/python3

# Install pip for python3.10
RUN curl https://bootstrap.pypa.io/get-pip.py | python3

COPY requirements.txt setup.py README.md make.sh /app/
COPY bazos /app/bazos

RUN pip install -r /app/requirements.txt
#RUN pip install -e /app

# Ports
EXPOSE 4444 5900

ENV DISPLAY=:99

WORKDIR /app
CMD ["fish"]
#CMD ["/app/make.sh", "entrypoint"]
