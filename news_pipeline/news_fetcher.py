# -*- coding: utf-8 -*-

import os
import sys
from newspaper import Article  

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://kbsylnro:aePMEklD0z0mTmoDivBy3S00yA9GGzKC@donkey.rmq.cloudamqp.com/kbsylnro"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://jkqxpdhr:AVmZ8yaiOODH1CJqJTlA8EIpPq_d83GF@donkey.rmq.cloudamqp.com/jkqxpdhr"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECOUNDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)


def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print 'message is broken'
        return
    task = msg

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text

    dedupe_news_queue_client.sendMessage(task)


while True:

    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECOUNDS)
