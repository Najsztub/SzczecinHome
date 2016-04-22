# coding: utf-8
'''
MN: 21/04/16
First approach to NLP of real estate data
Based on a NLP tutorial part2 from here:
https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-2-word-vectors

Import data from 080416 as data to fit
'''

import pandas as pd
import codecs
import re
from data.data import clean_data

# Load and clean train data
df = pd.read_csv("data/items_otodom.pl_270316_8.csv")
df = clean_data(df)
df=df[df.price >50]
df=df[df.rooms <=6]
# Load and clean train data
test = clean_data(pd.read_csv("data/items_otodom.pl_210416_12.csv"))
test=test[test.price >50]
test=test[test.rooms <=6]

# TODO Add column indicatig over- or under-pricing according to OLS model
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Leave only non-missings
df= df[ df.floor.notnull() & df.rooms.notnull()]
# Fit regression model 
result = smf.ols('price ~ pow + C(rooms) + C(floor) ', data=df).fit()

# Inspect the results
print result.summary()

# create prediction errors
df['pred_error'] = result.resid_pearson
df['price_class'] = 0 + (result.resid_pearson>.4) \
                    - (result.resid_pearson<-.4)

print "Cases identified as 0: neutral, -1: over and 1: underpriced"
print df.price_class.value_counts()

# Split data to training and model
train = df
'''
Stopped selecting the data, now we can continue with our model from example 2
'''
# Remove punctation
# Load PL stopwords
# File from: http://www.ranks.nl/stopwords/polish

f = codecs.open("data/stopwords_pl", encoding='utf8')
try:
    st_pl = f.readlines()
finally:
    f.close()

st_pl = [w[:-1] for w in st_pl]

# Define function returning words from text with optional stopwords
def desc_to_words(raw_text, st=None):
    words = raw_text.lower().split()
    if st is not None:
        stops = set(st) 
        meaningful_words = [w for w in words if not w in stops] 
        return(meaningful_words)
        #return( " ".join( meaningful_words ))
    else:
        return(words)

# Split house dscription into sentences
import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/polish.pickle')

def desc_to_sentences(desc, tokenizer, st = None):
    # Use NLTK tokenizer to split house description into sentences
    raw_sentences = tokenizer.tokenize(desc.strip().decode('utf8'))
    # Loop over sentences
    sentences = []
    for sent in raw_sentences:
        # Skip if there are no sentences
        if len(sent) > 0 :
            # Get list of words in a sentence otherwise and append
            sentences.append(desc_to_words(sent, st = st))
    return sentences

# Initialize empty sentence list
sentences = []
# Create sentences for training and test data
print "Parsing sentences from training data"
for desc in train['description']:
    sentences += desc_to_sentences(desc, tokenizer)
print "Parsing sentences from test data"
for desc in test['description']:
    sentences += desc_to_sentences(desc, tokenizer)

print "We have %d sentences in test and training data"%(len(sentences))
'''
Word2Vect model part
'''

# Import logging features
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',\
    level=logging.INFO)

# Set values for various parameters
num_features = 300    # Word vector dimensionality                      
min_word_count = 40   # Minimum word count                        
num_workers = 4       # Number of threads to run in parallel
context = 10          # Context window size
downsampling = 1e-3   # Downsample setting for frequent words

# Initialize and train the model (this will take some time)
from gensim.models import word2vec
print "Training model..."
model = word2vec.Word2Vec(sentences, workers=num_workers, \
            size=num_features, min_count = min_word_count, \
            window = context, sample = downsampling)

# If you don't plan to train the model any further, calling 
# init_sims will make the model much more memory-efficient.
model.init_sims(replace=True)

# It can be helpful to create a meaningful model name and 
# save the model for later use. You can load it later using Word2Vec.load()
model_name = "300features_40minwords_10context"
model.save(model_name)
