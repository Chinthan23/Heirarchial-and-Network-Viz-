import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

def get_sunburst_for_coin(coin):
	coin_data=pd.read_csv("./data/coin_"+coin+".csv")
	months={1: "Jan",2: "Feb",3: "Mar",4: "Apr",5: "May",6: "Jun",7: "Jul",8: "Aug",9: "Sep",10: "Oct",11: "Nov", 12 : "Dec"}
	coin_data["Year"]=coin_data.apply(lambda row: row.Date[:4] , axis=1)
	coin_data["Month"]=coin_data.apply(lambda row: months[int(row.Date[5:7])] , axis=1)
	coin_data["Date1"]=coin_data.apply(lambda row: row.Date[8:10] , axis=1)
	fig=px.sunburst(data_frame=coin_data,values='Volume',path=['Year','Month','Date1'],
	color="Volume",color_continuous_scale='thermal_r',width=1600,height=1600, title="Sunburst visualisation showing volume traded for "+coin+".")
	return fig

coin="Ethereum"
sunburst=get_sunburst_for_coin(coin)
sunburst.show()