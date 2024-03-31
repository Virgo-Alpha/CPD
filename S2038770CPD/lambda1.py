import boto3
import json

# // TODO: Find out what the SQS contains 
# // TODO: extract entities in the Lambda function
# TODO: Store the entities in a DynamoDB test_table and run them through AWS Rekognition

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')
# Initialize the Rekognition client
rekognition = boto3.client('rekognition')

# Define the DynamoDB table name
table_name = 'vehicleTable'

def detect_text_and_labels(image_bucket, image_key):
    # Detect labels and text in the image using Amazon Rekognition
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': image_bucket,
                'Name': image_key
            }
        },
        MaxLabels=10,  # Adjust the max number of labels returned as needed
        MinConfidence=70  # Set the minimum confidence threshold for labels
    )

    # Extract detected labels and their confidence scores
    labels = [{'Name': label['Name'], 'Confidence': label['Confidence']} for label in response['Labels']]

    # Detect text in the image
    text_response = rekognition.detect_text(
        Image={
            'S3Object': {
                'Bucket': image_bucket,
                'Name': image_key
            }
        }
    )

    # Extract detected text and its confidence scores
    detected_text = [{'Text': text['DetectedText'], 'Confidence': text['Confidence']} for text in text_response['TextDetections']]

    return labels, detected_text

def lambda_handler(event, context):
    try:
        # Extract message body from the SQS event
        for record in event['Records']:
            message_body = json.loads(record['body'])
            image_bucket = message_body['Records'][0]['s3']['bucket']['name']
            image_key = message_body['Records'][0]['s3']['object']['key']
            eventName = message_body['Records'][0]['eventName']
            eventTime = message_body['Records'][0]['eventTime']
            sourceIP = message_body['Records'][0]['requestParameters']['sourceIPAddress']

            # Detect labels and text in the image
            labels, detected_text = detect_text_and_labels(image_bucket, image_key)

            # Initialize empty lists
            labels = []
            label_confidence = []
            text = []
            text_confidence = []

            # Extract labels and their confidence scores
            for label in labels:
                labels.append(label['Name']['S'])
                label_confidence.append(label['Confidence']['S'])

            # Extract text and its confidence scores
            for text_item in detected_text:
                text.append(text_item['Text']['S'])
                text_confidence.append(text_item['Confidence']['S'])

            # Prepare item for DynamoDB with detected labels and text
            dynamo_item = {
                'imageName': {'S': image_key},
                'image_bucket': {'S': image_bucket},
                'eventName': {'S': eventName},
                'eventTime': {'S': eventTime},
                'sourceIP': {'S': sourceIP},
                'labels': {'L': [{'S': label} for label in labels]},
                'label_confidence': {'L': [{'S': confidence} for confidence in label_confidence]},
                'text': {'L': [{'S': t} for t in text]},
                'text_confidence': {'L': [{'S': confidence} for confidence in text_confidence]}
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
