import boto3
import os

s3 = boto3.client('s3')

Direc= "/Users/aravindbalakrishnan/Downloads/test"
files = os.listdir(Direc)
files = [f for f in files if os.path.isfile(Direc+'/'+f)] 
fileid=0;
for x in files:
    s3.upload_file(
        Filename=Direc+"//"+x,
        Bucket="intelligent-driver-safety-system-s3-bucket",
        Key="screenshot-test"+x,
    )


print('Files Uploaded')