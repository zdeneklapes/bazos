FROM python:3.10 as base


FROM base as builder-chromedriver

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install all packages for chromedriver: https://gist.github.com/varyonic/dea40abcf3dd891d204ef235c6e8dd79
RUN apt-get update && \
    apt-get install -y xvfb gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y

RUN apt-get install -y google-chrome-stable && \
    CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
    DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER")

RUN wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /chromedriver/chromedriver* -d /chromedriver

# make the chromedriver executable and move it to default selenium path.
RUN chmod +x /chromedriver/chromedriver
RUN mv /chromedriver/chromedriver /usr/bin/chromedriver

#RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
#RUN rm google-chrome-stable_current_amd64.deb

FROM builder-chromedriver as builder-python

RUN set -ex && \
    apt-get update &&  \
    apt-get -y install \
      cron \
      vim \
      fish \
      python3-dev \
      bat \
    --no-install-recommends && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    rm -rf /var/lib/apt/lists/* && \
    service cron start
RUN pip install -e .

FROM builder-python

# set the proxy addresses
ENV HTTP_PROXY "http://134.209.29.120:8080"
ENV HTTPS_PROXY "https://45.77.71.140:9050"

CMD ["fish"]
