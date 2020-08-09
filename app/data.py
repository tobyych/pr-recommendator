import pandas as pd

class LocalFileDataGenerator:
  def __init__(self, filepath):
    self.filepath = filepath
    self.df = pd.read_csv('./1974_3493_bundle_archive/articles1.csv', index_col=0)

  def content_generator(self)
    for _, row in self.df.iterrows():
      yield row['content']