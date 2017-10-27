from __future__ import print_function
import filecmp, io, os, urllib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd
import boto3, botocore # AWS libraries
pd.options.display.width = 640
plt.style.use('ggplot')

# Variables for AWS
BUCKET_NAME = 'mtochs-finance' # replace with your bucket name
MARGIN_DEBT_DIR = 'margin_debt'
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)
client = boto3.client('s3')

def plt_to_s3(plt, bucket=BUCKET_NAME, dir=''):
	
	return 0