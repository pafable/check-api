from packages import (
    ApiEndpoint,
    AwsResources,
    AzureResources
)
from azure.identity import DefaultAzureCredential
import os
import unittest


class TestConstants(unittest.TestCase):
    def test_api_endpoint(self):
        assert ApiEndpoint.API1.value
        assert ApiEndpoint.API2.value
        assert ApiEndpoint.API3.value

    def test_aws_resources(self):
        assert AwsResources.dev.value
        assert AwsResources.prod.value

    def test_azure_resources(self):
        assert AzureResources.dev.value
        assert AzureResources.dev.get_az_cred


if __name__ == '__main__':
    unittest.main()
