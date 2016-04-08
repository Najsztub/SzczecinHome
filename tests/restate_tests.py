from nose.tools import *
import restate

def setup():
    print "SETUP!"
    
def teardown():
    print "TEAR DOWN!"
    
def test_basic():
    print "I RAN!"

def test_create_sample_data():
    print "Creates data in sample_data as 5% sameple of real data"
    import pandas as pd
    print "Load pandas data"
    df = pd.read_csv("data/items_otodom.pl_270316_8.csv", encoding = 'utf-8')
    df = df.sample(frac = 0.05)
    print "Save clean dataset"
    df.to_csv("sample_data/items_otodom.pl_270316_8_sample.csv", encoding = 'utf-8')
    
