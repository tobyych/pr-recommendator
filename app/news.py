from config import config
import os
os.environ['PYTHONHASHSEED'] = 0

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

def summary_generator(batch, abs_sum, ex_sum, tb_wrapper, absa_wrapper):
  for row in batch:
    yield ArticleSummary(
      row.id,
      abs_sum.get_abstractive_summary(row.content),
      ex_sum.get_extractive_summary(row.content),
      tb_wrapper.get_sentiment_score(row.content),
      absa_wrapper.get_sentiment_score(row.content[:511], row.company)
    )

def entity_generator(batch, ner_wrapper):
  for row in batch:
    for entity in ner_wrapper.get_name_entities(row.content):
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

  ex_sum = BERTExtractiveSummariser()
  abs_sum = T5AbstractiveSummariser()
  tb_wrapper = TextBlobWrapper()
  absa_wrapper = ABSAWrapper()
  ner_wrapper = RankedNameEntityWrapper()

  for batch in db.query_by_batch(sql, {'id': start_id}):
    db.write('INSERT INTO news_ner (news_id, entity_text, rank) VALUES (?, ?, ?)', entity_generator(batch, ner_wrapper))
    db.write('INSERT INTO news_summary (news_id, abstractive_summary, extractive_summary, sentiment_score, ab_sentiment) VALUES (?, ?, ?, ?, ?)', summary_generator(batch, abs_sum, ex_sum, tb_wrapper, absa_wrapper))


if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description='PR Recommendator - a news tracking application')
  parser.add_argument('--init', dest='init',
                      action='store_true', default=False,
                      help='create tables in SQLite DB')
  parser.add_argument('--crawl', dest='crawl',
                      action='store_true', default=False,
                      help='crawl news articles from public APIs')
  parser.add_argument('--process', dest='process',
                      action='store_true', default=False,
                      help='process the news articles inside DB')
  args = parser.parse_args()

  from db import DB
  from schema.article import ArticleEntity, ArticleSummary

  if args.init:
    DB.init_db()
    exit()
  
  from api._newsapi import NewsAPIWrapper
  from api.nytimes import NYTimesAPIWrapper

  if args.crawl:
    wrapper = NYTimesAPIWrapper()
    db = DB()
    crawl_data_to_db(db, wrapper)
    db.close()
    exit()

  import warnings
  warnings.filterwarnings("ignore")

  from nlp.ner import RankedNameEntityWrapper
  from nlp.sentiment import TextBlobWrapper, ABSAWrapper
  from nlp.summarisation import BERTExtractiveSummariser, T5AbstractiveSummariser

  if args.process:
    db = DB()
    process(db)
    db.close()