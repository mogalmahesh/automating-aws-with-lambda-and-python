import boto3
import os
import csv


def lambda_handler(event, context):
    # Run this command if you are running it on local machine. Replace profile name.
    # boto3.setup_default_session(profile_name='admin-analyticshut')
    
    dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
    table = dynamodb.Table('dev-users')
    s3 = boto3.client('s3')

    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    download_path = os.path.join('/tmp/',  key)
    # download_path = 'users_data.csv'
    s3.download_file(source_bucket, key, download_path)

    items = []
    with open(download_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            items.append(row)

    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)


