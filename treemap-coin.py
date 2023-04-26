import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

def get_treemap_for_coin(coin):
	coin_data=pd.read_csv("./data/coin_"+coin+".csv")
	months={1: "Jan",2: "Feb",3: "Mar",4: "Apr",5: "May",6: "Jun",7: "Jul",8: "Aug",9: "Sep",10: "Oct",11: "November", 12 : "December"}
	coin_data["Year"]=coin_data.apply(lambda row: row.Date[:4] , axis=1)
	coin_data["Month"]=coin_data.apply(lambda row: months[int(row.Date[5:7])] , axis=1)
	coin_data["Date1"]=coin_data.apply(lambda row: row.Date[8:10] , axis=1)
	fig=px.treemap(data_frame=coin_data,path=[px.Constant(coin),'Year','Month'],values='Volume',color="Volume",color_continuous_scale="magma_r",
	title="Treemap visualisation showing volume traded for "+coin+".")
	fig.update_traces(root_color="grey")
	return fig

coin="Ethereum"
treemap=get_treemap_for_coin(coin)
treemap.show()