import boto3
import json

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')
# Initialize the Rekognition client
rekognition = boto3.client('rekognition')

# Define the DynamoDB table name
table_name = 'entryTableS2038770'

def detect_text_and_labels(image_bucket, image_key):
    """Detect labels and text in an image using Amazon Rekognition
    :param image_bucket: S3 bucket name where the image is stored
    :param image_key: S3 object key for the image
    :return: List of detected labels and text in the image
    """
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
    """Lambda function handler to process messages from SQS and add items to DynamoDB
    :param event: SQS event containing messages
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

            # Detect labels and text in the image
            detected_labels, detected_text = detect_text_and_labels(image_bucket, image_key)

            print(f'Detected labels: {detected_labels}')
            print(f'Detected text: {detected_text}')
            
            # Initialize empty lists
            label_names = []
            label_confidence_scores = []
            text_values = []
            text_confidence_scores = []
            
            # Extract labels and their confidence scores
            for label in detected_labels:
                label_names.append(label['Name'])
                label_confidence_scores.append(label['Confidence'])
            
            # Extract text and its confidence scores
            for text_item in detected_text:
                text_values.append(text_item['Text'])
                text_confidence_scores.append(text_item['Confidence'])
            
            # Store the lists in the DynamoDB item
            dynamo_item = {
                'imageName': {'S': image_key},
                'image_bucket': {'S': image_bucket},
                'eventName': {'S': eventName},
                'eventTime': {'S': eventTime},
                'sourceIP': {'S': sourceIP},
                'label_names': {'L': [{'S': label} for label in label_names]},
                'label_confidence_scores': {'L': [{'S': str(score)} for score in label_confidence_scores]},
                'text_values': {'L': [{'S': text} for text in text_values]},
                'text_confidence_scores': {'L': [{'S': str(score)} for score in text_confidence_scores]}
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
