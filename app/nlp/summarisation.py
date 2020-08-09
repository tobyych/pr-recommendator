import torch
import json 
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
from summarizer import Summarizer

def get_abstractive_summary(text):
  # abstractive summarizer based on T5 in huggingface's library

  model = T5ForConditionalGeneration.from_pretrained('t5-small')
  tokenizer = T5Tokenizer.from_pretrained('t5-small')
  device = torch.device('cpu')

  preprocess_text = text.strip().replace("\n", "")
  t5_prepared_Text = "summarize: " + preprocess_text
  tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)

  # summmarize 
  summary_ids = model.generate(tokenized_text,
                                num_beams=4,
                                no_repeat_ngram_size=2,
                                min_length=30,
                                max_length=100,
                                early_stopping=True)

  output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

  return output

def get_extractive_summary(text):
  # extractive summarizer based on BERT
  model = Summarizer()
  return model(text, num_sentences=3)