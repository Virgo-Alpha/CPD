import boto3

# Initialize the SNS client
sns = boto3.client('sns')

def subscribe_email_to_topic(email_address, topic_arn):
    """
    Subscribe an email address to an SNS topic
    :param email_address: Email address to subscribe
    :param topic_arn: ARN of the SNS topic
    :return: True if successful, False otherwise
    """
    try:
        response = sns.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email_address
        )
        print("Subscribed email address to topic:", response)
        return True
    except Exception as e:
        print("Error subscribing email address to topic:", e)
        return False

# Example usage
email_address = "john.doe@example.com"
topic_arn = "arn:aws:sns:us-east-1:519012545046:Vehicles-Notification"

subscribe_email_to_topic(email_address, topic_arn)
