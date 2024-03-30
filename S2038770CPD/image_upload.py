import boto3
import os
from botocore.exceptions import ClientError
import logging
import time

# Initialize the Boto3 client for S3
s3_client = boto3.client('s3')

def upload_image_to_s3(file_name, bucket='mybucket-s2038770', object_name=None):
    """Upload an image to an S3 bucket

    :param file_name: name of Image to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded successfully, False otherwise
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        s3_client.upload_file(os.path.join('Images', file_name), bucket, file_name)
        print(f'Uploaded {file_name} to S3')
        return True
    except ClientError as e:
        logging.error(e)
        print(f'Error uploading {file_name} to S3: {e}')
        return False

# Main function to upload image files at intervals
def main():
    # List all files in the "Images" folder
    image_files = os.listdir('Images')

    for file_name in image_files:
        # Upload each image file to S3
        success = upload_image_to_s3(file_name=file_name)
        if success:
            # 30 second interval between uploads
            time.sleep(30)

if __name__ == '__main__':
    main()
