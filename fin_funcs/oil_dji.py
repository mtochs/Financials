djiimport datetime
from fredapi import Fred
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import pandas_datareader as pdr
plt.style.use('ggplot')

def dji_oil(freq='M', start_date = '1980-01-01', 
		end_date = datetime.datetime.today().strftime('%Y-%m-%d')):
	
	# Collect daily oil data from St Louis Fed
	fred = Fred(api_key='e37f5aff803c4bc3c4f2b727bd5d9f70')
	oil = fred.get_series('DCOILWTICO')
	# Convert to pandas dataframe
	oil = pd.DataFrame({
		'Date':oil.keys().tolist(),
		'oil':oil.tolist() })
	oil.set_index('Date', inplace=True)

	oil.index = oil.index + pd.Timedelta(days=365*10) # phase shift oil 10 years forward
	x_min, x_max = oil.index.min(), oil.index.max()

	df = pdr.get_data_yahoo(symbols='^DJI', start=start_date, end=end_date)['Close']

	# Resample data to reduce static
	oil = oil.resample(freq).mean()
	df = df.resample(freq).mean()

	# Create plot
	fig, ax = plt.subplots()
	ax2 = ax.twinx()

	# Use log scaling for both data sets
	fig1 = oil.plot(ax=ax, color='black').set_yscale('log')
	fig2 = df.plot(ax=ax2, color='blue', secondary_y=True).set_yscale('log')

	# **************** Formatting graph parameters ****************
	# Source: https://matplotlib.org/devdocs/gallery/api/date.html
	years = mdates.YearLocator()   # every year
	months = mdates.MonthLocator()  # every month
	yearsFmt = mdates.DateFormatter('%Y')
	# Set xaxis tick format
	#ax.xaxis.set_major_locator(years)
	#ax.xaxis.set_major_formatter(yearsFmt)
	#ax.xaxis.set_minor_locator(months)
	ax.grid(True)
	fig.autofmt_xdate()
	fig.set_size_inches(16, 9)
	fig.tight_layout()
	ax.set_title('Oil, DJI Chart')
	plt.xlim(xmin=x_min, xmax=x_max)
	return plt