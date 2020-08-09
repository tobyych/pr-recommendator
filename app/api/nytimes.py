import requests
import json
from api.article_extractor import get_full_text
from configparser import ConfigParser
from datetime import datetime, timedelta
from schema.article import Article

class NYTimesAPIWrapper:
  def __init__(self):
    config = ConfigParser()
    config.read('../config.ini')
    self.api_key = config['nytimesapi']['API_KEY']
    self.search_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={}&page={}&begin_date={}&api-key={}'


  def article_generator(self, query):
    for i in range(1, 101):
      url = self.search_url.format(
        query,
        i,
        (datetime.now() - timedelta(7)).strftime('%Y%m%d'),
        self.api_key
      )
      
      res = requests.get(url)
      if res.status_code == 200:
        articles = res.json()['response']['docs']
        if len(articles) == 0:
          return
        for article in articles:
          published_at = article['pub_date'][:10] + ' ' + article['pub_date'][11:19]
          title = article['headline']['main']
          content = get_full_text(article['web_url'])
          yield Article(
            query,
            title,
            content,
            article['byline']['original'],
            published_at,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            hash(title),
            hash(content),
          )


if __name__ == '__main__':
  wrapper = NYTimesAPIWrapper()
  for i in wrapper.article_generator('apple'):
    print(i)
    break