# -*- coding: utf-8 -*-

import datetime
import os
import sys
import redis
import hashlib
from kafka import KafkaProducer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

NEWS_TIME_OUT_IN_SECONDS = 3600 * 24
SLEEP_TIME_IN_SECOUNDS = 10

NEWS_SOURCES = [
    'ars-technica',
    'associated-press',
    'bbc-news',
    'bbc-sport',
    'bild',
    'bloomberg',
    'cnn',
    'engadget',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]
producer = KafkaProducer(bootstrap_servers='localhost:1231', 'tap-news-scrape-news-task-queue', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)

while True:
    news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)
    num_of_new_news = 0
    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if redis_client.get(news_digest) is None:
            num_of_new_news += 1
            news['digest'] = news_digest
            #format: YYYY-MM-DDTHH:MM:SS in UTC
            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            redis_client.set(news_digest, news)
            redis_client.expire(news_digest,NEWS_TIME_OUT_IN_SECONDS)
            producer.send(news)
    print "Fetched %d new news." % num_of_new_news

    time.sleep(SLEEP_TIME_IN_SECOUNDS)
