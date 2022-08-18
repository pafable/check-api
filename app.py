from packages import ApiEndpoint, AwsResources, create_ec2_instance, destroy_ec2_instance
from time import perf_counter
from typing import Final
from urllib.request import urlopen
import asyncio
import json
import logging
import os
import ssl

SUFFIX: Final = ('test-instance',)
USE1_INSTANCE_NAME: Final = (f'{AwsResources.dev.region}-{SUFFIX[0]}',)
USW2_INSTANCE_NAME: Final = (f'{AwsResources.prod.region}-{SUFFIX[0]}',)

logging.basicConfig(level=logging.INFO, format='[ %(levelname)s ] %(message)s')

# This is needed to interact with HTTPS websites
ssl._create_default_https_context = ssl._create_unverified_context


async def main():
    api_resp = urlopen(ApiEndpoint.API1.url)
    api_resp = json.loads(api_resp.read().decode())
    api_check = api_resp['entries'][0]['API']

    logging.info(f'API: {api_check}')

    aws_use1_create = asyncio.create_task(
        create_ec2_instance(
            AwsResources.dev.region,
            AwsResources.dev.ami_id,
            AwsResources.dev.instance_type,
            USE1_INSTANCE_NAME[0],
            os.environ['SSH_KEY_USE1'],
            1,
            1
        )
    )

    try:
        await aws_use1_create

        if len(api_check) >= 10:
            aws_usw2_create = asyncio.create_task(
                create_ec2_instance(
                    AwsResources.prod.region,
                    AwsResources.prod.ami_id,
                    AwsResources.prod.instance_type,
                    USW2_INSTANCE_NAME[0],
                    os.environ['SSH_KEY_USW2'],
                    1,
                    1
                )
            )
            await aws_usw2_create
            logging.info(f'USW2 Instance: {aws_usw2_create.result()["Instances"][0]["InstanceId"]}')

        logging.info(f'USE1 Instance: {aws_use1_create.result()["Instances"][0]["InstanceId"]}')
    except Exception as e:
        logging.error(e)

    '''
    UNCOMMENT LINES BELOW TO TERMINATE INSTANCES
    FOR TESTING ONLY!
    '''
    aws_use1_destroy = destroy_ec2_instance(
            [aws_use1_create.result()["Instances"][0]["InstanceId"]],
            AwsResources.dev.region
        )

    if aws_use1_destroy["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise logging.error(f'Destroy error code: {aws_use1_destroy["ResponseMetadata"]["HTTPStatusCode"]}')
    else:
        logging.info(f'{aws_use1_destroy["TerminatingInstances"][0]["InstanceId"]} has been destroyed')

    if len(api_check) >= 10:
        aws_usw2_destroy = destroy_ec2_instance(
                [aws_usw2_create.result()["Instances"][0]["InstanceId"]],
                AwsResources.prod.region
            )

        if aws_usw2_destroy["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise logging.error(f'Destroy error code: {aws_usw2_destroy["ResponseMetadata"]["HTTPStatusCode"]}')
        else:
            logging.info(f'{aws_usw2_destroy["TerminatingInstances"][0]["InstanceId"]} has been destroyed')


if __name__ == '__main__':
    asyncio.run(main())

logging.info(f'Total execution time: {round(perf_counter(), 2)} secs')
