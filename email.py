import boto3

# Initialize the SNS client
sns = boto3.client('sns')

def send_email(subject, message, topic_arn):
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

# Example usage
subject = "Test Email"
message = "This is a test email sent through AWS SNS."
topic_arn = "arn:aws:sns:us-east-1:519012545046:Vehicles-Notification"

send_email(subject, message, topic_arn)
