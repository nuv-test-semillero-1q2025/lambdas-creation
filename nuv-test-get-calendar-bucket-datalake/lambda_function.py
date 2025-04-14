import json
import boto3
from urllib.parse import unquote_plus

# Initialize the S3 client to interact with S3
s3 = boto3.client('s3')

source_bucket = 'nuv-prod-calendars-datalake'  # Bucket in Account Nuvu 10
destination_bucket = 'nuv-test-calendar-datalake'  # Bucket in Account Universidad Nacional

def lambda_handler(event, context):

    for record in event['Records']:
        # Extract the object key (file name)
        bucket_name = unquote_plus(record['s3']['bucket']['name'])
        object_key = unquote_plus(record['s3']['object']['key'])

        URI = f"s3://{bucket_name}/{object_key}"

        # check the procedence of the file - confirm the authorize file name to copy
        # Check if the object key contains "AREO_Data in its name"
        if "AREO_Data" in URI.split('/')[4]:
        
            try:
                # Copy the object from the source bucket in Account A to the destination bucket in Account B
                copy_source = {'Bucket': source_bucket, 'Key': object_key}
                s3.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=object_key)

                print(f"Successfully copied {object_key} from {source_bucket} to {destination_bucket}")

            except Exception as e:
                print(f"Error copying {object_key}: {str(e)}")
                raise e
        else: 
            print(f"Skipping file {object_key} as it does not match the criteria.")

    return {
        'statusCode': 200,
        'body': json.dumps('File copy operation completed.')
    }