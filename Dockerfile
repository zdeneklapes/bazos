FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT 8000
ENV EDITOR vim
EXPOSE 8000

WORKDIR /app
COPY . /app/

#RUN curl -LO https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
#RUN rm google-chrome-stable_current_amd64.deb

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


RUN chmod +x /app/main.sh
CMD ["fish"]


