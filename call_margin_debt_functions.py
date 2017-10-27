from margin_debt_s3 import update_margin_debt_s3 
#import pandas as pd


df = update_margin_debt_s3()

print df.tail()
#print df[ (df['Margin debt YoY'] >= .4) & (df['Date'] >= '2009-01-01')]
#print df[-12:-11]['Margin debt'] * 1.4