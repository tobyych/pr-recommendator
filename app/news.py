from db import DB
from config import config
from api._newsapi import NewsAPIWrapper
from api.nytimes import NYTimesAPIWrapper
from nlp.ner import get_name_entities
from nlp.sentiment import get_sentiment_score
from nlp.summarisation import get_abstractive_summary, get_extractive_summary
from schema.article import ArticleEntity, ArticleSummary

TARGETS = ['facebook', 'apple', 'google', 'tesla', 'huawei']

def article_generator(api_client, target):
  for article in api_client.article_generator(query=target):
    rows = db.query('SELECT count(1) cnt FROM news WHERE content_hash=:hash', {'hash': hash(article.content)})
    count = rows[0][0]
    if count == 0:
      yield article

def crawl_data_to_db(db, wrapper):
  for target in TARGETS:
    db.write('INSERT INTO news (company, title, content, author, published_at, crawled_at, title_hash, content_hash) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', article_generator(wrapper, target))

def summary_generator(batch):
  for row in batch:
    yield ArticleSummary(
      row.id,
      get_abstractive_summary(row.content),
      get_extractive_summary(row.content),
      get_sentiment_score(row.content)
    )

def entity_generator(batch):
  for row in batch:
    for entity in get_name_entities(row.content):
      yield ArticleEntity(
        row.id,
        entity[0],
        entity[1]
      )

def process(db):
  rows = db.query('SELECT max(news_id) max_id FROM news_summary')
  last_processed_id = rows[0][0]
  start_id = last_processed_id if last_processed_id is not None else 0
  sql = 'SELECT * FROM news WHERE id > :id'
  for batch in db.query_by_batch(sql, {'id': start_id}):
    db.write('INSERT INTO news_ner (news_id, entity_text, rank) VALUES (?, ?, ?)', entity_generator(batch))
    db.write('INSERT INTO news_summary (news_id, abstractive_summary, extractive_summary, sentiment_score) VALUES (?, ?, ?, ?)', summary_generator(batch))



if __name__ == '__main__':
  wrapper = NYTimesAPIWrapper()
  db = DB()
  # crawl_data_to_db(db, wrapper)
  process(db)
  db.close()