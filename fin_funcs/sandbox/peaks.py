from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
#import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.data as web
pd.options.display.width = 640
plt.style.use('ggplot')

def get_peaks(freq='M', tick='^GSPC', start_date = '1986-01-01', 
		end_date = datetime.today().strftime('%Y-%m-%d')):
	
	# Get S&P data
	df = pdr.get_data_yahoo(symbols=tick, start=start_date, end=end_date)

	high_max = df[df.High == df.High.max()]['High']
	close_max = df[df.Close == df.Close.max()]['Close']
	low_min = df[df.Low == df.Low.min()]['Low']
	close_min = df[df.Close == df.Close.min()]['Close']
	print "\nhigh max: \n", high_max
	print "\nclose max: \n", close_max
	print "\nlow min: \n", low_min
	print "\nclose min: \n", close_min
	print "\ndiff: ", (low_min - high_max) / high_max
	
	return df

def gains_by_threshold(freq='D', tick='^GSPC', threshold=0, start_date = '2010-01-01', 
		end_date = datetime.today().strftime('%Y-%m-%d')):
	
	# Get S&P data
	df = pdr.get_data_yahoo(symbols=tick, start=start_date, end=end_date)['Close']
	df = df.pct_change()
	df = df[df.abs() > threshold]
	return df


if __name__ == "__main__":
	#df = get_peaks(start_date='1999-01-01', end_date='2003-12-01')
	df = gains_by_threshold(threshold=0.015)
	print df.tail(20)