# -*- coding: utf-8 -*-
# MN: 08/04/16

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
matplotlib.style.use('ggplot')

def clean_data(df):
    # Drop redundant columns
    df.drop(['_template', '_type', '_cached_page_id'], axis = 1, inplace = True)
    
    # Clean description
    df['description'] = df['description'].str.replace("^Opis ", "")
    # Clean location
    df['location'] = df['location'].str.replace(" - Zobacz na mapie", "")
    df['location'] = df['location'].str.extract("([\w\s]+\s,\s)(.*)", re.UNICODE)[1]
    loc = df['location'].str.split(", ", expand = True)[[0, 1, 2]]
    loc.rename(columns = {0: 'city', 1:'district', 2:'street'}, inplace=True)
    # Remove trailing spaces
    for c in loc.columns:
        loc[c] = loc[c].str.replace('\s+$', '')
    # Write city, district, 
    df.drop('location', axis = 1, inplace = True)
    df = pd.concat([df, loc], axis =1 )
    
    # Leave only Szczecin
    df = df[df['city'] == "Szczecin"]
    
    # Create year of construction
    df['build_year'] = df['details'].str.extract("(rok budowy: )([0-9]{4})")[1]
    # Create market type
    df['rynek'] = df['details'].str.extract("(rynek: )(\w+)", re.UNICODE)[1]
    
    df['okna'] = df['details'].str.extract("(okna: )(\w+)", re.UNICODE)[1]
    
    df['zabudowa'] = df['details'].str.extract("(rodzaj zabudowy: )(\w+)", re.UNICODE)[1]
    
    df['ogrzewanie'] = df['details'].str.extract("(ogrzewanie: )(\w+)", re.UNICODE)[1]
    
    df['wlasnosc'] = df['details'].str.extract(u"(forma własności: )(\w+)", re.UNICODE)[1]
    
    df['material'] = df['details'].str.extract(u"(materiał budynku: )(\w+)", re.UNICODE)[1]
    df.loc[df.material == "wielka", 'material'] = "wielka płyta"
    
    df['czynsz'] = df['details'].str.extract("(czynsz: )([0-9]+)")[1]
    
    # Clean data  

    df.loc[df.build_year.astype(float) < 1600, 'build_year'] = np.NaN

    # Replace NaN in floor as ground floor
    df.loc[df.floor.isnull(), 'floor'] = 0

    return df

if __name__ == "__main__":
    print "Load data"
    df = pd.read_csv("data/items_otodom.pl_080416_10.csv", encoding = 'utf-8')
    print "Clean data"
    df = clean_data(df)
    # leave only interesting observaions
    df=df[df.price >50]
    df=df[df.price<600]
    df=df[df['pow'] <250]
    df = df[df.rooms<=4]


    print "Plot year of construction histogram"
    ax = df.build_year.astype(float).hist(bins=100)
    ax.set_xlim(1900, 2017)
    ax.set_xlabel("Construction year")
    ax.set_ylabel("N. obs.")
    fig = ax.get_figure()
    fig.savefig("graphs/construction_year_hist.png")
    plt.show()
    plt.close(fig)

    print "Plot price/area by rooms"
    g = sns.FacetGrid(df, col="rooms", col_wrap=2)
    g.map(plt.scatter, "pow", "price")
    g.savefig("graphs/price_pow.png")
    plt.show()

    
