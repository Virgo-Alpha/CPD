import boto3
import botocore

# student ID definition
student_id = 'S2038770'

def create_ec2_instance(instance_params):
    """Create an EC2 instance with the specified parameters.

    :param instance_params: Parameters for creating the EC2 instance
    :return: Instance ID of the created EC2 instance, or None if creation failed
    """

    ec2_client = boto3.client('ec2')
    try:
        response = ec2_client.run_instances(**instance_params)
        instance_id = response['Instances'][0]['InstanceId']
        print(f'Successfully created EC2 instance with ID: {instance_id}')
        return instance_id
    except botocore.exceptions.ClientError as e:
        print(f'Error creating EC2 instance: {e.response["Error"]["Message"]}')
        return None

def main_ec2():
    # Define the parameters for creating the EC2 instance
    ec2_instance_params = {
        'ImageId': 'ami-0005e0cfe09cc9050',
        'InstanceType': 't2.micro',
        'KeyName': 'vockey',
        'SecurityGroupIds': ['sg-007eabf003fb80edd'],
        'MinCount': 1,
        'MaxCount': 1,
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

    # Create the EC2 instance
    create_ec2_instance(ec2_instance_params)

if __name__ == '__main__':
    main_ec2()
