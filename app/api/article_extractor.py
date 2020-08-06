from newspaper import Article

def get_full_text(url):
  a = Article(url)
  a.download()
  a.parse()
  return a.text