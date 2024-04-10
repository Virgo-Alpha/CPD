import boto3
import botocore

# student ID definition
student_id = 's2038770'

def create_s3_bucket(bucket_name):
    """Create an S3 bucket with versioning, server-side encryption, and lifecycle policy enabled.

    :param bucket_name: Name of the S3 bucket to create
    """

    s3_client = boto3.client('s3')
    try:
        # Create the S3 bucket
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': 'us-east-1'}
        )
        print(f'Successfully created S3 bucket with name: {bucket_name}')

        # Enable versioning on the S3 bucket
        s3_client.put_bucket_versioning(
            Bucket=bucket_name,
            VersioningConfiguration={'Status': 'Enabled'}
        )
        print(f'Versioning enabled on S3 bucket: {bucket_name}')

        # Implement server-side encryption on the S3 bucket
        s3_client.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration={
                'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]
            }
        )
        print(f'Server-side encryption enabled on S3 bucket: {bucket_name}')

        # Implement lifecycle policy for transitioning objects to S3 Glacier
        s3_client.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration={
                'Rules': [
                    {
                        'ID': 'MoveToGlacierRule',
                        'Status': 'Enabled',
                        'Transitions': [{'Days': 30, 'StorageClass': 'GLACIER'}],
                        'NoncurrentVersionTransitions': [{'NoncurrentDays': 60, 'StorageClass': 'GLACIER'}]
                    }
                ]
            }
        )
        print('Lifecycle policy configured for S3 bucket')

    except botocore.exceptions.ClientError as e:
        print(f'Error creating S3 bucket: {e.response["Error"]["Message"]}')

def main_s3():
    # Define the S3 bucket name
    bucket_name = f'mybucket-{student_id}'

    # Create the S3 bucket with specified configurations
    create_s3_bucket(bucket_name)

if __name__ == '__main__':
    main_s3()
