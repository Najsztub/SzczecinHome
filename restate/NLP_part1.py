# coding: utf-8
'''
MN: 30/03/16
First approach to NLP of real estate data
Based on a NLP tutorial from here:
https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-1-for-beginners-bag-of-words

'''

import pandas as pd
import codecs
import re
from .restate import clean_data

pDir = ""

# Load and clean data
df = pd.read_csv("data/items_otodom.pl_270316_8.csv")
df = clean_data(df)
df=df[df.price >50]
df=df[df.rooms <=6]
df = df[[df.columns[0], 'description', 'details', 'pow', 'price', 'floor', 'rooms', 'zabudowa']]
df.columns = ['id', 'description', 'details', 'pow', 'price', 'floor', 'rooms', 'zabudowa']

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

print df.price_class.value_counts()
# -1: overpriced

# Split data to training and model
train = df[df.id < int(df.shape[0]/1.5)]
test = df[df.id >= int(df.shape[0]/1.5)]

print train['description'][0]

# Remove punctation
# Load PL stopwords
# File from: http://www.ranks.nl/stopwords/polish

f = codecs.open(pDir + "data/stopwords_pl", encoding='utf8')

try:
	st_pl = f.readlines()

finally:
	f.close()

st_pl = [w[:-1] for w in st_pl]

print st_pl[0:10]


# Def as function
def desc_to_words(raw_text, st):
	words = raw_text.lower().split()
	stops = set(st) 
	meaningful_words = [w for w in words if not w in stops] 
	return( " ".join( meaningful_words )) 
	
# Clean in a loop
clean_desc_train = [desc_to_words(w, st_pl) for  w in train['description']]
clean_desc_test = [desc_to_words(w, st_pl) for  w in test['description']]	

# create bag of words

print clean_desc_train[0]
print "Creating the bag of words...\n"
from sklearn.feature_extraction.text import CountVectorizer

# Initialize the "CountVectorizer" object, which is scikit-learn's
# bag of words tool.  
vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000) 

# fit_transform() does two functions: First, it fits the model
# and learns the vocabulary; second, it transforms our training data
# into feature vectors. The input to fit_transform should be a list of 
# strings.
train_data_features = vectorizer.fit_transform(clean_desc_train)
test_data_features = vectorizer.transform(clean_desc_test)

# Numpy arrays are easy to work with, so convert the result to an 
# array
train_data_features = train_data_features.toarray()
test_data_features = test_data_features.toarray()
print train_data_features.shape

vocab = vectorizer.get_feature_names()
#print vocab

print "Training the random forest..."
from sklearn.ensemble import RandomForestClassifier

# Initialize a Random Forest classifier with 100 trees
forest = RandomForestClassifier(n_estimators = 100) 

# Fit the forest to the training set, using the bag of words as 
# features and the sentiment labels as the response variable
#
# This may take a few minutes to run
forest = forest.fit( train_data_features, train["price_class"] )

# Use the random forest to make sentiment label predictions
result = forest.predict(test_data_features)

# Copy the results to a pandas dataframe with an "id" column and
# a "sentiment" column
output = pd.DataFrame( data={"id":test["id"], "price":test["price_class"], "gen":result} )

output['test'] = output['gen'] == output['price']
print("Fit accuracy: {0:.2f}%").format(output['test'].mean()*100)

# Use pandas to write the comma-separated output file
output.to_csv( pDir+"data/Bag_of_Words_model.csv", index=False, quoting=3 )
