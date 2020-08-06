import sqlite3
from config import config

class DB:
  def __init__(self):
    self.conn = sqlite3.connect(config['db']['filepath'])

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
    config = ConfigParser()
    config.read('./config.ini')
    
    conn = sqlite3.connect(config['db']['filepath'])
    c = conn.cursor()
    c.execute('CREATE TABLE news (company text, title text, content text, author text, published_at text, crawled_at text, title_hash int, content_hash int)')
    conn.commit()
    conn.close()

if __name__ == '__main__':
  DB.init_db()