from __future__ import print_function
import filecmp, io, os, urllib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import boto3, botocore # AWS libraries
pd.options.display.width = 640
plt.style.use('ggplot')
plt.figure(num=None, figsize=(16, 9), dpi=80, facecolor='w', edgecolor='k')

# Variables for AWS
BUCKET_NAME = 'mtochs-finance' # replace with your bucket name
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)
client = boto3.client('s3')

def bucket_file_exists(file_key):
	exists = False
	try:
	    s3.Object(BUCKET_NAME, file_key).load()
	except botocore.exceptions.ClientError as e:
	    if e.response['Error']['Code'] == "404":
	        exists = False
	    else:
	        raise
	else:
	    exists = True
	return exists

def upload_plt(plt, file_key, save_local=False):
	# Convert plt to bin for upload to S3
	img_data = io.BytesIO()
	plt.savefig(img_data, format='png')
	img_data.seek(0)
	
	if bucket_file_exists(file_key) == True:
		# Delete file_key if it exists
		client.delete_object(Bucket=BUCKET_NAME, Key=file_key)

	# Upload new image
	bucket.put_object(Body=img_data, ContentType='image/png', Key=file_key)
	print("New plt uploaded: ", file_key)
	# Clear plt
	if save_local == True: 
		plt.savefig(file_key)
		print("Plt saved locally: ", file_key)
	plt.clf(), plt.close('all')


#print(bucket_file_exists(BUCKET_NAME, 'margin_debt/md_balances.png'))