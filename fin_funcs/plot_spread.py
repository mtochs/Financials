import datetime
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import pandas_datareader as pdr
plt.style.use('ggplot')


def plot_spread(tickers=['^IRX','^TYX'], start_date='1995-01-01',
		end_date=datetime.datetime.today().strftime('%Y-%m-%d')):
	df = pd.DataFrame(data=None, columns=['A', 'B', 'diff'])
	df.B = pd.to_numeric(pdr.get_data_yahoo(symbols=tickers[1], start=start_date, end=end_date)['Close'], downcast='float')
	df.A = pd.to_numeric(pdr.get_data_yahoo(symbols=tickers[0], start=start_date, end=end_date)['Close'], downcast='float')
	df['diff'] = df['B'].subtract(df['A'])
	# Last data point	
	last = df.iloc[-1]['diff']

	fig, ax = plt.subplots()
	df['diff'].plot(color='#5687d4')
	# Horizontal line at last data point
	plt.axhline(y=last, color='#d62728')
	fig.set_size_inches(16, 9)
	fig.tight_layout()
	return df,plt

if __name__ == "__main__":
	#	13 week '^IRX',
	#	5 Year  '^FVX',
	#	10 year '^TNX',
	#	30 year '^TYX'
	
	df, plt = plot_spread(tickers=['^FVX','^TYX'])
	plt.show()