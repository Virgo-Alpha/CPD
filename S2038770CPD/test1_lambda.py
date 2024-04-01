import boto3
import json

# Initialize the DynamoDB and SNS clients
dynamodb = boto3.client('dynamodb')
sns = boto3.client('sns')

# Define the DynamoDB table name
vehicle_table_name = 'vehicleTableS2038770'
sns_topic_arn = 'arn:aws:sns:us-east-1:your-account-id:your-sns-topic'

def lambda_handler(event, context):
    try:
        # Extract label names
        label_names = event['Records'][0]['dynamodb']['NewImage']['label_names']['L']
        label_names = [item['S'] for item in label_names]

        if 'Vehicle' and 'Car' not in label_names:
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
        
        print(f'new text_value set: {new_text_values_set}')

        # Check if any new text value can be found in the vehicle table text values
        if new_text_values_set.intersection(vehicle_table_text_values_set):
            # send an SNS notification (email) but for now just print the image_name
            print(f'No matching text values found in the vehicle table for image: {event["Records"][0]["dynamodb"]["NewImage"]["imageName"]["S"]}')
            # If there is an intersection, get the value of the blacklisted attribute and check if it is True
            # If it is True, send an SNS notification (email)

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
        
        # imageName = event['Records'][0]['dynamodb']['NewImage']['imageName']['S']
        
        print(f'Blacklist: {blacklisted_text_values_set}')
        
        # Check if any new text value matches a blacklisted value
        if new_text_values_set.intersection(blacklisted_text_values_set):
            # Send email via SNS but for now just print the image name
            print(f'Blacklisted text value detected in image')
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