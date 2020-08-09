from configparser import ConfigParser
from datetime import datetime, timedelta

from api.article_extractor import get_full_text
from newsapi import NewsApiClient
from schema.article import Article


class NewsAPIWrapper:
  def __init__(self):
    config = ConfigParser()
    config.read('../config.ini')

    self.api_client = NewsApiClient(api_key=config['newsapi']['API_KEY'])

  def article_generator(self, query):
    response = self.api_client.get_everything(q=query,
                                             sources='bbc-news,the-verge',
                                             domains='bbc.co.uk,techcrunch.com',
                                             from_param=(datetime.now() - timedelta(3)).strftime('%Y-%m-%d'),
                                             language='en',
                                             sort_by='popularity',
                                             page_size=100,
                                             page=1)
    articles = response['articles']
    for article in articles:
      published_at = article['publishedAt'][:10] + ' ' + article['publishedAt'][11:19]
      title = article['title']
      content = get_full_text(article['url'])
      yield Article(
        query,
        title,
        content,
        article['author'],
        published_at,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        hash(title),
        hash(content),
      )

if __name__ == '__main__':
  wrapper = NewsAPIWrapper()
  for i in wrapper.article_generator('apple'):
    print(i)
    break