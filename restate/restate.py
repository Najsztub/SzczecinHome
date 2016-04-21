# -*- coding: utf-8 -*-
# MN: 08/04/16

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

from data.data import clean_data

matplotlib.style.use('ggplot')

def plot_price_area(out, show = False):
    g = sns.FacetGrid(df, col="rooms", col_wrap=2)
    g.map(plt.scatter, "pow", "price")
    g.savefig(out)
    if show:
        plt.show()

def plot_year_hist(out, show = False):
    ax = df.build_year.astype(float).hist(bins=100)
    ax.set_xlim(1900, 2017)
    ax.set_xlabel("Construction year")
    ax.set_ylabel("N. obs.")
    fig = ax.get_figure()
    fig.savefig("graphs/construction_year_hist.png")
    if show:
        plt.show()
    plt.close(fig)

if __name__ == "__main__":
    print "Load data"
    df = pd.read_csv("data/items_otodom.pl_080416_10.csv", encoding = 'utf-8')
    print "Clean data"
    df = clean_data(df)
    # leave only interesting observaions
    df=df[df.price >50]
    df=df[df.price<600]
    df=df[df['pow'] <250]
    df = df[df.rooms<=5]

    print "Plot year of construction histogram"
    plot_year_hist("graphs/construction_year_hist.png")

    print "Plot price/area by rooms"
    plot_price_area("graphs/price_pow.png")

    
