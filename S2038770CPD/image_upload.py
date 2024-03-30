import boto3
import os
import time

# Initialize the Boto3 client for S3
s3_client = boto3.client('s3')

# Define the S3 bucket name
bucket_name = 'mybucket-s2038770'

# Function to upload image file to S3
def upload_image_to_s3(file_name):
    try:
        # Upload image file to S3
        s3_client.upload_file(os.path.join('Images', file_name), bucket_name, file_name)
        print(f'Uploaded {file_name} to S3')

    except Exception as e:
        print(f'Error uploading {file_name} to S3: {e}')

# Main function to upload image files at intervals
def main():
    while True:
        # List all files in the "Images" folder
        image_files = os.listdir('Images')

        for file_name in image_files:
            # Upload each image file to S3
            upload_image_to_s3(file_name)

        # Adjust interval as needed (30 seconds in this case)
        time.sleep(30)

if __name__ == '__main__':
    main()
