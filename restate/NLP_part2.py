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
test = data_clean(pd.read_csv("data/items_otodom.pl_080416_10.csv"))
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
df['price_class'] = 0 + (result.resid_pearson>.4) - (result.resid_pearson<-.4)

print "Cases identified as 0: neutral, -1: over and 1: underpriced"
print df.price_class.value_counts()

# Split data to training and model
train = df
'''
Stopped selecting the data, now we can continue with our model from example 2
'''
