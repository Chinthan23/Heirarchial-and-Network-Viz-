import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

data_files_path = []
for dirname, _, filenames in os.walk('./data/'):
    for filename in filenames:
        data_files_path.append(os.path.join(dirname, filename))
#         print(os.path.join(dirname, filename))

coins_df = []
for path in data_files_path:
    coins_df.append(pd.read_csv(path))

all_coins_df = pd.concat([coins_df[6], coins_df[10], coins_df[4]])
all_coins_df['Symbol'] = all_coins_df['Symbol'].astype('category')
all_coins_df['Coin_id'] = all_coins_df['Symbol'].cat.codes

def scatter_matrix_plot(df):
    fig = go.Figure(data=go.Splom(
                dimensions=[dict(label='High',
                                 values=df['High']),
                            dict(label='Low',
                                 values=df['Low'],),
                            dict(label='Open',
                                 values=df['Open']),
                            dict(label='Close',
                                 values=df['Close']),
                           dict(label='Volume',
                                 values=df['Volume']),
                           dict(label='Marketcap',
                                 values=df['Marketcap'])],
                text=df['Name'],
                showupperhalf=False,
                marker=dict(color=df['Coin_id'],
                            colorscale='rainbow',
                            showscale=False, # colors encode categorical variables,
                            opacity=0.8,
                            line_color='white', line_width=0.5)
                ))


    fig.update_layout(
        title='Cryptocurrency History',
        width=1000,
        height=1000,
    )

    return fig
scatter_matrix=scatter_matrix_plot(all_coins_df)
scatter_matrix.show()