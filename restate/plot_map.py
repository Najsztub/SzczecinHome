# coding: utf-8
import sys
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import smopy
#from data.data import clean_data

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
# Replace price
df['price'] = df.price.str.replace(" zł", "")
df['price'] = df.price.str.replace(" ", "")
df['price'] = df.price.str.replace(",", ".")
df['price'] = df.price.astype("float")

# Replace square meters as number
df['pow'] = df['pow'].str.replace("[^0-9,\.]", "")
df['pow'] = df['pow'].str.replace(",", ".")
df['pow'] = df['pow'].astype("float")

# Generate price per sq_meter
df['sq_price'] = df['price']/df['pow']

# Remove houses priced above 99.9% of prices
df = df[df.sq_price < df.sq_price.quantile(0.999)]

# Szczecin + Prawobrzeże
min_lat = 53.35
max_lat = 53.55
min_lon = 14.42
max_lon = 14.75

df=df[df['data_lat']>min_lat]
df=df[df['data_lat']<max_lat]
df=df[df['data_lon']>min_lon]
df=df[df['data_lon']<max_lon]

ax = df.plot(kind='hexbin', y='data_lat', x='data_lon', C='price',
             reduce_C_function=np.mean, gridsize = 50, cmap=plt.cm.Greens)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
fig = ax.get_figure()
fig.savefig("graphs/price_map_%s.png"%date)

########################################
# Plot hexbin map

#df = df[df.price < 600000]

# Szczecin: Lewobrzeże
min_lat = 53.38
max_lat = 53.5
min_lon = 14.44
max_lon = 14.62

df=df[df['data_lat']>min_lat]
df=df[df['data_lat']<max_lat]
df=df[df['data_lon']>min_lon]
df=df[df['data_lon']<max_lon]

print "Downloading map from Openstreetmap..."
map = smopy.Map((min_lat, min_lon, max_lat, max_lon), z=13)
print "Done"

dd=map.to_pixels(df.data_lat, df.data_lon)
pdf = pd.DataFrame({
    'lon':dd[0],
    'lat':dd[1],
    'price':df['price'],
    'sq_price':df['sq_price']
    })

img = map.to_pil()
dpi = 300
img_size = (2*img.size[0]/dpi, 1.6*img.size[1]/dpi)
# Plot price and price per sq_meter
for p in ['price', 'sq_price']:
    print "Plot %s"%p
    # Clear plot area
    plt.figure(figsize = img_size, dpi = dpi)
    plt.axis("off")
    plt.imshow(img)
    plt.hexbin(y=pdf['lat'], x=pdf['lon'], C=pdf[p],
               reduce_C_function=np.mean, gridsize = 50,
               cmap=plt.cm.Spectral_r, alpha = 0.75)
    cb = plt.colorbar(fraction=0.046, pad=0.04)
    cb.set_label('House price [PLN]')
    plt.tight_layout()
    plt.savefig(
        "graphs/price_map_%s_%s_withMap.png"%(date, p),
        dpi=dpi)


