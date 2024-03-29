import boto3
import botocore

# Initialize the Boto3 EC2 client
ec2_client = boto3.client('ec2')

# my student ID
student_id = 'S2038770'

ec2_instance_params = {
    'ImageId': 'ami-0005e0cfe09cc9050',  # Specify the desired Amazon Machine Image (AMI) ID
    'InstanceType': 't2.micro',  # Specify the instance type (e.g., t2.micro)
    'KeyName': 'vockey',  # Specify the key pair name for SSH access
    'security_group': 'sg-007eabf003fb80edd',  # Specify the security group ID
    'MinCount': 1,  # Minimum number of instances to launch
    'MaxCount': 1,  # Maximum number of instances to launch
    'TagSpecifications': [
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': f'EC2Instance{student_id}'
                }
            ]
        }
    ]
}


try:
    # Create the EC2 instance
    response = ec2_client.run_instances(**ec2_instance_params)
    # Extract the instance ID from the response
    instance_id = response['Instances'][0]['InstanceId']
    print(f'Successfully created EC2 instance with ID: {instance_id}')
except botocore.exceptions.ClientError as e:
    print(f'Error creating EC2 instance: {e.response["Error"]["Message"]}')
