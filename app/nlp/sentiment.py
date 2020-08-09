from textblob import TextBlob
import aspect_based_sentiment_analysis as absa

class ABSAWrapper:
  def __init__(self):
    self.nlp = absa.load()

  def get_sentiment_score(self, text, query):
    task = self.nlp(text, aspects=[query])
    subtask = task.subtasks[query]
    return subtask.sentiment.name

class TextBlobWrapper:
  def __init__(self):
    pass

  def get_sentiment_score(self, text):
    preprocessed_text = text.replace('\n\n', '')
    blob = TextBlob(preprocessed_text)
    return blob.sentiment.polarity