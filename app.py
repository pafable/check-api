from packages import app_contstants, create_ec2
from urllib.request import urlopen
from time import perf_counter
from typing import Final
import asyncio
import json
import logging
import os
import pprint
import ssl


USE1_INSTANCE_NAME: Final = 'us-east-1-test-instance'
USW2_INSTANCE_NAME: Final = 'us-west-2-test-instance'
pp: Final = pprint.PrettyPrinter(indent=2)

ssl._create_default_https_context = ssl._create_unverified_context

resp = urlopen(app_contstants.ApiEndpoint.API1.url)
resp = json.loads(resp.read().decode())


pp.pprint(resp['entries'][0]['API'])


def main():
    use1 = create_ec2.create_ec2_instance(
        app_contstants.Ec2Images.USE1.region,
        app_contstants.Ec2Images.USE1.ami_id,
        app_contstants.InstanceTypes.dev.instance_type,
        USE1_INSTANCE_NAME,
        os.environ['SSH_KEY_USE1'],
        1,
        1
    )
    pp.pprint(use1)

    usw2 = create_ec2.create_ec2_instance(
        app_contstants.Ec2Images.USW2.region,
        app_contstants.Ec2Images.USW2.ami_id,
        app_contstants.InstanceTypes.dev.instance_type,
        USW2_INSTANCE_NAME,
        os.environ['SSH_KEY_USW2'],
        1,
        1
    )
    pp.pprint(usw2)


if __name__ == '__main__':
    main()

print(f'{round(perf_counter(), 2)} secs')
