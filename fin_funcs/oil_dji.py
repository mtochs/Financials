from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import pandas_datareader as pdr
import pandas_datareader.data as web
plt.style.use('ggplot')

def dji_oil(freq='M', oil_shift=10, start_date = '1980-01-01', 
		end_date = datetime.today().strftime('%Y-%m-%d')):
	
	# change start_date to datetime format
	start_date = datetime.strptime(start_date, "%Y-%m-%d")

	# if an end_date is manually entered change it to datetime format
	if end_date != datetime.today().strftime('%Y-%m-%d'):
		end_date = datetime.strptime(end_date, "%Y-%m-%d")

	start_date_oil = start_date - timedelta(days=365*10)
	
	# Collect daily oil data from St Louis Fed
	df = web.DataReader("DCOILWTICO", "fred", start_date_oil, end_date)
	df.columns = ['oil']

	# shift oil data forward 10 years
	df.index = df.index + timedelta(days=365*oil_shift) # phase shift oil 10 years forward
		
	df['dji'] = pdr.get_data_yahoo(symbols='^DJI', start=start_date, end=end_date)['Close']

	# Resample data to reduce static
	df = df.resample(freq).mean()

	# Cap df at end_date parameter
	if end_date != datetime.today().strftime('%Y-%m-%d'):
		df = df[df.index < end_date]
	# Collect min, max for chart
	x_min, x_max = df.index.min(), df.index.max()

	# Create plot
	fig, ax = plt.subplots()
	ax2 = ax.twinx()

	# Use log scaling for both data sets
	fig1 = df['oil'].plot(ax=ax, color='black').set_yscale('log')
	fig2 = df['dji'].plot(ax=ax2, color='blue', secondary_y=True).set_yscale('log')

	# **************** Formatting graph parameters ****************
	ax.grid(True)
	fig.autofmt_xdate()
	ax.set_title('Oil (10 Year Forward Shift) and DJI')
	plt.xlim(xmin=x_min, xmax=x_max)
	fig.set_size_inches(16, 9)
	fig.tight_layout()

	return df, plt


if __name__ == "__main__":
	df, plt = dji_oil()
	plt.show()
