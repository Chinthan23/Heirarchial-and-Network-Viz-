import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import os

data_files_path = []
for dirname, _, filenames in os.walk('./data/'):
    for filename in filenames:
        data_files_path.append(os.path.join(dirname, filename))

coins_df = []
for path in data_files_path:
    coins_df.append(pd.read_csv(path))

def get_all_coins_on_given_date(coins_df,date):
	name_array = []
	symbol_array = []
	date_array = []
	# volume_traded_array = []
	volume_array = []
	
	for df in coins_df:
			coin_data = df.loc[df['Date'] == date][['Name', 'Symbol', 'Date','Volume']]
			if coin_data.shape[0] > 0:
					name_array.append(coin_data.iloc[0]['Name'])
					symbol_array.append(coin_data.iloc[0]['Symbol'])
					date_array.append(coin_data.iloc[0]['Date'])
					volume_array.append(coin_data.iloc[0]['Volume'])
					# volume_traded_array.append(coin_data.iloc[0]['Value of volume'])
	data = {'Name': name_array, 
					'Symbol': symbol_array, 
					'Date': date_array, 
					# 'Value of volume': volume_traded_array,
					'Volume': volume_array}
	all_coins_change_df = pd.DataFrame(data)
	return all_coins_change_df

def get_sunburst_all_coins_given_date(coins_df,date):
	all_coins_volume_traded_df = get_all_coins_on_given_date(coins_df, date)
	fig=px.sunburst(data_frame=all_coins_volume_traded_df,values='Volume',path=['Symbol'],color="Volume",
	title="Sunburst visualisation showing volume traded for all coins traded on {}.".format(date[:11]))#,width=1600,height=1200)
	return fig

date='2017-10-02 23:59:59'
# all_coins_value_of_volume_traded_df = get_all_coins_on_given_date(coins_df, '2017-10-02 23:59:59')
sunburst_all_coins=get_sunburst_all_coins_given_date(coins_df,date)
sunburst_all_coins.show()