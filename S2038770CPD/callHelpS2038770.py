import boto3

# Initialize the SNS client
sns = boto3.client('sns')

def lambda_handler(event, context):
    """
    Lambda function handler to process an SMS request and send an SNS notification
    :param event: API Gateway event containing the HTTP method
    :param context: Lambda context object
    """
    # Define the numbers for police and security company
    numbers = {
        "police": "911",
        "security_company": "555-1234"
    }
    
    # Check if the HTTP method is GET
    if event['httpMethod'] == 'GET':
        # Prepare the response body as a table
        response_body = (
            f'Assistance has been requested via SMS. Please use the numbers below to call for additional help:\n'
            f"\nPolice Contact: {numbers['police']}\n"
            f"Security Company Contact: {numbers['security_company']}\n"
        )
        
        # Prepare the response object
        response = {
            "statusCode": 200,
            "body": response_body
        }

        sns_message = "Help urgently requested at Bly Manor. Please send assistance."
        
        # Publish the message to the SNS topic for SMS subscription
        topic_arn = 'arn:aws:sns:us-east-1:519012545046:helpRequested'
        sns.publish(
            TopicArn=topic_arn,
            Message=sns_message
        )
    else:
        # If the method is not GET, return a method not allowed response
        response = {
            "statusCode": 405,
            "body": "Method not allowed"
        }
    
    return response
