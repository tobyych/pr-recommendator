from db import DB
from config import config
from api._newsapi import NewsAPIWrapper

TARGETS = ['facebook', 'apple', 'google', 'tesla', 'huawei']

def article_generator(api_client, target):
  for article in api_client.article_generator(query=target):

    rows = db.query('SELECT count(1) FROM news WHERE content_hash=:hash', {'hash': hash(article.content)})
    count = rows[0][0]
    if count == 0:
      yield article

if __name__ == '__main__':
  db = DB()
  wrapper = NewsAPIWrapper()
  for target in TARGETS:
    db.write('INSERT INTO news VALUES (?, ?, ?, ?, ?, ?, ?, ?)', article_generator(wrapper, target))
  db.close()


