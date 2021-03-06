# -*- coding: utf-8 -*-

import datetime
import os
import sys
import time
from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client

from kafka import KafkaConsumer


SLEEP_TIME_IN_SECOUNDS = 1

NEWS_TABLE_NAME = "news"

SAME_NEWS_SIMILARITY_THRESHOLD = 0.9

client = KafkaConsumer(bootstrap_servers='localhost:1232','tap-news-dedupe-news-task-queue')


def handle_message(msg):
    print 1
    if msg is None or not isinstance(msg, dict) :
        return
    print 1
    task = msg
    print 1
    text = task['text']
    print
    if text is None:
        return

    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()
    same_day_news_list = list(db[NEWS_TABLE_NAME].find({'publishedAt': {'$gte': published_at_day_begin, '$lt': published_at_day_end}}))

    if same_day_news_list is not None and len(same_day_news_list) > 0:
        print 1
        documents = [news['text'] for news in same_day_news_list]
        print 1
        documents.insert(0, text)

        # Calculate similarity matrix
        print 1
        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T

        print pairwise_sim.A

        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                print "Duplicated news. Ignore."
                return

    task['publishedAt'] = parser.parse(task['publishedAt'])

    title = task['title']
    if title is not None:
        topic = news_topic_modeling_service_client.classify(title)
        task['class'] = topic

    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)
while True:
    if client is not None:
        msg = client.poll()
        if msg is not None:
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass
        time.sleep(SLEEP_TIME_IN_SECOUNDS)
