import sqlite3
from config import config
from collections import namedtuple

BATCH_SIZE = 100

def namedtuple_factory(cursor, row):
  """Returns sqlite rows as named tuples."""
  fields = [col[0] for col in cursor.description]
  Row = namedtuple("Row", fields)
  return Row(*row)


class DB:
  def __init__(self):
    self.conn = sqlite3.connect(config['db']['filepath'])
    self.conn.row_factory = namedtuple_factory

  def query_by_batch(self, sql, params=None):
    c = self.conn.cursor()

    if params:
      c.execute(sql, params)
    else:
      c.execute(sql)
    
    while True:
      batch = c.fetchmany(BATCH_SIZE)
      if not batch:
        return
      yield batch

  def query(self, sql, params=None):
    c = self.conn.cursor()

    if params:
      c.execute(sql, params)
    else:
      c.execute(sql)
    
    rows = c.fetchall()
    return rows

  def write(self, sql, rows):
    self.conn.executemany(sql, rows)
    self.conn.commit()
  
  def close(self):
    try:
      self.conn.close()
    except Exception as e:
      print(e.with_traceback())

  @classmethod
  def init_db(cls):    
    conn = sqlite3.connect(config['db']['filepath'])
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS news (id integer primary key autoincrement, company text, title text, content text, author text, published_at text, crawled_at text, title_hash int, content_hash int)')
    c.execute('CREATE TABLE IF NOT EXISTS news_ner(news_id int, entity_text text, rank num, FOREIGN KEY(news_id) REFERENCES news(id))')
    c.execute('CREATE TABLE IF NOT EXISTS news_summary(news_id int, abstractive_summary text, extractive_summary text, sentiment_score num, ab_sentiment text, FOREIGN KEY(news_id) REFERENCES news(id))')
    conn.commit()
    conn.close()

if __name__ == '__main__':
  DB.init_db()