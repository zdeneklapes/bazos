FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT 8000
ENV EDITOR vim
EXPOSE 8000

WORKDIR /app
COPY requirements.txt main.sh /app/
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

RUN chmod +x /app/main.sh
CMD ["fish"]
