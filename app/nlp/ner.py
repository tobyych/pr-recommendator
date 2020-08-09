import spacy
import pytextrank

class RankedNameEntityWrapper:
  def __init__(self):
    self.nlp = spacy.load('en_core_web_lg')
    tr = pytextrank.TextRank()
    self.nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

  def get_name_entities(self, text):
    doc = self.nlp(text)
    interested_entities = []
    for p in doc.ents:
      if p.label_ in ['PERSON', 'ORG']:
        interested_entities.append(p.text.lower())
    for p in doc._.phrases:
      if p.text in interested_entities:
        yield (p.text, p.rank)