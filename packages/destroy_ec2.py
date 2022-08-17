import boto3


def destroy_ec2_instance(instance_ids: list, region: str) -> dict:
    """
    Destroys EC2 instances
    :param instance_ids:
    :param region:
    :return:
    """
    ec2 = boto3.client('ec2', region_name=region)
    return ec2.terminate_instances(InstanceIds=instance_ids)
