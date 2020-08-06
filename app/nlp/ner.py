import spacy

nlp = spacy.load('en_core_web_sm')

doc = nlp(articles[0]['content'])

for token in doc:
  print(token.text, token.pos, token.tag, token.dep)

for ent in doc.ents:
  print(ent.text, ent.start_char, ent.end_char, ent.label_)