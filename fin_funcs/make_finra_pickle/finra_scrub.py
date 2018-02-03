from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
pd.options.display.width = 640
import requests

pickle_file = 'finra_margin.pkl'

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
	# Set columns as float
	#df_finra_update = df_finra_update.astype(float)
	# Drop all empty data rows
	df_finra_update = df_finra_update[np.isfinite(df_finra_update)]
	return df_finra_update

def update_margin():
	df = pd.read_pickle(pickle_file) 
	df_finra_update = finra_tables()
	df.update(df_finra_update)
	df.to_pickle(pickle_file)
	print df.head()


def make_pickle():
	df = pd.read_csv('finra_margin.csv')
	df['Date'] = pd.to_datetime(df['Date'], format="%m/%d/%Y")
	df = df.set_index('Date')
	df = df.astype(float)
	print df.head()
	df.to_pickle(pickle_file)

if __name__ == "__main__":
	update_margin()


	'''
	from tabulate import tabulate
	for table in tables:
		df = pd.read_html(str(table))
		#df.columns = ['Date','Margin Debt', 'Free Credit in Cash Accounts', 'Free Credit in Margin Accounts']
		print( tabulate(df[0], headers='keys', tablefmt='psql') )
	'''