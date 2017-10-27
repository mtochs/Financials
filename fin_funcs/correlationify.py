import datetime
import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.data as web
import numpy as np

import matplotlib.pyplot as plt
plt.style.use('ggplot')


def corr_data(tickers, start_date, end_date, freq, rolling_corr):
	df = pd.DataFrame(data=None, columns=['A', 'B'])
	#df['TY'] = pdr.get_data_yahoo(symbols=tickers[0], start=start_date, end=end_date)['Adj Close']
	#df['SP500'] = pdr.get_data_yahoo(symbols=tickers[1], start=start_date, end=end_date)['Adj Close']
	df.A = web.DataReader(tickers[0], 'yahoo', start_date, end_date)['Close']
	df.B = web.DataReader(tickers[1], 'yahoo', start_date, end_date)['Close']
	df.dropna()
	df_r = df.resample('W').mean()
	df_r['Corr'] = df_r.A.rolling(window=rolling_corr).corr(df_r.B)
	df_r.dropna()
	return df_r

def correlationify(tickers = ['^TNX', '^GSPC'], start_date = '1998-01-01',
		end_date = datetime.datetime.today().strftime('%Y-%m-%d'),
		freq='W', rolling_corr = 40, threshold=-0.65):
	
	df = corr_data(tickers, start_date, end_date, freq, rolling_corr)

	fig, axes = plt.subplots(nrows=2, ncols=1)
	fig1 = df.A.plot(ax=axes[0]).set_xlim([start_date, end_date])
	fig1 = df.B.plot(ax=axes[0], secondary_y=True)#.invert_yaxis()
	fig2 = df.Corr.plot(ax=axes[1]).set_xlim([start_date, end_date])

	for i, row in df[df.Corr < threshold].iterrows():
		plt.axvline(x=i, color='#79c879', alpha=0.2)
		
	fig.set_size_inches(16, 9)
	fig.tight_layout()
	return df, plt


if __name__ == "__main__":
	df, plt = correlationify()
	#print df[df.Corr < -.75]
	plt.show()