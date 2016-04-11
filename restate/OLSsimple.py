# -*- coding: utf-8 -*-
'''
MN: 11/04/16
Simple OLS anaysis
'''
import pandas as pd
import restate
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Load data
print "Load data"
df = pd.read_csv("data/items_otodom.pl_080416_10.csv", encoding = 'utf-8')
print "Clean data"
df = restate.clean_data(df)
# leave only interesting observaions
df=df[df.price >50]
df=df[df.price<600]
df=df[df['pow'] <250]
df = df[df.rooms<=5]
    
# Leave only non-missings
df= df[ df.floor.notnull() & df.rooms.notnull()]
# Fit regression model 
result = smf.ols('price ~ pow + C(rooms) + C(floor) ', data=df).fit()

# Inspect the results
print result.summary()
