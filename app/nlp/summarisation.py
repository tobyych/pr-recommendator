import torch
import json 
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
from summarizer import Summarizer

class T5AbstractiveSummariser:
  def __init__(self):
    self.model = T5ForConditionalGeneration.from_pretrained('t5-small')
    self.tokenizer = T5Tokenizer.from_pretrained('t5-small')
    self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

  def get_abstractive_summary(self, text):
    preprocess_text = text.strip().replace("\n", "")
    t5_prepared_Text = "summarize: " + preprocess_text
    tokenized_text = self.tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(self.device)

    # summmarize 
    summary_ids = self.model.generate(tokenized_text,
                                  num_beams=4,
                                  no_repeat_ngram_size=2,
                                  min_length=30,
                                  max_length=100,
                                  early_stopping=True)

    output = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return output

class BERTExtractiveSummariser:
  def __init__(self):
    self.model = Summarizer()

  def get_extractive_summary(self, text):
    # extractive summarizer based on BERT
    return self.model(text, num_sentences=3)