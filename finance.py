from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.options.display.width = 640
plt.style.use('ggplot')

import  aws_funcs.plt_to_s3 as aws
from fin_funcs.candlestick import candlstkr, candlstkr_ratio
from fin_funcs.correlationify import correlationify
from fin_funcs.dji_oil import dji_oil
from fin_funcs.margin_debt import margin_debt_all, margin_debt_yoy, margin_debt_net
from fin_funcs.plot_spread import plot_spread, yieldr

candls = [
		['^IXIC', 'candls_NASDAQ'], 
		['^GSPC', 'candls_SP500'],
		['^DJI', 'candls_DJI'],
		['^TYX', 'candls_30yr'],
		['^RUT', 'candls_Russel2000'],
		['AMZN', 'candls_AMZN'],
		['FB', 'candls_FB'],
		['GOOGL', 'candls_GOOGL'],
		['MSFT', 'candls_MSFT'],
		['NFLX', 'candls_NFLX'],
		['NVDA', 'candls_NVDA'],
		['SMH', 'candls_SMH']
	]

ratios = [
		['IVW','IVE', 'candlr_Growth_to_Value', 'S&P Growth to Value (IVW:IVE)'], # S&P Growth to Value
		['DBC','SPY', 'candlr_Commodities_to_SP500', 'Commodities to S&P500 (DBC:SPY)'], # Commodities to S&P
		['GLD', 'SPY', 'candlr_Gold_to_SP500', 'Gold to S&P500 (GLD:SPY)'], # Russia to S&P500
		['RSX', 'SPY', 'candlr_Russia_to_SP500'], # Russia to S&P500
		['TLT', 'SPY', 'candlr_Treasuries_to_SP500'],
		['XLY', 'XLP', 'candlr_Consumer_Discretionary_to_Staples', 'Consumer Discretionary to Consumer Staples (XLY:XLP)']
	]

spreads = [
		['^IRX','^FVX', 'tspread_00-10'],
		['^IRX','^TNX', 'tspread_00-10'],
		['^IRX','^TYX', 'tspread_00-30'],
		['^FVX','^TNX', 'tspread_05-10'],
		['^FVX','^TYX', 'tspread_05-30'],
		['^TNX','^TYX', 'tspread_10-30']
	]

def make_candls(d):
	for i in d:
		df, plt = candlstkr(tick=i[0])
		aws.upload_plt(plt, i[1] + '.png', save_local=True)

def make_candls_ratios(d):
	for i in d:
		try:
			df, plt = candlstkr_ratio(tickers=i[0:2], title=i[3])
			aws.upload_plt(plt, i[2] + '.png', save_local=True)
		except IndexError:
			df, plt = candlstkr_ratio(tickers=i[0:2])
			aws.upload_plt(plt, i[2] + '.png', save_local=True)

def make_plot_spreads(d):
	for i in d:
		df, plt = plot_spread(tickers=i[0:2], start_date='1990-01-01')
		aws.upload_plt(plt, i[2] + '.png', save_local=True)
	# Make chart with all yields showing
	df, plt = yieldr()
	aws.upload_plt(plt, 'tyields.png', save_local=True)

def make_dji_oil():
	df_oil,oil_plt = dji_oil()
	aws.upload_plt(oil_plt, 'dji_oil.png', save_local=True)

def make_corr():
	df_corr, corr_plt = correlationify()
	aws.upload_plt(corr_plt, 'corr_sp500_10yr.png', save_local=True)

def make_margin_debt():
	df, plt = margin_debt_all()
	aws.upload_plt(plt, 'md_bal_all.png', save_local=True)
	df, plt = margin_debt_yoy()
	aws.upload_plt(plt, 'md_bal_yoy.png', save_local=True)
	df, plt = margin_debt_net()
	aws.upload_plt(plt, 'md_bal_net.png', save_local=True)

def update_charts():
	make_candls(candls)
	make_candls_ratios(ratios)
	make_plot_spreads(spreads)
	make_dji_oil()
	make_corr()
	make_margin_debt()


if __name__ == "__main__":
	#  Inputs
	#   tick, start_date, end_date, freq
	#df, plt = candlstkr(tick='USO', start_date='2007-01-01')
	#df, plt = candlstkr(tick='DBC', start_date='2007-01-01')

	#  Inputs
	#   tickers=['A','B'], start_date, end_date, freq
	#df_candl_ratio, plt = candlstkr_ratio(tickers=['GSG','SPY'])
	#df_candl_ratio, plt = candlstkr_ratio(tickers=['SPY','RSP'])  # S&P to S&P Equal wt
	
	#  Inputs
	#   tickers=['A','B'], start_date, end_date
	#   freq, rolling_corr, threshold
	#df_corr, plt = correlationify()

	#  Inputs
	#   tickers=['A','B'], start_date, end_date
	#df_spread, plt = plot_spread(tickers=['^IRX','^TNX'], start_date='1990-01-01')
	#print(df_spread.tail(3))
	#df_spread, plt = plot_spread(tickers=['^FVX','^TYX'], start_date='2018-01-01')
	#print(df_spread.tail(10))
	#df_spread, plt = plot_spread(tickers=['^TNX','^TYX'], start_date='2018-01-01')
	#print(df_spread.tail(10))
	
	#plt.show(), plt.clf()
	make_margin_debt()
	#update_charts()