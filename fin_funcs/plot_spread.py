import datetime
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import pandas_datareader as pdr
plt.style.use('ggplot')

yield_names = {
	'^IRX' : '13 Week',
	'^FVX' : '5',
	'^TNX' : '10',
	'^TYX' : '30'
}

def plot_spread(tickers=['^IRX','^TYX'], start_date='1995-01-01',
		end_date=datetime.datetime.today().strftime('%Y-%m-%d')):
	df = pd.DataFrame(data=None, columns=['A', 'B', 'diff'])
	df.B = pd.to_numeric(pdr.get_data_yahoo(symbols=tickers[1], start=start_date, end=end_date)['Close'], downcast='float')
	df.A = pd.to_numeric(pdr.get_data_yahoo(symbols=tickers[0], start=start_date, end=end_date)['Close'], downcast='float')
	df['diff'] = df['B'].subtract(df['A'])
	# Last data point	
	last = df.iloc[-1]['diff']

	fig, ax = plt.subplots()
	ax.set_title(yield_names[tickers[0]] + ' to ' + yield_names[tickers[1]] + ' Year Spread')
	years = mdates.YearLocator()   # every year
	months = mdates.MonthLocator()  # every month
	yearsFmt = mdates.DateFormatter('%Y')
	# Set xaxis tick format
	ax.xaxis.set_major_locator(years)
	ax.xaxis.set_major_formatter(yearsFmt)
	ax.xaxis.set_minor_locator(months)
	ax.grid(True)
	
	df['diff'].plot(color='#5687d4')
	# Horizontal line at last data point
	plt.axhline(y=last, color='#d62728')
	
	fig.set_size_inches(16, 9)
	fig.tight_layout()
	return df,plt

def yieldr(start_date='1995-01-01', end_date=datetime.datetime.today().strftime('%Y-%m-%d')):
	df = pd.DataFrame()
	df['13 Week'] = pd.to_numeric(pdr.get_data_yahoo(symbols='^IRX', start=start_date, end=end_date)['Close'], downcast='float')
	df['5 Year'] = pd.to_numeric(pdr.get_data_yahoo(symbols='^FVX', start=start_date, end=end_date)['Close'], downcast='float')
	df['10 Year'] = pd.to_numeric(pdr.get_data_yahoo(symbols='^TNX', start=start_date, end=end_date)['Close'], downcast='float')
	df['30 Year'] = pd.to_numeric(pdr.get_data_yahoo(symbols='^TYX', start=start_date, end=end_date)['Close'], downcast='float')

	fig, ax = plt.subplots()
	
	fig1 = df['13 Week'].plot(color='red')
	fig2 = df['5 Year'].plot(color='orange')
	fig3 = df['10 Year'].plot(color='yellow')
	fig4= df['30 Year'].plot(color='green')

	plt.legend()
	
	years = mdates.YearLocator()   # every year
	months = mdates.MonthLocator()  # every month
	yearsFmt = mdates.DateFormatter('%Y')
	# Set xaxis tick format
	ax.xaxis.set_major_locator(years)
	ax.xaxis.set_major_formatter(yearsFmt)
	ax.xaxis.set_minor_locator(months)
	ax.grid(True)

	fig.set_size_inches(16, 9)
	fig.tight_layout()

	return df, plt

if __name__ == "__main__":
	#	13 week '^IRX',
	#	5 Year  '^FVX',
	#	10 year '^TNX',
	#	30 year '^TYX'
	
	df, plt = plot_spread(tickers=['^FVX','^TYX'])
	print df.tail(10)
	plt.show()

	#df, plt = yieldr()
	#print df.tail()
	#plt.show()