import boto3


async def create_ec2_instance(region: str, image: str, instance_type: str, instance_name: str, keyname: str, max_count: int, min_count: int) -> dict:
    """
    Creates EC2 instances
    :param region:
    :param image:
    :param instance_type:
    :param instance_name:
    :param keyname:
    :param max_count:
    :param min_count:
    :return:
    """
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
