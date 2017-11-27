from __future__ import print_function
from datetime import datetime, date
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import pandas as pd
pd.options.display.width = 640
import quandl
from config import *
quandl.ApiConfig.api_key = q_key # Put API Quandl key here

start_date_default = date(1995, 01, 01)
end_date_default = date.today().strftime('%Y-%m-%d')

def df_margin_debt():
	df = quandl.get("NYXDATA/MARKET_CREDIT")
	return df

def md_plt(df, title):
	fig, ax = plt.subplots()
	ax.grid(True)
	colors = ['red', 'green', 'blue']
	for i, col in enumerate(df.columns.values):
		df[col].plot(color=colors[i])
	plt.title(title)
	plt.legend()
	fig.autofmt_xdate()
	fig.set_size_inches(16, 9)
	fig.tight_layout()
	return plt

def calc_yoy(d, s):
	return ( ( d[s] - d[s].shift(12) ) / d[s].shift(12) ).fillna(0)

def margin_debt_all(start_date = start_date_default, end_date = end_date_default):
	df = df_margin_debt()
	# Trim df to date parameters
	df = df.loc[start_date:end_date]
	plt = md_plt(df, 'All NYSE Balances')
	return df, plt

def margin_debt_yoy(start_date = start_date_default, end_date = end_date_default):
	df = df_margin_debt()
	for i, col in enumerate(df.columns.values):
		df[col + ' YoY'] = calc_yoy(df, col)
	# Remove unneeded columns 
	df.drop(df.columns[[0,1,2]], axis=1, inplace=True)
	# Trim df to date parameters
	df = df.loc[start_date:end_date]
	plt = md_plt(df, 'Year-Over-Year Growth of NYSE Balances')
	return df, plt

def margin_debt_net(start_date = start_date_default, end_date = end_date_default):
	df = df_margin_debt()
	# Subtract margin debt from free credit cash and credit balance
	df['Net Balance'] = (df[df.columns[1]].fillna(0) + df[df.columns[2]].fillna(0) - df[df.columns[0]].fillna(0)).astype(float)
	# Remove unneeded columns 
	df.drop(df.columns[[0,1,2]], axis=1, inplace=True)
	# Trim df to date parameters
	df = df.loc[start_date:end_date]
	plt = md_plt(df, 'Net Account Balances')
	return df, plt


if __name__ == "__main__":
	df, plt = margin_debt_net()
	plt.show()