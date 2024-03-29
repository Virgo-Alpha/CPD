import boto3
import time

# Initialize the Boto3 clients for S3 and SQS
s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')

# Define the SQS queue URL
queue_url = 'https://sqs.us-east-1.amazonaws.com/519012545046/MyQueueS2038770'

# Define the S3 bucket name
bucket_name = 'mybucket-s2038770'

# Function to upload image file to S3 and send message to SQS
def upload_image_to_s3(file_name):
    try:
        # Upload image file to S3
        s3_client.upload_file(file_name, bucket_name, file_name)

        # Send message to SQS queue
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=file_name
        )
        print(f'Uploaded {file_name} to S3 and sent message to SQS')

    except Exception as e:
        print(f'Error uploading {file_name} to S3 and sending message to SQS: {e}')

# Main function to upload image files at intervals
def main():
    while True:
        # ! Replace 'image1.jpg', 'image2.jpg', etc. with your image file names
        image_files = ['image1.jpg', 'image2.jpg', 'image3.jpg']

        for file_name in image_files:
            upload_image_to_s3(file_name)

            # Adjust interval as needed (30 seconds in this case)
            time.sleep(30)

if __name__ == '__main__':
    main()
