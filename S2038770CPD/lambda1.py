import boto3
import json

# // TODO: Find out what the SQS contains 
# // TODO: extract entities in the Lambda function
# TODO: Store the entities in a DynamoDB test_table and run them through AWS Rekognition

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the DynamoDB table name
table_name = 'test_table'

def lambda_handler(event, context):
    """Extracts message body from SQS event and stores it in DynamoDB table.
    
    :param event: SQS event containing message body
    :param context: Lambda context object
    :return: Response indicating success or failure
    """
    try:
        # Extract message body from the SQS event
        for record in event['Records']:
            message_body = json.loads(record['body'])
            image_bucket = message_body['Records'][0]['s3']['bucket']['name']
            image_key = message_body['Records'][0]['s3']['object']['key']
            eventName = message_body['Records'][0]['eventName']
            eventTime = message_body['Records'][0]['eventTime']
            sourceIP = message_body['Records'][0]['requestParameters']['sourceIPAddress']

            # Generate a unique ID based on current timestamp
            id_timestamp = str(int(time.time()))

            # Prepare item for DynamoDB
            dynamo_item = {
                'id': {'S': id_timestamp},
                'image_bucket': {'S': image_bucket},
                'image_key': {'S': image_key},
                'eventName': {'S': eventName},
                'eventTime': {'S': eventTime},
                'sourceIP': {'S': sourceIP},
            }

            # Put item into DynamoDB table
            dynamodb.put_item(TableName=table_name, Item=dynamo_item)

            print(f'Successfully added item: {image_key} to DynamoDB table: {table_name}')

        return {
            'statusCode': 200,
            'body': json.dumps('Items added to DynamoDB table successfully')
        }
    except Exception as e:
        print(f'Error adding items to DynamoDB table: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to add items to DynamoDB table')
        }
