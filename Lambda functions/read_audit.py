import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    #Hardcoded bucket name and json file names'audit.json'
    bucket_name = 'maxbucketcw'
    file_name = 'audit.json'
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    file_content = response['Body'].read().decode('utf-8')
    data = json.loads(file_content)
    return {
        'statusCode': 200,
        'body': json.dumps(data, indent=4)
    }
