import json
import boto3

glue_client = boto3.client('glue')

def lambda_handler(event, context):
    
    # Extract bucket name and file path from S3 event
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        URI = f"s3://{bucket_name}/{object_key}"

        # Check if the object key contains "AREO_Data" in its name - this is the condition to trigger the Glue job
        if "AREO_Data" in URI.split('/')[4]:

            # Start AWS Glue Job
            response = glue_client.start_job_run(
                JobName="nuv-test-from-csv-to-parket",
                Arguments={
                    "--SOURCE_S3_PATH": f"s3://{bucket_name}/{object_key}"
                }
            )
            
            print(f"Started Glue Job: {response['JobRunId']}")
            print(f"Glue Job ARN: {response['JobRunId']}")
            # Log the file to be handled
            print(f'File to be handle: s3://{bucket_name}/{object_key}')

        else:

            # If the file does not match the criteria, log it and return a message
            # Log the file that does not match the criteria
            print(f'File {URI} not apply for the glue job')
            return {
                'statusCode': 200,
                'body': json.dumps('File not in the correct folder')
            }
        
    return {
        'statusCode': 200,
        'body': json.dumps('Glue job triggered successfully')
    }
