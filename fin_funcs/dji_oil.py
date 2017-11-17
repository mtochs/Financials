import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
#import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.data as web
plt.style.use('ggplot')

def dji_oil(freq='M', start_date = '1986-01-01', 
		end_date = datetime.datetime.today().strftime('%Y-%m-%d')):
	
	# Collect daily oil data from St Louis Fed
	oil = web.DataReader('DCOILWTICO', 'fred', start_date, end_date)
	# Phase shift dates 10 years forward
	oil.index = oil.index + pd.Timedelta(days=365*10) # phase shift oil 10 years forward
	oil.columns = ['oil']
	
	# Get Dow Jones data
	oil['dji'] = pdr.get_data_yahoo(symbols='^DJI', start=start_date, end=end_date)['Close']

	# Resample data to reduce static
	oil = oil.resample(freq).mean()
	
	# Create plot
	fig, ax = plt.subplots()
	ax.grid(True)
	ax2 = ax.twinx()

	# Use log scaling for both data sets
	fig1 = oil['oil'].plot(ax=ax, color='black').set_yscale('log')
	fig2 = oil['dji'].plot(ax=ax2, color='blue', secondary_y=True).set_yscale('log')
	
	x_min, x_max = oil.index.min(), oil.index.max()
	plt.xlim(xmin=x_min, xmax=x_max)
	plt.title('Oil, DJI Chart')
	fig.autofmt_xdate()
	fig.set_size_inches(16, 9)
	fig.tight_layout()
	return oil, plt


if __name__ == "__main__":
	'''
	from fredapi import Fred
	# Previous way to grab fred data before using pdr's 'web'
	fred = Fred(api_key='e37f5aff803c4bc3c4f2b727bd5d9f70')
	oil = fred.get_series('DCOILWTICO')
	# Convert to pandas dataframe
	oil = pd.DataFrame({
		'Date':oil.keys().tolist(),
		'oil':oil.tolist() })
	oil.set_index('Date', inplace=True)
	'''

	df, plt = dji_oil()
	plt.show()