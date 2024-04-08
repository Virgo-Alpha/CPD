import boto3
import json
from datetime import datetime

# Initialize the DynamoDB and SNS clients
dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns')
s3 = boto3.client('s3')

# Define the DynamoDB table name
vehicle_table_name = 'vehicleTableS2038770'
sns_topic_arn = 'arn:aws:sns:us-east-1:519012545046:Vehicles-Notification'

# GET request to the following link displays emergency contacts
help_api = 'https://xgo132q6la.execute-api.us-east-1.amazonaws.com/default/callHelpS2038770'

current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

def send_email(subject, message, link=None, topic_arn=sns_topic_arn):
    """
    Send_email function to send an email via SNS
    :param subject: Email subject
    :param message: Email message
    :param link: Optional link to include in the email
    :param topic_arn: SNS topic ARN to send the email to
    """
    try:
        email_message = message
        if link:
            # If link is provided, include the link in the email
            email_message += f'\n\nDownload the Image with the Vehicle here: {link}'
        email_message += f'\n\nClick the following link to request assistance: {help_api}'
        response = sns.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=email_message
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
        print(f'Event: {event}')
        label_names = event['Records'][0]['dynamodb']['NewImage']['label_names']['L'] or event['Records'][0]['dynamodb']['OldImage']['label_names']['L']
        label_names = [item['S'] for item in label_names]

        if 'Vehicle' not in label_names:
            print(f'No vehicle detected in the image. labels: {label_names}')
            return {
                'statusCode': 200,
                'body': json.dumps('No vehicle detected in the image')
            }
        
        # Extract list of text values from the DynamoDB event
        new_text_values = event['Records'][0]['dynamodb']['NewImage']['text_values']['L'] # or event['Records'][0]['dynamodb']['OldImage']['text_values']['L']
        new_text_values = [item['S'] for item in new_text_values]
        
        print(f'New Text Values: {new_text_values}')

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
            # ! send an SNS notification
            print(f'No matching text values found in the vehicle table for image: {event["Records"][0]["dynamodb"]["NewImage"]["imageName"]["S"]}')
            
            email_subject = 'Unidentified Vehicle Detected'
            email_message = f'\nAn unidentified vehicle was detected in the image: {event["Records"][0]["dynamodb"]["NewImage"]["imageName"]["S"]}\n'
            email_message += f'\nEvent Time: {event["Records"][0]["dynamodb"]["NewImage"]["eventTime"]["S"]}\n'
            email_message += f'\nText Detected: {new_text_values}\n'
            email_message += f'\nVehicle Labels: {label_names}'
            # Set the S3 link to the image
            s3_link = f'https://{event["Records"][0]["dynamodb"]["NewImage"]["image_bucket"]["S"]}.s3.amazonaws.com/{event["Records"][0]["dynamodb"]["NewImage"]["imageName"]["S"]}'
            print(f'S3 Link: {s3_link}')
            send_email(email_subject, email_message, link=s3_link)
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
                # ! Send email via SNS
                print(f'Blacklisted text value detected in an image')
                
                email_subject = 'Blacklisted Vehicle Detected'
                email_message = f'A blacklisted Vehicle value was detected in the image: {event["Records"][0]["dynamodb"]["NewImage"]["imageName"]["S"]}\n'
                email_message += f'\nEvent Time: {formatted_time}\n'
                email_message += f'\nVehicle Number Plate: {blacklisted_text_values_set}\n'
                # Set the S3 link to the image
                s3_link = f'https://{event["Records"][0]["dynamodb"]["NewImage"]["image_bucket"]["S"]}.s3.amazonaws.com/{event["Records"][0]["dynamodb"]["NewImage"]["imageName"]["S"]}'
                print(f'S3 Link: {s3_link}')
                send_email(email_subject, email_message, link=s3_link)
            else:
                print('No Blacklisted image uploaded')

        return {
            'statusCode': 200,
            'body': json.dumps('Processing completed successfully')
        }
    except Exception as e:
        print(f'Error processing event: {e}')
        print(f'Event: {event}')
        return {
            'statusCode': 500,
        }
