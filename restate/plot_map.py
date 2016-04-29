# coding: utf-8
import sys
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

from data.data import clean_data

matplotlib.style.use('ggplot')
date = "290416"
if len(sys.argv) >1:
    date = sys.argv[1]

df = pd.read_csv("data/szczecin_%s.csv"%date)
# leave only interesting observaions
# df=df[df['pow'] <250]
df = df[df.rooms<=5]
df = df[df.data_lat != 0]
df=df[df.location.str.contains( "Szczecin")]
df=df[df['data_lat']<53.6]
df=df[df['data_lat']>53.32]
df=df[df['data_lon']>14.0]
df=df[df['data_lon']<14.8]

# Replace price
df['price'] = df.price.str.replace(" zł", "")
df['price'] = df.price.str.replace(" ", "")
df['price'] = df.price.str.replace(",", ".")
df['price'] = df.price.astype("float")

ax = df.plot(kind='hexbin', y='data_lat', x='data_lon', C='price',
             reduce_C_function=np.mean, gridsize = 50, cmap=plt.cm.Greens)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
fig = ax.get_figure()
fig.savefig("graphs/price_map_%s.png"%date)
