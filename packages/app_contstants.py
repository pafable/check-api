from azure.identity import DefaultAzureCredential
from enum import Enum
from typing import Final
import boto3


class ApiEndpoint(Enum):
    """
    APIs to check
    1. api.publicapis.org
    2. cat-fact.herokuapp.com
    """
    API1: Final = ('https://api.publicapis.org/random', 'first')
    API2: Final = ('https://api.publicapis.org/categories', 'second')
    API3: Final = ('https://cat-fact.herokuapp.com/facts', 'third')

    def __init__(self, url, position: str) -> None:
        self.url = url
        self.position = position

    @property
    def do_something(self):
        return f'api endpoint {self.url} and position {self.position}'


class AwsResources(Enum):
    """
    Constants for resources stored or used in AWS
    """
    dev: Final = ('t2.micro', 'azure-subscription-id-dev', 'us-east-1', 'ami-090fa75af13c156b4')
    prod: Final = ('t3.large', 'azure-subscription-id-prod', 'us-west-2', 'ami-0cea098ed2ac54925')

    def __init__(self, instance_type: str, az_sub_id: str, region: str, ami_id: str) -> None:
        self.instance_type = instance_type
        self.az_sub_id = az_sub_id
        self.region = region
        self.ami_id = ami_id


class AzureResources(Enum):
    """
    Constants for Resources in Azure
    """
    dev: Final = ('test-rg100', 'eastus')

    def __init__(self, rg_name: str, region: str) -> None:
        self.rg_name = rg_name
        self.region = region

    @property
    def get_az_sub_id(self) -> str:
        ssm = boto3.client('ssm', region_name=AwsResources.dev.region)
        return ssm.get_parameter(Name=AwsResources.dev.az_sub_id, WithDecryption=True)["Parameter"]["Value"]

    @property
    def get_az_cred(self):
        return DefaultAzureCredential(exclude_shared_token_cache_credential=True)
