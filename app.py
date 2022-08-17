from packages import app_contstants, create_ec2, destroy_ec2
from urllib.request import urlopen
from time import perf_counter
from typing import Final
import asyncio
import json
import logging
import os
import ssl


USE1_INSTANCE_NAME: Final = f'{app_contstants.Ec2Images.USE1.region}-test-instance'
USW2_INSTANCE_NAME: Final = f'{app_contstants.Ec2Images.USW2.region}-test-instance'

logging.basicConfig(level=logging.INFO, format='[ %(levelname)s ] - %(message)s')
ssl._create_default_https_context = ssl._create_unverified_context


async def main():
    api_resp = urlopen(app_contstants.ApiEndpoint.API1.url)
    api_resp = json.loads(api_resp.read().decode())
    api_check = api_resp['entries'][0]['API']

    logging.info(f'API: {api_check}')

    use1_create = asyncio.create_task(
        create_ec2.create_ec2_instance(
            app_contstants.Ec2Images.USE1.region,
            app_contstants.Ec2Images.USE1.ami_id,
            app_contstants.InstanceTypes.dev.instance_type,
            USE1_INSTANCE_NAME,
            os.environ['SSH_KEY_USE1'],
            1,
            1
        )
    )

    try:
        await use1_create

        if len(api_check) >= 10:
            usw2_create = asyncio.create_task(
                create_ec2.create_ec2_instance(
                    app_contstants.Ec2Images.USW2.region,
                    app_contstants.Ec2Images.USW2.ami_id,
                    app_contstants.InstanceTypes.dev.instance_type,
                    USW2_INSTANCE_NAME,
                    os.environ['SSH_KEY_USW2'],
                    1,
                    1
                )
            )
            await usw2_create
            logging.info(f'USW2 Instance: {usw2_create.result()["Instances"][0]["InstanceId"]}')

        logging.info(f'USE1 Instance: {use1_create.result()["Instances"][0]["InstanceId"]}')
    except Exception as e:
        logging.error(e)

    '''
    UNCOMMENT LINES BELOW TO TERMINATE INSTANCES
    FOR TESTING ONLY!
    '''
    # use1_destroy = destroy_ec2.destroy_ec2_instance(
    #         [use1_create.result()["Instances"][0]["InstanceId"]],
    #         app_contstants.Ec2Images.USE1.region
    #     )
    #
    # if use1_destroy["ResponseMetadata"]["HTTPStatusCode"] != 200:
    #     raise logging.error(f'Destroy error code: {use1_destroy["ResponseMetadata"]["HTTPStatusCode"]}')
    # else:
    #     logging.info(f'{use1_destroy["TerminatingInstances"][0]["InstanceId"]} has been destroyed')
    #
    # if len(api_check) >= 10:
    #     usw2_destroy = destroy_ec2.destroy_ec2_instance(
    #             [usw2_create.result()["Instances"][0]["InstanceId"]],
    #             app_contstants.Ec2Images.USW2.region
    #         )
    #
    #     if usw2_destroy["ResponseMetadata"]["HTTPStatusCode"] != 200:
    #         raise logging.error(f'Destroy error code: {usw2_destroy["ResponseMetadata"]["HTTPStatusCode"]}')
    #     else:
    #         logging.info(f'{usw2_destroy["TerminatingInstances"][0]["InstanceId"]} has been destroyed')


if __name__ == '__main__':
    asyncio.run(main())

logging.info(f'Total execution time: {round(perf_counter(), 2)} secs')
