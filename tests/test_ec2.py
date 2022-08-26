import asyncio
import os
import unittest
from typing import Final
from packages import (
    AwsResources,
    create_ec2_instance,
    destroy_ec2_instance
)

NAME: Final = 'unit-test'


class TestEc2(unittest.TestCase):
    async def test_create_ec2_instance(self):
        assert asyncio.create_task(
            create_ec2_instance(
                AwsResources.dev.region,
                AwsResources.dev.ami_id,
                AwsResources.dev.instance_type,
                NAME,
                os.environ['SSH_KEY_USE1'],
                1,
                1
            )
        )

    async def test_destroy_ec2_instance(self):
        assert asyncio.create_task(
            destroy_ec2_instance(
                AwsResources.dev.region
            )
        )



if __name__ == '__main__':
    unittest.main()
