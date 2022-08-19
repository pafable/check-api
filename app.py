from packages import ApiEndpoint, \
    AwsResources, \
    AzureResources, \
    create_ec2_instance, \
    create_ip, \
    create_nic, \
    create_rg, \
    create_subnet, \
    create_vm, \
    create_vnet, \
    destroy_vm, \
    destroy_ec2_instance
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
EUS_RG_NAME: Final = (f'{AzureResources.dev.location}-{SUFFIX[0]}-rg',)
EUS_VM_NAME: Final = (f'{AzureResources.dev.location}-{SUFFIX[0]}',)

logging.basicConfig(level=logging.INFO, format='[ %(levelname)s ] %(message)s')

# This is needed to interact with HTTPS websites
ssl._create_default_https_context = ssl._create_unverified_context


async def main():
    try:
        api_resp = urlopen(ApiEndpoint.API1.url)
        api_resp = json.loads(api_resp.read().decode())
        api_check = api_resp['entries'][0]['API']

        logging.info(f'API: {api_check}')

        # AWS EC2 instance creation in us-east-1
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

        if len(api_check) >= 15:
            # AWS EC2 instance creation in us-west-2
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

        # Azure resource group creation
        azure_eus_create_rg = asyncio.create_task(
            create_rg(
                EUS_RG_NAME[0],
                AzureResources.dev.location
            )
        )
        await azure_eus_create_rg

        # Azure vnet creation
        azure_eus_create_vnet = asyncio.create_task(
            create_vnet(azure_eus_create_rg.result())
        )

        # Azure subnet creation
        azure_eus_create_sub = asyncio.create_task(
            create_subnet(azure_eus_create_rg.result())
        )

        # Azure ip address creation
        azure_eus_create_ip = asyncio.create_task(
            create_ip(azure_eus_create_rg.result())
        )

        await azure_eus_create_vnet
        logging.info('created azure vnet')

        await azure_eus_create_sub
        logging.info('created azure subnet')

        await azure_eus_create_ip
        logging.info('created azure ip address')

        # Azure nic creation
        azure_eus_create_nic = asyncio.create_task(
            create_nic(
                azure_eus_create_rg.result(),
                azure_eus_create_sub.result().id,
                azure_eus_create_ip.result().id
            )
        )

        await azure_eus_create_nic
        logging.info('created azure nic')

        # Azure vm creation in eastus
        azure_eus_create_vm = asyncio.create_task(
            create_vm(
                azure_eus_create_rg.result(),
                EUS_VM_NAME[0],
                AzureResources.dev.location,
                AzureResources.dev.vm_size,
                os.environ['VM_USER'],
                os.environ['VM_PASS'],
                azure_eus_create_nic.result().id
            )
        )

        await aws_use1_create
        await azure_eus_create_vm
        logging.info(f'Azure EUS Instance: {azure_eus_create_vm.result().name} and ID: {azure_eus_create_vm.result().vm_id}')
        logging.info(f'AWS USE1 Instance: {aws_use1_create.result()["Instances"][0]["InstanceId"]}')

        if len(api_check) >= 15:
            await aws_usw2_create
            logging.info(f'AWS USW2 Instance: {aws_usw2_create.result()["Instances"][0]["InstanceId"]}')

        '''
        UNCOMMENT LINES BELOW TO TERMINATE INSTANCES
        FOR TESTING ONLY!
        '''
        #
        # DESTROY_MSG = """
        #
        #         DESTROYING INSTANCES!!!
        #
        # """
        # logging.info(DESTROY_MSG)
        #
        # aws_use1_destroy = destroy_ec2_instance(
        #     [aws_use1_create.result()["Instances"][0]["InstanceId"]],
        #     AwsResources.dev.region
        # )
        #
        # if aws_use1_destroy["ResponseMetadata"]["HTTPStatusCode"] != 200:
        #     raise logging.error(f'Destroy error code: {aws_use1_destroy["ResponseMetadata"]["HTTPStatusCode"]}')
        # else:
        #     logging.info(f'AWS USE1 {aws_use1_destroy["TerminatingInstances"][0]["InstanceId"]} has been destroyed')
        #
        # if len(api_check) >= 15:
        #     aws_usw2_destroy = destroy_ec2_instance(
        #         [aws_usw2_create.result()["Instances"][0]["InstanceId"]],
        #         AwsResources.prod.region
        #     )
        #
        #     if aws_usw2_destroy["ResponseMetadata"]["HTTPStatusCode"] != 200:
        #         raise logging.error(f'Destroy error code: {aws_usw2_destroy["ResponseMetadata"]["HTTPStatusCode"]}')
        #     else:
        #         logging.info(
        #           f'AWS USW2 {aws_usw2_destroy["TerminatingInstances"][0]["InstanceId"]} has been destroyed'
        #          )
        #
        # azure_eus_destroy = destroy_vm(
        #     azure_eus_create_rg.result(),
        #     EUS_VM_NAME[0]
        # )
        # logging.info(f'Azure EUS {EUS_VM_NAME[0]} has been destroyed')

    except Exception as e:
        logging.error(e)

if __name__ == '__main__':
    asyncio.run(main())

logging.info(f'Total execution time: {round(perf_counter(), 2)} secs')
