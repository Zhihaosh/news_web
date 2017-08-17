import requests
from json import loads

NEWS_API_ENDPOINT = "http://newsapi.org/v1/"
NEWS_API_KEY = "8c2680a1c20d4ed7903a7b6511579ae9"
ARTICLES_API = "articles"

CNN = 'cnn'
DEFAULT_SOURCES = [CNN]

SORT_BY_TOP = 'top'

def buildUrl(end_point=NEWS_API_ENDPOINT, api_name=ARTICLES_API):
    return end_point + api_name

def getNewsFromSource(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):
    articles = [];
    for source in sources:
        payload = {'apiKey':NEWS_API_KEY,
                    'source':source,
                    'sortBy' :sortBy
                    }
        response = requests.get(buildUrl(),params = payload)
        res_json = loads(response.content)
        if(res_json is not None and
            res_json['status'] == 'ok'and
            res_json['source'] is not None):
            for news in res_json['articles']:
                news['source'] = res_json['source']
        articles.extend(res_json['articles'])

    return articles
