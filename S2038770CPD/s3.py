import boto3
import botocore

# Initialize the Boto3 S3 client
s3_client = boto3.client('s3')

# student ID definition
student_id = 's2038770'

# Define the S3 bucket name with your student ID
s3_bucket_name = f'mybucket-{student_id}'

try:
    # Create the S3 bucket with versioning enabled
    s3_client.create_bucket(
        Bucket=s3_bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'us-east-1'
        }
    )
    print(f'Successfully created S3 bucket with name: {s3_bucket_name}')

    # Enable versioning on the S3 bucket
    s3_client.put_bucket_versioning(
        Bucket=s3_bucket_name,
        VersioningConfiguration={
            'Status': 'Enabled'
        }
    )
    print(f'Versioning enabled on S3 bucket: {s3_bucket_name}')

    # Implement server-side encryption on the S3 bucket
    s3_client.put_bucket_encryption(
        Bucket=s3_bucket_name,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256'
                    }
                }
            ]
        }
    )
    print(f'Server-side encryption enabled on S3 bucket: {s3_bucket_name}')

    # Implement lifecycle policy for transitioning objects to S3 Glacier
    s3_client.put_bucket_lifecycle_configuration(
        Bucket=s3_bucket_name,
        LifecycleConfiguration={
            'Rules': [
                {
                    'ID': 'MoveToGlacierRule',
                    'Prefix': '',
                    'Status': 'Enabled',
                    'Transitions': [
                        {
                            'Days': 30,  # Transition objects to S3 Glacier after 30 days
                            'StorageClass': 'GLACIER'
                        }
                    ],
                    'NoncurrentVersionTransitions': [
                        {
                            'NoncurrentDays': 60,  # Transition noncurrent object versions to S3 Glacier after 60 days
                            'StorageClass': 'GLACIER'
                        }
                    ]
                }
            ]
        }
    )
    print('Lifecycle policy configured for S3 bucket')

except botocore.exceptions.ClientError as e:
    print(f'Error creating S3 bucket: {e.response["Error"]["Message"]}')
