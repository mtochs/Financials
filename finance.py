from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.options.display.width = 640
plt.style.use('ggplot')

import  aws_funcs.plt_to_s3 as aws
from fin_funcs.candlestick import candlstkr, candlstkr_ratio
from fin_funcs.correlationify import correlationify
from fin_funcs.margin_debt import update_margin_debt_s3 
from fin_funcs.plot_spread import plot_spread

candls = [
		['^IXIC', 'candls_NASDAQ'], 
		['^GSPC', 'candls_SP500'],
		['^DJI', 'candls_DJI'],
		['^TYX', 'candls_30yr'],
		['^RUT', 'candls_Russel2000']
	]

ratios = [
		['IVW','IVE', 'candlr_Growth_to_Value'], # S&P Growth to Value
		['RSX', 'SPY', 'candlr_Russia_to_SP500'], # Russia to S&P500
		['DBC','SPY', 'candlr_Commodities_to_SP500'], # Commodities to S&P
		['TLT', 'SPY', 'candlr_Treasuries_to_SP500']
	]

spreads = [
		['^FVX','^TYX', 'tspread_05-30.png'],
		['^TNX','^TYX', 'tspread_10-30.png'],
		['^IRX','^TNX', 'tspread_00-10.png']
	]

def make_candls(d):
	for i in d:
		df, plt = candlstkr(tick=i[0])
		aws.upload_plt(plt, i[1] + '.png')

def make_candls_ratios(d):
	for i in d:
		df, plt = candlstkr_ratio(tickers=i[0:2])
		aws.upload_plt(plt, i[2] + '.png')

def make_plot_spreads(d):
	for i in d:
		df, plt = plot_spread(tickers=i[0:2], start_date='1990-01-01')
		aws.upload_plt(plt, i[2] + '.png')

if __name__ == "__main__":
	make_candls(candls)
	make_candls_ratios(ratios)
	make_plot_spreads(spreads)

	#  Inputs
	#   tick, start_date, end_date, freq
	#df, plt = candlstkr(tick='XLP', freq='W')
	#plt.show()

	#  Inputs
	#   tickers=['A','B'], start_date, end_date, freq
	#df_candl_ratio, plt = candlstkr_ratio(tickers=['SPY', 'TLT'])
	#plt.show(), plt.clf()
	
	#  Inputs
	#   tickers=['A','B'], start_date, end_date
	#   freq, rolling_corr, threshold
	#df_corr, plt = correlationify()
	#plt.show(), plt.clf()

	#  Inputs
	#   tickers=['A','B'], start_date, end_date
	#df_spread, plt = plot_spread()
	#plt.show(), plt.clf()

	#df = update_margin_debt_s3()