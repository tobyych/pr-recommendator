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

class ArticleEntity(NamedTuple):
  news_id: int
  entity_text: str
  rank: float

class ArticleSummary(NamedTuple):
  news_id: int
  abstractive_summary: str
  extractive_summary: str
  sentiment_score: float
