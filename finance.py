from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.options.display.width = 640
plt.style.use('ggplot')

import aws_funcs.plt_to_s3
from fin_funcs.candlestick import candlstkr, candlstkr_ratio
from fin_funcs.correlationify import correlationify
from fin_funcs.plot_spread import plot_spread


if __name__ == "__main__":
	#  Inputs
	#   tick, start_date, end_date, freq
	df_candl, plt = candlstkr(tick='RSX')
	#print(df_candl.head())
	plt.show()
	#plt.clf()

	#  Inputs
	#   tickers=['A','B'], start_date, end_date, freq
	#df_candl_ratio, plt = candlstkr_ratio(tickers=['TLT','SPY'], freq='W')
	#plt.show()
	#plt.clf()

	#  Inputs
	#   tickers=['A','B'], start_date, end_date
	#   freq, rolling_corr, threshold
	#df_corr, plt = correlationify()
	#plt.show()
	#plt.clf()

	#  Inputs
	#   tickers=['A','B'], start_date, end_date
	#df_spread, plt = plot_spread()
	#plt.show()