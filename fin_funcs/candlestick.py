import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.data as web
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
plt.style.use('ggplot')
pd.option_context('display.max_rows', None, 'display.max_columns', 3)

def candl_plt(df_resamp, title, bar_width):
	fig, ax = plt.subplots()
	ax.set_title(title)
	# Code from https://ntguardian.wordpress.com/2016/09/19/introduction-stock-market-data-python-1/
	candlestick_ohlc(ax, list(zip(list(mdates.date2num(df_resamp.index.tolist())),
		df_resamp["Open"].tolist(), df_resamp["High"].tolist(),
		df_resamp["Low"].tolist(), df_resamp["Close"].tolist())),
		colorup="green", colordown="red", width=bar_width)
	
	# **************** Formatting graph parameters ****************
	# Source: https://matplotlib.org/devdocs/gallery/api/date.html
	years = mdates.YearLocator()   # every year
	months = mdates.MonthLocator()  # every month
	yearsFmt = mdates.DateFormatter('%Y')
	# Set xlim min and max with 1 month offset in each direction for asthetics
	xlim_min = df_resamp.index.min() - relativedelta(months=+1)
	xlim_max = df_resamp.index.max() + relativedelta(months=+1)
	ax.set_xlim([xlim_min, xlim_max])
	# Set xaxis tick format
	ax.xaxis.set_major_locator(years)
	ax.xaxis.set_major_formatter(yearsFmt)
	ax.xaxis.set_minor_locator(months)
	# *************************************************************
	ax.grid(True)
	fig.set_size_inches(16, 9)
	fig.autofmt_xdate()
	fig.tight_layout()
	return plt

def candlstkr(tick='^GSPC', start_date='1995-01-01',
		end_date=datetime.datetime.today().strftime('%Y-%m-%d'), freq='M'):
	if freq == 'M':
		bar_width = 20
	elif freq == 'W':
		bar_width = 0.6

	df = web.DataReader(tick, 'yahoo', start_date, end_date)
	df = df.drop(['Adj Close', 'Volume'], axis=1)
	df_resamp = pd.DataFrame(data=None, columns=df.columns)
	
	df_resamp.Open = df.Open.resample(freq).first()
	df_resamp.High = df.High.resample(freq).max()
	df_resamp.Low = df.Low.resample(freq).min()
	df_resamp.Close = df.Close.resample(freq).last()
	df_resampe = df_resamp.dropna()

	# Update start_date for plt publishing
	start_date = df_resamp.index.min().strftime('%m/%d/%y')

	candl_title = tick + ' from ' + start_date + ' to ' + end_date
	plt = candl_plt(df_resamp, candl_title, bar_width)
	return df_resamp, plt

def candlstkr_ratio(tickers=['^GSPC', '^TYX'], start_date='1995-01-01',
		end_date=datetime.datetime.today().strftime('%Y-%m-%d'), freq='M'):
	if freq == 'M':
		bar_width = 20
	elif freq == 'W':
		bar_width = 1

	df_A = web.DataReader(tickers[0], 'yahoo', start_date, end_date)
	df_B = web.DataReader(tickers[1], 'yahoo', start_date, end_date)
	df_A = df_A.drop(['Adj Close', 'Volume'], axis=1)
	df_B = df_B.drop(['Adj Close', 'Volume'], axis=1)

	df_resamp = pd.DataFrame(data=None, columns=df_A.columns)
	df_resamp.Open = df_A.Open.resample(freq).first() / df_B.Open.resample(freq).first()
	df_resamp.High = df_A.High.resample(freq).max() / df_B.Open.resample(freq).max()
	df_resamp.Low = df_A.Low.resample(freq).min() / df_B.Low.resample(freq).min()
	df_resamp.Close = df_A.Close.resample(freq).last() / df_B.Close.resample(freq).last()
	df_resamp = df_resamp.dropna()

	# Update start_date for plt publishing
	start_date = df_resamp.index.min().strftime('%m/%d/%y')

	candl_title = tickers[0] + ' to ' + tickers[1] + ' ratio from ' + start_date + ' to ' + end_date
	plt = candl_plt(df_resamp, candl_title, bar_width)
	return df_resamp, plt

