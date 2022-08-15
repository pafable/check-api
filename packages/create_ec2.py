import boto3


def create_ec2_instance(region: str, image: str, instance_type: str, instance_name: str, keyname: str, max_count: int, min_count: int) -> dict:
    ec2 = boto3.client('ec2', region_name=region)
    resp = ec2.run_instances(
        ImageId=image,
        InstanceType=instance_type,
        KeyName=keyname,
        MaxCount=max_count,
        MinCount=min_count,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name
                    }
                ]
            }
        ]
    )

    return resp
