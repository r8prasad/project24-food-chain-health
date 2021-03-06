"""
Created on Sun June 2 2019
@author: adnan
"""

import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import subplots
import matplotlib.colors as mcolors


def threshold_on_metric(df, columns_filter, thresh_info):
	assert isinstance(df, pd.DataFrame)
	assert isinstance(columns_filter, list) and len(columns_filter)>0
	assert isinstance(thresh_info, dict) and len(thresh_info) == len(columns_filter)-1
	# Add Final_Score column to dataframe
	df['Final_Score'] = 0.0

	# Thresholding on metrics
	for metric in columns_filter[1:]:
		# Retrieving thresholding information
		rmin = thresh_info[metric][0]
		rmax = thresh_info[metric][1]
		# print('rmin, rmax = ',rmin, rmax)
		# print('df[metric] = ', df[metric])
		# Thresholding each metrics
		df[metric] = df[metric].apply(lambda x: True if (rmin <= x <= rmax) else False) #converting True/False to 1/0
		#df[metric] = (2*df[metric] - 1) #converting 1/0 to 1/-1 and then flipping the logic if needed
		df["Protein Metric"].replace([0,1], [-1,1], inplace=True) 
		#df["Fat Metric"].replace([0,1], [-1,0], inplace=True) 
		df["Carbs Metric"].replace([0,1], [-1,0], inplace=True) 
		#df["Cholesterol Metric"].replace([0,1], [-1,0], inplace=True) 
		df["Saturated Fat Metric"].replace([0,1], [-1,0], inplace=True) 
		df["Trans Fat"].replace([0,1], [-1,0], inplace=True) 
		# Calculating final score based on threholded metric value
		df['Final_Score'] += df[metric]
		# print(df['Final_Score'])
	return df

def main():
	
	# Initializations
	data_folder = '../../data/FinalData'
	extra_str = ''
	ext = '.csv'
	columns_filter = ['Item', 'Carbs Metric', 'Cholesterol Metric', 'Protein Metric', 'Trans Fat', 'Saturated Fat Metric']
	# Setting acceptable range for each metric
	thresh_info = {	'Carbs Metric': [0.9, 1.2],
						'Cholesterol Metric': [0.0, 1.1],
						'Protein Metric': [0.9, 20.0],
						'Trans Fat': [0.0,1.1],
						'Saturated Fat Metric': [0.9, 1.1]}
	assert len(columns_filter)-1 == len(thresh_info), 'Number of metrics mismatch'
	# Importing CSS colors
	colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

	# Getting names of restaurants
	restaurant_names = ['DunkinDonuts', 'Dominos', 'ChickFilA','BurgerKing', 'Mcdonalds', 'PaneraBread', 'PizzaHut', 'KFC', 'Subway', 'PandaExpress']
	# restaurant_names = os.listdir(data_folder)
	# restaurant_names = [name.split('.')[0] for name in restaurant_names]
	assert len(restaurant_names) > 0, 'Need to have atleast one restaurant csv file!'


	fig, axs = plt.subplots(2, 5, figsize=(12, 6), sharey=True)
	fig.subplots_adjust(hspace = .5, wspace=.2)
	axs = axs.flatten()
	pie_colors = [colors['lime'], colors['lightsteelblue'], colors['crimson']]
	
	for i in range(0,len(restaurant_names)):
		# Reading the csv file and storing as DataFrame
		restaurant = restaurant_names[i]
		print('Processing info from restaurant - ', restaurant)
		df = pd.read_csv(data_folder+'/'+restaurant+extra_str+ext, encoding = 'iso-8859-1') 
		# Selecting columns with metrics only
		df = df[columns_filter]
		# Thresholding all metrics based on thresh_info
		df = threshold_on_metric(df, columns_filter, thresh_info)
		# Sorting according to final score
		df = df.sort_values(by='Final_Score')
		# Counting according to final score
		df_count = df.groupby(by='Final_Score').count()['Item']
		# Counting how many food items as good, bad or neutral
		info = {'healthy': sum(df['Final_Score']>=0),
				'neutral': sum(df['Final_Score']==-1),
				'unhealthy': sum(df['Final_Score']<-1)
				}
		# Convert from counts to percentage
		denom = sum(info.values())
		info = {k:v*100/denom for k,v in info.items()}
		# Plotting
		_, _, legend_props = axs[i].pie(list(info.values()), colors = pie_colors, autopct='%1.1f%%', wedgeprops = {'edgecolor':'0', 'linewidth':0.5})
		axs[i].set_title(restaurant)

	plt.tight_layout()
	fig.legend(legend_props, labels = ('Healthy', 'Neutral', 'Unhealthy'), loc = 'lower right')
	# plt.show()
	plt.savefig('healthy_vs_unhealthy', dpi=300)

if __name__ == '__main__':
	main()