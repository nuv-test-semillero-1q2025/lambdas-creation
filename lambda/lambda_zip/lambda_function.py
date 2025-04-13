import json

def lambda_handler(event, context):
    print(event)
    print("Hola mundo!")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

