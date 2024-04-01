import boto3
import json
from datetime import datetime

# Initialize the DynamoDB and SNS clients
dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns')

# Define the DynamoDB table name
vehicle_table_name = 'vehicleTableS2038770'
sns_topic_arn = 'arn:aws:sns:us-east-1:519012545046:Vehicles-Notification'

current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

def send_email(subject, message, topic_arn=sns_topic_arn):
    """Send an email using the SNS service
    :param subject: Email subject
    :param message: Email message
    :param topic_arn: SNS topic ARN
    :return: True if successful, False otherwise
    """
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
        print("Email sent successfully:", response)
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

def lambda_handler(event, context):
    """
    Lambda function handler to process messages from DynamoDB and send SNS notifications if necessary
    :param event: DynamoDB event containing new records
    :param context: Lambda context object
    
    :return: Response indicating success or failure
    """

    try:
        # Extract label names
        label_names = event['Records'][0]['dynamodb']['NewImage']['label_names']['L'] or event['Records'][0]['dynamodb']['OldImage']['label_names']['L']
        label_names = [item['S'] for item in label_names]

        if 'Vehicle' not in label_names:
            print(f'No vehicle detected in the image. labels: {label_names}')
            return {
                'statusCode': 200,
                'body': json.dumps('No vehicle detected in the image')
            }
        
        # Extract list of text values from the DynamoDB event
        new_text_values = event['Records'][0]['dynamodb']['NewImage']['text_values']['L']
        new_text_values = [item['S'] for item in new_text_values]

        # Retrieve text values from the vehicleTableS2038770 DynamoDB table
        response = dynamodb.scan(
            TableName=vehicle_table_name,
            ProjectionExpression='text_values'
        )

        # Extract text values from the response and convert to set
        vehicle_table_text_values = set()
        for item in response['Items']:
            text_values = item['text_values']['L']
            vehicle_table_text_values.update({value['S'] for value in text_values})

        # Convert the lists to sets
        new_text_values_set = set(new_text_values)
        vehicle_table_text_values_set = set(vehicle_table_text_values)

        # Check if any new text value can be found in the vehicle table text values
        if not new_text_values_set.intersection(vehicle_table_text_values_set):
            print(f'No matching text values found in the vehicle table for image: {event["Records"][0]["dynamodb"]["NewImage"]["imageName"]["S"]}')
    
            email_subject = 'Unidentified Vehicle Detected'
            email_message = f'An unidentified vehicle was detected in the image: {event["Records"][0]["dynamodb"]["NewImage"]["imageName"]["S"]}\n'
            email_message += f'Event Time: {event["Records"][0]["dynamodb"]["NewImage"]["eventTime"]["S"]}\n'
            email_message += f'Text Detected: {new_text_values}\n'
            email_message += f'Vehicle Labels: {label_names}'
            send_email(email_subject, email_message)
        else:
            # Check if any text value is blacklisted - if there is an intersection from the above
            response = dynamodb.scan(
                TableName=vehicle_table_name,
                FilterExpression='Blacklisted = :blacklist',
                ExpressionAttributeValues={':blacklist': {'BOOL': True}},
                ProjectionExpression='text_values'
            )

            # Extract text values from the response and convert to set
            blacklisted_text_values_set = set()
            for item in response['Items']:
                text_values = item['text_values']['L']
                blacklisted_text_values_set.update({value['S'] for value in text_values})
            
            # Check if any new text value matches a blacklisted value
            if new_text_values_set.intersection(blacklisted_text_values_set):
                print(f'Blacklisted text value detected in an image')
                
                email_subject = 'Blacklisted Vehicle Detected'
                email_message = f'A blacklisted Vehicle value was detected in an image\n'
                email_message += f'Event Time: {formatted_time}\n'
                email_message += f'Vehicle Number Plate: {blacklisted_text_values_set}\n'
                send_email(email_subject, email_message)
            else:
                print('No Blacklisted image uploaded')

        return {
            'statusCode': 200,
            'body': json.dumps('Processing completed successfully')
        }
    except Exception as e:
        print(f'Error processing event: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to process event')
        }