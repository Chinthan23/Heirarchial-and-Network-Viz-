# %%
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib
import json

# %% [markdown]
# # Loading Data

# %%
data_files_path = []
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        data_files_path.append(os.path.join(dirname, filename))
#         print(os.path.join(dirname, filename))

# %%
coins_df = []
for path in data_files_path:
    coins_df.append(pd.read_csv(path))

# %%
len(coins_df), coins_df[0].shape

# %%
coins_df[0].head()

# %%
def compute_change(coins_df, variable = 'Close'):
    for df in coins_df:
        variable_values = list(df[variable])
        variable_values.append(0)
        df[variable + '_change'] = [((next_day - present_day)*100.0)/present_day for present_day, next_day in zip(variable_values, variable_values[1:])]

# %%
compute_change(coins_df)

# %%
coins_df[9].head()

# %%
def get_all_coins_change(coins_df, date, variable='Close'):
    
    name_array = []
    symbol_array = []
    date_array = []
    change_array = []
    
    
    for df in coins_df:
        coin_data = df.loc[df['Date'] == date][['Name', 'Symbol', 'Date', variable + '_change']]
        if coin_data.shape[0] > 0:
#             print(coin_data.head())
            name_array.append(coin_data.iloc[0]['Name'])
            symbol_array.append(coin_data.iloc[0]['Symbol'])
            date_array.append(coin_data.iloc[0]['Date'])
            change_array.append(coin_data.iloc[0][variable + '_change'])

    print(name_array)
    print(symbol_array)
    data = {'Name': name_array, 
            'Symbol': symbol_array, 
            'Date': date_array, 
            variable + '_change': change_array}
    all_coins_change_df = pd.DataFrame(data)
    return all_coins_change_df

# %%
date_to_viz = "2021-01-27"

# %%
all_coins_close_change_df = get_all_coins_change(coins_df, date_to_viz + ' 23:59:59', variable='Close')

# %%
# all_coins_close_change_df.sort_values('Close_change')

# %%
all_coins = ['Chainlink', 'Cardano', 'Solana', 'Dogecoin', 'Polkadot', 'NEM', 'XRP', 'Ethereum', 
             'Aave', 'Bitcoin', 'Cosmos', 'Litecoin', 'Uniswap', 'EOS', 'Binance Coin', 'Crypto.com Coin', 
             'USD Coin', 'Monero', 'TRON', 'Wrapped Bitcoin', 'Tether', 'IOTA', 'Stellar']
all_coins_symbol = ['LINK', 'ADA', 'SOL', 'DOGE', 'DOT', 'XEM', 'XRP', 'ETH', 
                    'AAVE', 'BTC', 'ATOM', 'LTC', 'UNI', 'EOS', 'BNB', 'CRO', 
                    'USDC', 'XMR', 'TRX', 'WBTC', 'USDT', 'MIOTA', 'XLM']

# %%
def get_edges(max_diff = 2, variable='Close'):
    edgelist = ""
    for c1 in all_coins_symbol:
        for c2 in all_coins_symbol:
            c1_change = all_coins_close_change_df.loc[all_coins_close_change_df['Symbol'] == c1][variable + '_change']
            c2_change = all_coins_close_change_df.loc[all_coins_close_change_df['Symbol'] == c2][variable + '_change']
            if c1 != c2 and c1_change.shape[0]>0 and c2_change.shape[0]>0 and abs(float(c1_change) - float(c2_change)) < max_diff:
                edgelist += c1 + ' ' + c2 + ' ' + str(1/abs(float(c1_change) - float(c2_change))) + ' \n'
    return edgelist

# %%
edgelist = get_edges(max_diff=1)

# %%
f = open("./edgelist.txt", "w")
f.write(edgelist)
f.close()

# %% [markdown]
# # Network Visualization

# %% [markdown]
# Edge if 0<diff<max_diff.
# 
# max_diff = 2
# 
# Edge weight = 1/diff
# 
# 
# Node color: green for positive and red for negative

# %%
G=nx.read_weighted_edgelist("./edgelist.txt")

# %%
# add all nodes to graph
for coin in list(all_coins_close_change_df['Symbol']):
#     coin_value = float(all_coins_close_change_df.loc[all_coins_close_change_df['Symbol'] == coin]['Close_change'])
    G.add_node(coin, weight = float(all_coins_close_change_df.loc[all_coins_close_change_df['Symbol'] == coin]['Close_change']))

# %%
s =nx.node_link_data(G)
json_graph = json.dumps(s)
with open("json_out.json", "w") as outfile:
    outfile.write(json_graph)

# %% [markdown]
# ## Circular Node-Link Diagram

# %%
plt.figure(figsize=(8, 5))
color_map = ['green' if 
             float(all_coins_close_change_df.loc[all_coins_close_change_df['Symbol'] == node]['Close_change'])>=0  
             else 'red' for node in G]
positive_nodes = all_coins_close_change_df[all_coins_close_change_df['Close_change']>=0]['Symbol']
negative_nodes = all_coins_close_change_df[all_coins_close_change_df['Close_change']<0]['Symbol']

pos=nx.circular_layout(G)
nx.draw(G, pos=pos, nodelist = positive_nodes, with_labels = True, node_color = "green")
nx.draw(G, pos=pos, nodelist = negative_nodes, with_labels = True, node_color = "red")
plt.title("Network visualization of coins that have similar close price change behavior on "+ date_to_viz + " (green for positive change, red for negative change)")
plt.show()

# %% [markdown]
# ## Force-directed Node-Link Diagram

# %%
plt.figure(figsize=(8, 5))
color_map = ['green' if 
             float(all_coins_close_change_df.loc[all_coins_close_change_df['Symbol'] == node]['Close_change'])>=0  
             else 'red' for node in G]
positive_nodes = all_coins_close_change_df[all_coins_close_change_df['Close_change']>=0]['Symbol']
negative_nodes = all_coins_close_change_df[all_coins_close_change_df['Close_change']<0]['Symbol']

pos=nx.spring_layout(G, k=0.7, iterations=25)
nx.draw(G, pos=pos, nodelist = positive_nodes, with_labels = True, node_color = "green")
nx.draw(G, pos=pos, nodelist = negative_nodes, with_labels = True, node_color = "red")
plt.title("Network visualization of coins that have similar close price change behavior on "+ date_to_viz + " (green for positive change, red for negative change)")
plt.show()

# %%
plt.figure(figsize=(8, 5))

values = [float(all_coins_close_change_df.loc[all_coins_close_change_df['Symbol'] == node[0]]['Close_change'])  for node in G.nodes(data=True)]

cm = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red","white","green"])

pos=nx.spring_layout(G, k=0.7, iterations=25)

cm = matplotlib.cm.get_cmap("RdYlGn")
for node in G.nodes():
    value = float(all_coins_close_change_df.loc[all_coins_close_change_df['Symbol'] == node]['Close_change'])
    nx.draw(G, pos=pos, nodelist = [node], with_labels = True, node_color = cm((value/(2*max(values)))+0.5))

sm = plt.cm.ScalarMappable(cmap=cm, norm=plt.Normalize(vmin = -max(values), vmax=max(values)))
sm._A = []
cbar = plt.colorbar(sm, fraction=0.046, pad=0.04)
cbar.set_label("Percentage change in close price for cryto currencies")
plt.title("Network visualization of coins that have similar close price change behavior on " + date_to_viz)
plt.show()

# %%
# all_coins_close_change_df.sort_values(['Close_change'])

# %% [markdown]
# # Matrix Visualization

# %%
def get_adj_matrix(variable='Close'):
    matrix = []
    for c1 in all_coins_symbol:
        matrix_row = []
        for c2 in all_coins_symbol:
            c1_change = all_coins_close_change_df.loc[all_coins_close_change_df['Symbol'] == c1][variable + '_change']
            c2_change = all_coins_close_change_df.loc[all_coins_close_change_df['Symbol'] == c2][variable + '_change']
            matrix_row.append(abs(float(c1_change) - float(c2_change)) )
        matrix.append(matrix_row)
    return matrix

# %%
adjacency_matrix = get_adj_matrix()

# %%
adjacency_matrix = np.array(adjacency_matrix)

# %%
adjacency_matrix = np.log(adjacency_matrix)

# %%
fig = plt.figure(figsize=(7, 7)) # in inches
cm = matplotlib.cm.get_cmap("magma").copy()
cm.set_bad(color="white")
plt.imshow(adjacency_matrix,
                  cmap=cm,
                  interpolation="none")
sm = plt.cm.ScalarMappable(cmap="magma", norm=plt.Normalize(vmin =np.nanmin(adjacency_matrix), vmax=np.nanmax(adjacency_matrix)))
sm._A = []
cbar = plt.colorbar(sm, fraction=0.046, pad=0.04)
plt.xticks(range(len(all_coins_symbol)), all_coins_symbol, rotation=90)
plt.yticks(range(len(all_coins_symbol)), all_coins_symbol)
cbar.set_label("Difference of percentage change of closing price (log scale)")
plt.title("Adjacency matrix visualization showing difference of %change in price for coins" + date_to_viz)
plt.show()


