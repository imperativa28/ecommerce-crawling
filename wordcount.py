import pandas as pd
from spacy.lang.id import Indonesian
from collections import Counter

df = pd.read_csv('tokopedia.csv', header=0, sep=';', index_col=0)
description = list(df['description'])
stopwords = open('stopwords.txt', 'r').read().splitlines()

nlp = Indonesian()

docs = []
for i, doc in enumerate(description):
    print('Processing doc: {}'.format(i))
    docs.append(nlp(str(doc)))

tokens_list = [[token.lemma_.lower() for token in doc if not token.is_punct and not token.is_space and token.lemma_ not in stopwords]
          for doc in docs]
tokens_flat = [token for tokens in tokens_list for token in tokens]
result = list(Counter(tokens_flat).items())

result_df = pd.DataFrame(result, columns=['word', 'frequencies'])
result_df.to_csv('word_counts.csv')
print(result_df)
