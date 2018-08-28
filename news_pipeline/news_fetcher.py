# -*- coding: utf-8 -*-

import os
import sys
from newspaper import Article  
import time
import json
from kafka import KafkaProducer
from kafka import KafkaConsumer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient



SLEEP_TIME_IN_SECOUNDS = 5

dedupe_news_queue_client = KafkaProducer(bootstrap_servers='localhost:1232', 'tap-news-dedupe-news-task-queue', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
scrape_news_queue_client = KafkaConsumer(bootstrap_servers='localhost:1231', 'tap-news-log-news-task-queue')


def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print 'message is broken'
        return
    task = msg

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text

    dedupe_news_queue_client.send(task)


while True:

    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.poll()
        if msg is not None:
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass
        time.sleep(SLEEP_TIME_IN_SECOUNDS)
