from __future__ import print_function
from bs4 import BeautifulSoup
from datetime import datetime, date
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
import pandas as pd
pd.options.display.width = 640
import requests
import os


start_date_default = date(1997, 01, 01)
end_date_default = date.today().strftime('%Y-%m-%d')
dir_path = os.path.dirname(os.path.realpath(__file__))
pickle_file = dir_path + '\\finra_margin.pkl'

def finra_tables():
	# Collect tables from FINRA site using Beautiful Soup
	finra_req = requests.get("http://www.finra.org/investors/margin-statistics")
	soup = BeautifulSoup(finra_req.content,'lxml')
	tables = soup.find_all('table')

	# Get current and last year and remove last row (NaN row)
	df_current_year = pd.read_html(str(tables[0]))[0][:-1]
	df_previous_year = pd.read_html(str(tables[1]))[0][:-1]
	# Join both years into one dataframe
	df_finra_update = df_previous_year.append(df_current_year)
	# Update the column names to conform with the master df
	df_finra_update.columns = ['Date','Margin Debt', 'Free Credit in Cash Accounts', 'Free Credit in Margin Accounts']
	# Standardize June to conform to formatting
	df_finra_update = df_finra_update.replace({'June': 'Jun'}, regex=True)
	# Reformat Date column
	df_finra_update['Date'] = pd.to_datetime(df_finra_update.Date, format="%b-%y")#.strftime('%m/01/%Y')
	# Set 'Date' as index
	df_finra_update = df_finra_update.set_index('Date')
	# Drop all empty data rows
	df_finra_update = df_finra_update[np.isfinite(df_finra_update)]
	return df_finra_update

def df_margin_debt():
	df = pd.read_pickle(pickle_file) 
	df_finra_update = finra_tables()
	df.update(df_finra_update)
	df.to_pickle(pickle_file)
	return df

# Quandl function is obsolete in favor of FINRA scrubbing method
# NYSE no longer updates margin debt as of December 2017
'''
def df_margin_debt_quandl():
	import quandl
	from config import *
	quandl.ApiConfig.api_key = q_key # Put API Quandl key here
	df = quandl.get("NYXDATA/MARKET_CREDIT")
	df.loc[pd.to_datetime('2017-10-31')] = [561444., 139978., 151729.]
	df.loc[pd.to_datetime('2017-11-30')] = [580945., 140870., 153196.]
	return df
'''

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
	df, plt = margin_debt_yoy() #margin_debt_net() margin_debt_yoy() margin_debt_all()
	#print(df.tail())
	plt.show()