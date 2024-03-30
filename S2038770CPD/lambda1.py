import boto3
import json

# // TODO: Find out what the SQS contains 
# TODO: extract entities in the Lambda function
# TODO: Store the entities in a DynamoDB test_table and run them through AWS Rekognition

event = {'Records': [
    {'messageId': 'f515e061-555f-4d0a-8a67-0807d4dfa833', 
     'receiptHandle': 'AQEBf3QYg0TmSFJd5HBZdbzUcTG2E3zLHMA5kIdY47F5P6M2YjHEuRTG++z/wsje8XhXjp7JUxgKL3Z1+kxPlcTiESZojSxreZx0qkQ1ounpWSHXhpZ7TBreKW/So/ezlsudfZ0L7qpnHvy6WxDYBL3MAezNBf2NdzDP+fQ995vweiw1wfIYrR29A0bKaG0Z7LS5+tSBPEbZfpldJfYLz3wVGf55kKsdfV9Rdqk0r45B3XCzx8vDxLO/fde+gpmbcdbN7XSmPqtaE13uD+dgYE497f2avfx0TWXfpGDtVXGWDjRDvdpyLAC22f6ohhKWPtENE+8Tqw55hLJOskCgPrdWQ36uWxv0Ctjg+6hBsvUrcysi8bKp/i1wCE1TF672mvpZiKwoIsaT7tJNyqiNUQDXaA==', 
     
     'body': '{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"us-east-1","eventTime":"2024-03-30T18:59:47.899Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"AWS:AROAXRV4O6ILBWVXIUVVX:i-0a4396d900b746df6"},"requestParameters":{"sourceIPAddress":"34.227.151.244"},"responseElements":{"x-amz-request-id":"269CZ0RBW38RCGSS","x-amz-id-2":"Ou5LA6PpMc0Ai/OhqHGgAWlndCjC0A7A3+jUGJVpLXxMcOAPRkdnuyDJig6Xd/UHeN6kmJfn8B989C9zSySFK4GU6r4JH74R"},"s3":{"s3SchemaVersion":"1.0","configurationId":"SQS_Notif","bucket":{"name":"mybucket-s2038770","ownerIdentity":{"principalId":"A2JT9LIIOSN8JZ"},"arn":"arn:aws:s3:::mybucket-s2038770"},"object":{"key":"IMG_20240212_151946.jpg","size":233274,"eTag":"331cb3fcb77ef34354967294b045ed61","versionId":"Usb5DvMuLNMwVqA9KzwL3.LXz4ZT4bwd","sequencer":"0066086123CEA364EE"}}}]}', 'attributes': {'ApproximateReceiveCount': '2', 'SentTimestamp': '1711825189037', 'SenderId': 'AROA4R74ZO52XAB5OD7T4:S3-PROD-END', 'ApproximateFirstReceiveTimestamp': '1711825489037'}, 'messageAttributes': {}, 'md5OfBody': 'f34fefb17623083c6cb1784767eaac1e', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:us-east-1:519012545046:MyQueueS2038770', 'awsRegion': 'us-east-1'}
    ]}

# Extract message_body, image_bucket, and image_key, eventName, eventTime, sourceIP from event
message_body = json.loads(event['Records'][0]['body'])
image_bucket = message_body['Records'][0]['s3']['bucket']['name']
image_key = message_body['Records'][0]['s3']['object']['key']
eventName = message_body['Records'][0]['eventName']
eventTime = message_body['Records'][0]['eventTime']
sourceIP = message_body['Records'][0]['requestParameters']['sourceIPAddress']

# ! Good from up till here

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the DynamoDB table name
table_name = 'test_table'

def lambda_handler(event, context):
    # Extract message body from the SQS event
    message_body = json.loads(event['Records'][0]['body'])
    # image_bucket = message_body['image_bucket']
    # image_key = message_body['image_key']

    # # Initialize the Rekognition client
    # rekognition = boto3.client('rekognition')

    # # Call Rekognition to detect labels
    # response_labels = rekognition.detect_labels(
    #     Image={
    #         'S3Object': {
    #             'Bucket': image_bucket,
    #             'Name': image_key
    #         }
    #     },
    #     MaxLabels=10,  # Adjust max number of labels as needed
    #     MinConfidence=70  # Adjust confidence threshold as needed
    # )

    # # Call Rekognition to detect text
    # response_text = rekognition.detect_text(
    #     Image={
    #         'S3Object': {
    #             'Bucket': image_bucket,
    #             'Name': image_key
    #         }
    #     }
    # )

    # # Process Rekognition label response
    # labels = response_labels['Labels']
    # detected_labels = [{'Name': label['Name'], 'Confidence': label['Confidence']} for label in labels]

    # # Process Rekognition text response
    # text_detections = response_text['TextDetections']
    # detected_texts = [{'Text': text['DetectedText'], 'Confidence': text['Confidence']} for text in text_detections]

    # Prepare item for DynamoDB
    dynamo_item = {
        message_body,
    }

    # Put item into DynamoDB table
    try:
        dynamodb.put_item(TableName=table_name, Item=dynamo_item)
        print(f'Successfully added item to DynamoDB table: {table_name}')
        return {
            'statusCode': 200,
            'body': json.dumps('Item added to DynamoDB table successfully')
        }
    except Exception as e:
        print(f'Error adding item to DynamoDB table: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to add item to DynamoDB table')
        }
