from __future__ import print_function
import filecmp, io, os, urllib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import boto3, botocore # AWS libraries
pd.options.display.width = 640
plt.style.use('ggplot')

factbook_web = 'factbook.xls'
factbook_s3 = 'factbook_s3.xls'
cols = ['Date', 'Margin debt', 'Free credit cash accounts', 'Credit balances in margin accounts', 'Account balance', 'Margin debt YoY', 'Free credit cash YoY', 'Credit balances YoY', 'Account balance YoY']

# Variables for AWS
BUCKET_NAME = 'mtochs-finance' # replace with your bucket name
MARGIN_DEBT_DIR = 'margin_debt'
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)
client = boto3.client('s3')


def delete_file(f):
	try:
		os.remove(f)
		print("Removed file:", f)
	except OSError:
		pass

def grab_factbook(all=True):
	if (all == True):
		dls = "http://www.nyxdata.com/nysedata/asp/factbook/table_export_csv.asp?mode=tables&key=50"
	else:
		dls = "http://www.nyxdata.com/nysedata/asp/factbook/table_export_csv.asp?mode=table&key=3153"
	urllib.urlretrieve(dls, factbook_web)	

def add_margin_debt_dir(x):
	return '{}/{}'.format(MARGIN_DEBT_DIR, x)

def purge_files():
	delete_file(factbook_web)
	delete_file(factbook_s3)

def compare_factbooks():
	purge_files()
	# Download new copy of factbook
	grab_factbook()
	factbook_s3_w_dir = add_margin_debt_dir(factbook_web)
	s3.Bucket(BUCKET_NAME).download_file(factbook_s3_w_dir, factbook_s3)
	return filecmp.cmp(factbook_web, factbook_s3)

def calc_yoy(d, s):
	return ( ( d[s] - d[s].shift(12) ) / d[s].shift(12) ).fillna(0)
def change_date(row):
	return row['Date'][3:] + "-" + row['Date'][:2]

def prep_data():
	df = pd.read_csv(factbook_web, sep='\t', skiprows=3).fillna(0)
	# Remove data with empty data
	df = df[df['Margin debt'] != 0]
	# Change column names
	df.columns = cols[0:4]
	# Change date format from mm/YYYY to YYYY-mm
	df['Date'] = pd.to_datetime( df.apply(change_date, axis=1) )
	# Convert all currencies to integers
	df[df.columns[1:]] = df[df.columns[1:]].replace('[\$,]', '', regex=True).astype(int)
	# Create 'Account balance' data
	df[cols[4]] = (df[cols[2]] + df[cols[3]] - df[cols[1]]).astype(int)
	# Add year-over-year change for financials
	df[cols[5]] = calc_yoy(df, cols[1])
	df[cols[6]] = calc_yoy(df, cols[2])
	df[cols[7]] = calc_yoy(df, cols[3])
	df[cols[8]] = calc_yoy(df, cols[4])
	return df

def plot_line(df, s):
	return plt.plot(df.Date, df[s], label=s)

def md_graph(df, lines, file_key, title, from_date='1998-01-01'):
	df_t = df[df.Date >= from_date].copy()
	for l in lines:
		plot_line(df_t, l)

	plt.legend()
	plt.title(title)
	
	# Save plots to S3
	img_data = io.BytesIO()
	plt.savefig(img_data, format='png')
	img_data.seek(0)
	
	file_key_w_dir = add_margin_debt_dir(file_key)
	# Delete png
	client.delete_object(Bucket=BUCKET_NAME, Key=file_key_w_dir)
	# Upload new image
	bucket.put_object(Body=img_data, ContentType='image/png', Key=file_key_w_dir)
	print("New png uploaded", file_key)
	# Clear plt
	plt.clf()

def update_graphs(df):
	md_graph(df, cols[1:4], 'md_balances.png', 'Account Sizes') # Graph balance data
	md_graph(df, cols[5:8], 'md_yoy.png', 'Year-over-Year Changes') # Graph YoY data
	md_graph(df, [cols[4]], 'md_account_bal.png', 'Outstanding Account Balances') # Account balance
	#md_graph(df, [cols[8]]) # Account balance YoY

def update_factbook_s3():
	# Delete existing file
	fb_s3_key = add_margin_debt_dir(factbook_web)
	client.delete_object(Bucket=BUCKET_NAME, Key=fb_s3_key)
	# Upload new file
	data = open(factbook_web, 'rb')
	bucket.put_object(Body=data, Key=fb_s3_key)

def update_margin_debt_s3():
	# Download from web and s3 then compare file size
	comparison = compare_factbooks()
	# Parse data from factbook
	df = prep_data()
	# Check if file has been updated
	if comparison == False:
		print("Files are different.")
		update_graphs(df)
		# Upload new factbook
		update_factbook_s3()
	else:
		print("No update needed.")
	# Delete both factbooks
	purge_files()
	return df


if __name__ == "__main__":
	df = update_margin_debt_s3()

#print df[ (df['Margin debt YoY'] >= .4) & (df['Date'] >= '2009-01-01')]
#print df[-12:-11]['Margin debt'] * 1.4