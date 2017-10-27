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
	df.B = pdr.get_data_yahoo(symbols=tickers[1], start=start_date, end=end_date)['Close']
	df.A = pdr.get_data_yahoo(symbols=tickers[0], start=start_date, end=end_date)['Close']
	df.diff = df.B - df.A
	# Last data point	
	last = df.diff.iloc[-1]

	fig, ax = plt.subplots()
	df.diff.plot(color='#5687d4')
	# Horizontal line at last data point
	plt.axhline(y=last, color='#d62728')
	fig.tight_layout()
	return df,plt

if __name__ == "__main__":
	#	13 week '^IRX',
	#	5 Year  '^FVX',
	#	10 year '^TNX',
	#	30 year '^TYX'
	
	df, plt = plot_spread()
	plt.show()