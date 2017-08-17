import requests
import os
import random


from lxml import html

GET_CNN_NEWS_XPATH = '''//p[@class="zn-body__paragraph"]//text() | //div[@class="zn-body__paragraph"]//text()'''

USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

with open(USER_AGENTS_FILE,'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])
random.shuffle(USER_AGENTS)

def getHeaders():
    ua = random.choice(USER_AGENTS)
    headers = {
        "Connection" : "close",
        "USER_AGENTS":ua
    }
    return headers

def extract_news(new_url):
    #download http
    session_requests = requests.session()
    response = session_requests.get(new_url, headers=getHeaders())
    news = {}

    try:
        #parse html
        tree = html.fromstring(response.content)
        # Extract information
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        news = ''.join(news)
    except Exception as e:
        print
        return {}

    return news
    #extract information
