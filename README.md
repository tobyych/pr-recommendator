# PR Recommendator - A News Tracker

This GitHub repository is an attempt to build a news tracker for ABC Relations Inc. This markdown file will serve as the final report for the mini-project, and will **detail the design of the application and workflow**, together with **the explanation for the models employed** to achieve the objectives.

## Scenario

ABC Relations Inc. is a traditional Public Relation firm helping clients to protect, enhance or build their reputations through all kinds of media channels. ABC’s clients include public/private companies or public figures. Facing the big wave of digital transformation, ABC hired you as the lead engineer of digital innovation department. They would like you to help them build up a sophisticated application to solve the following problem:

## Problem

ABC Relations Inc. wants to actively track their clients’ news and react timely. However, most PR managers do not have enough time to read all news contents everyday, and because most of them are not from computing background, they would not understand too much technical details. What they want is a user-friendly tool to **notify them, tell them briefly what happened, provide background knowledge of the full story, identify key persons/companies who are relative/responsible, and ideally, PR reaction suggestions**. Meanwhile, this application should also be careful about **fake news**, **duplicate contents**, **out-of-date articles**, etc. In other words, whatever results this application provide, should always be accurate.

## PR Strategies

- Business events
- Community relations
- Corporate and social responsibility
- Crisis management
- Employee relations
- Media relations
- Social media

## Project Focus

The primary objective of this project is to build a toolset that can aid PR managers to:

1. Inspect the latest news
2. Understand news article in short period of time
3. Identify the key identities mentioned in each piece of news article

It is also of high interest for the application to be capable of suggesting PR reactions. Currently, the project focuses on a specific strategy: crisis management. There are two example situations that the application attempts to identify:

1. When a competitor launched a new product or the public sentiment has surged in a short period of time
2. When a target company has received increasing negative communication and perception

## Methodologies

To fulfil the project focuses:

1. News would be fetched from publicly available APIs
   - NewsAPI, The New York Times API
2. Text summarisation
   - Extractive summary: turn an article into a handful number of key sentences
   - Abstractive summary: end-to-end sequential model generates textual summary
3. Key entities detecion
   - Name Entity Recognition (NER): list the name entities in the article
   - Extract the top-ranked entities from text documents using TextRank algorithm
4. Sentiment scoring
   - Gives two sentiment scores on each article: an overall score and a aspect-based score
   - Use the scores to detect if there is a upsurge or downfall in sentiment

**Exact duplicate** is also checked at insertion into the database. The implementation is done by hashing the article into a numeric value and check whether there is a document with the exact same hash in the database table already. A row can only be inserted if there is no existing row with same hash in the database table.

### Details

#### Text summarisation

Extractive summarisation is powered by the pretrained BERT model. First, the document is broken down into sentences and each sentence is embedded to a vector representation using pretrained BERT model weights. Second, a k-means clustering algorithm is run through the sentence embeddings and the sentences that are closest to the cluster's centroids are returned. This method is chosen since transformer archietectures are known to perform better than encoder-decoder networks on long sequences, where sentence embeddings with better quality could be obtained.

On the other hand, for abstractive summarisation, a pretrained version of T5 (Text-to-text Transfer Transformer) [(link to original paper)](https://arxiv.org/pdf/1910.10683.pdf) is used. The main capability of this model is its ability to operate all a multitude of NLP tasks including text summarisation. It is a model that conditionally generate output based on the input, for example, if we give it an input "summarize: ...", the output would be a summary of the given text.

### Key entities detection

spaCy v2.0's Named Entity Recognition (NER) is employed to find the key entities in each article. The NER system in spaCy incorporates the use of a residual convolutional nerual network with bloom embeddings, based on transitions of the entity tags in a sequence. 1D convolutional filters are applied over the input text to predict how the upcoming words may change the current entity tags. Upcoming words may either shift (change the entity), reduce (make the entity more granular), or output the entity. The input sequence is embedded with bloom embeddings, which model the characters, prefix, suffix, and part of speech of each word. Residual blocks are used for the CNNs, and the filter sizes are chosen with beam search.

As we are interested in person or organisations instead of any possible entity, we would like to refine the key entities recognized in the above algorithm. A word-level ranking algorithm is thus useful for selecting particularly interesting entities. The algorithm used in the application is [TextRank](http://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf). It is a graph-based algorithm where the graph is constructed by looking which words follow one another. The edge weight is defined to be higher whenever two words occur more frequently next to each other in the text.

### Sentiment scoring

Each article will receive two sentiment scores, one is the overall score for the whole article, another is the aspect-based sentiment score. The overall score is given by the sentiment module in a Python library called [TextBlob](https://textblob.readthedocs.io/en/dev/). The sentiment scorer is implemented using a Naive Bayes algorithm trained on annotated movie reviews and it calculates the average polarity and subjectivity over the words in a document. The inference speed is very fast compared to deep learning models and the memory footprint is low, which makes it suitable for real-world application.

However, it is often the case that the article mentions the target company in one sentence but talks about another company for the most part of it. In this case, the sentiment score from TextBlob may not be attributed to the target company, but another entity. Therefore, it is of interest to find a query sensitive sentiment scorer. An open source GitHub project provides an API to use its pretrained model for inference. The training task is formulated as a sequence-pair classification, which is analogical to BERT's next-sentence prediction, where each example in the training data is described in the following format: "[CLS] text subtokens [SEP] aspect subtokens [SEP]". The relation between the text and aspect would then be encoded into the CLS token.

## Workflow

The workflow of the application is as follows:

1. Fetch data from public APIs to obtain news data
2. Check if there is an exact duplicate in the database. If no, insert it into database.
3. Process the news articles in the database and insert the processed output into the database.
4. Query the database to obtain interested information or build a frontend application to display the results. (To avoid displaying out-of-date articles, select news articles published within a week for example)

## Screenshots

These screenshots serve as an example how to use the application and visualise the processed data.

![overview](screenshots/overview.png?raw=true)
An overview page can be displayed as above. (Upper left) Users can start exploring from this cell, where the daily average sentiment scores for each company can be inspected. Users can identify if there is a upsurge or downfall in the average sentiment scores and for example if there is a sudden downfall in scores, users might want to click on a specific row and discover more on the reasons why the sentiment score seems to be bad for that specific company. (Right) Users can look into further details in this cell, where summaries of articles for a company in a day are displayed. Users can read the titles and the extractive summaries to quickly understand what is going on for the company in a short period of time. (Lower left) When clicked on each article on the right cell, a list of key entities would be displayed. It is ranked in descending order of importance, therefore users should focus on the top rows to see who are the key players in the events each article describes.

![entities](screenshots/entities.png?raw=true)
A close-up look on the key entities part. When an article is selected, the lower left cell will display the key entities appeared in that article. There is a rank score to show in descending order of importance.

![trend](screenshots/trend.png?raw=true)
Moreover, the output data can be used to analyse trends in the sentiments for each company. For instance, we can plot the daily sentiment across time to compare the trends of sentiments for different companies and see if there is a general trend in a particular industry, let's say. 

![wordcloud](screenshots/wordcloud.png?raw=true)
Last but not least, it is also possible to visualise each article as a word cloud, sized by the sentiment scores or the counts. This gives an visually intuitive understanding about the article, which could help users get a sense of the main idea of the article in a shorter period of time.

## Ideas that are not implemented

There are several ideas that I think are interesting to the application but not implemented yet.

- Add more data sources (may even be multilingual) and present the geographical distribution of the sentiments. This can allow PR managers to understand the dynamics across geographical locations and where to prioritise when constructing a PR strategy for a customer. Also, media coverage of different data sources can also be analysed to understand which media outlet has the greatest cost effectiveness.
- Implement deduplication for near-duplicates. MinHash algorithm with Local Sensitivity Hashing could be used as a starting point.
- Incorporate competitiors as information to the application, so that when a competitor is mentioned as a key entity in an article, it may be of higher interest for the PR manager to read.
- Survey the most interesting questions PR manager may ask when they first read an article. Form templates and use model such as BERT to perform such question answering task.
- Simplify the language used in the article, and link rare words with references in Wikipedia, so that users can understand the article better without much background knowledge.