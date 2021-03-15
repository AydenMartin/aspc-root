import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from https://medium.com/left-join/beautiful-bar-charts-with-python-and-matplotlib-not-published-d97b1e1f32e3
def genSigStrGraph_Example():
    #con = sqlite3.connect("data/portal_mammals.sqlite")
    #df = pd.read_sql_query("SELECT * from surveys", con)

    df = pd.read_csv('data.csv')
    colors = []
    arr = df.values
    for x in arr:
        if(x[1] < x[2]):
            colors.append('#ff0000')
        else:
            colors.append('#ffc001')
    xticks = df.iloc[:, 0]
    try:
        bars2 = df.iloc[:, 1].str.replace(',', '.').astype('float')
    except AttributeError:
        bars2 = df.iloc[:, 1].astype('float')
    try:
        bars1 = df.iloc[:, 2].str.replace(',', '.').astype('float')
    except AttributeError:
        bars1 = df.iloc[:, 2].astype('float')

    fig = plt.figure()
    fig.suptitle('MeshNet Signal Strenth: MBPS', fontsize=12)
    plt.xlabel('Leaf Devices', fontsize=12)


    barWidth1 = 0.085
    barWidth2 = 0.032
    x_range = np.arange(len(bars1) / 8, step=0.125)

    plt.bar(x_range, bars1, color='#e6ffee', width=barWidth1 / 2, edgecolor='#c3d5e8', label='T')
    plt.bar(x_range, bars2, color=colors, width=barWidth2 / 2, edgecolor='#c3d5e8', label='A')
    for i, bar in enumerate(bars2):
        plt.text(i / 8 - 0.015, bar + 1, bar, fontsize=8)


    plt.xticks(x_range, xticks)
    plt.tick_params(
        bottom=False,
        left=False,
        labelsize=12
    )

    plt.rcParams['figure.figsize'] = [25, 7]
    plt.axhline(y=0, color='gray')

    plt.box()




    plt.savefig("Charts/speed.jpg", dpi=300)