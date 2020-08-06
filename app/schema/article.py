from typing import NamedTuple

class Article(NamedTuple):
  company: str
  title: str
  content: str
  author: str
  published_at: str
  crawled_at: str
  title_hash: int
  content_hash: int
