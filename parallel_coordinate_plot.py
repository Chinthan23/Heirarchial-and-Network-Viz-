import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px

data_files_path = []
for dirname, _, filenames in os.walk('./data/'):
    for filename in filenames:
        data_files_path.append(os.path.join(dirname, filename))

coins_df = []
for path in data_files_path:
    coins_df.append(pd.read_csv(path))

all_coins_df = pd.concat([coins_df[6], coins_df[7], coins_df[4]])
all_coins_df['Symbol'] = all_coins_df['Symbol'].astype('category')
all_coins_df['Coin_id'] = all_coins_df['Symbol'].cat.codes

colorarray=px.colors.qualitative.Dark2

def plot_parallel_coords(df, color_param):
    df["Year"]=df.apply(lambda row: (int)(row.Date[:4]) , axis=1)
    df["Month"]=df.apply(lambda row: (int)(row.Date[5:7]) , axis=1)
    df["Day"]=df.apply(lambda row: (int)(row.Date[8:10]) , axis=1)
    df["Date1"] = (df['Year'] * 100 + df['Month']) * 100 + df['Day'] 
    # print(df['Year'].max())
    # print(df['Year'].min())
    date_min = df['Date1'].min()
    date_max = df['Date1'].max()    
    ticks = df.loc[(df['Day'] == 1) & (df['Month'] == 4)]
    df = df.loc[df['Day'] == 1]
    # print(ticks['Year'].max())
    # print(ticks['Year'].min())
    # print(ticks.head())
    # print(df.head())
    min_val = min(df['Low'].min(),df['High'].min(),df['Open'].min(), df['Close'].min())
    max_val = max(df['Low'].max(),df['High'].max(),df['Open'].max(), df['Close'].max())
    fig = go.Figure(data=
        go.Parcoords(
            line = dict(color = df[color_param],
                       colorscale = [[0,colorarray[0]],[0.5,colorarray[3]],[1,colorarray[6]]],
                       showscale = False),
            dimensions = list([
                dict(range = [0, 2],
                    label = 'Coin_id', values = df['Coin_id'],
                    ticktext=list(df["Symbol"].unique()),tickvals=list(df['Coin_id'].unique())),

                dict(range = [date_min, date_max],
                     tickvals = list(ticks['Date1']),
                     ticktext = list((ticks['Date1'] //10000).unique()),
                    label = 'Date', values = df['Date1']),
                dict(range = [min_val, max_val],
                    label = 'Low', values = df['Low']),
                dict(range = [min_val, max_val],
                    label = 'High', values = df['High']),
                dict(range = [min_val, max_val],
                    label = 'Open', values = df['Open']),
                dict(range = [min_val, max_val],
                    label = 'Close', values = df['Close'])
            ])
        )
    )
    return fig


parallel_coords=plot_parallel_coords(all_coins_df, "Coin_id")
parallel_coords.show()




