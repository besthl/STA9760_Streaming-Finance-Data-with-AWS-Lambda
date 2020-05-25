import json
import boto3
import os
import subprocess
import sys

subprocess.check_call([sys.executable, "-m", "pip", "install", "--target", "/tmp", 'yfinance'])
sys.path.append('/tmp')
import yfinance as yf

# chose the stock we'd like to know
CHOICES = ["FB","SHOP","BYND","NFLX","PINS","SQ","TTD","OKTA","SNAP","DDOG"]

# define lambda handler function
def lambda_handler(event, context):
     # initialize boto3 client
    fh = boto3.client("firehose", "us-east-2")
    
    # get data using yfinance
    for j in range(0,len(CHOICES)):
        df = yf.download(CHOICES[j], start="2020-05-14", end="2020-05-15",interval='1m')
        output = []
        
        # load data as dictionary
        for i in range(0,len(df)):
            data = {"High":df['High'][i],"Low":df['Low'][i],"ts":df.index[i].strftime('%m/%d/%Y %X'),"name":CHOICES[j]}
    
             # convert it to JSON -- IMPORTANT!!
            as_jsonstr = json.dumps(data)
    
            # this actually pushed to our firehose datastream
             # we must "encode" in order to convert it into the
             # bytes datatype as all of AWS libs operate over
             # bytes not strings
            
            temp = {'Data': as_jsonstr.encode('utf-8')}
        
            #append each row into output data set
            output.append(temp)
    
        #put data into S3 using delivery stream "yfinance"
        fh.put_record_batch(
            DeliveryStreamName="yfinance", 
            Records= output
            )

    # return
    return {
        'statusCode': 200,
        'body': json.dumps(f'Done! Recorded: {as_jsonstr}')
    }