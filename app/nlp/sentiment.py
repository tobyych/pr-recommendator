from textblob import TextBlob

def get_sentiment_score(text):
  preprocessed_text = text.replace('\n\n', '')
  blob = TextBlob(preprocessed_text)
  return blob.sentiment.polarity