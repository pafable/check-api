from packages import (
    ApiEndpoint,
    AwsResources,
    AzureResources,
    create_ec2_instance,
    create_ip,
    create_nic,
    create_rg,
    create_subnet,
    create_vm,
    create_vnet,
    destroy_rg,
    destroy_vm,
    destroy_ec2_instance
)
from time import perf_counter
from typing import Final
from urllib.request import urlopen
import asyncio
import json
import logging
import os
import ssl
import sys

SUFFIX: Final = ('test-instance',)
USE1_INSTANCE_NAME: Final = (f'{AwsResources.dev.region}-{SUFFIX[0]}',)
USW2_INSTANCE_NAME: Final = (f'{AwsResources.prod.region}-{SUFFIX[0]}',)
EUS_RG_NAME: Final = (f'{AzureResources.dev.location}-{SUFFIX[0]}-rg',)
EUS_VM_NAME: Final = (f'{AzureResources.dev.location}-{SUFFIX[0]}',)

logging.basicConfig(level=logging.INFO, format='[ %(levelname)s ] %(message)s')

# This is needed to interact with HTTPS websites
ssl._create_default_https_context = ssl._create_unverified_context


class AwsInstance:
    def __init__(self, region: str, ami: str, instance_type: str, instance_name: str, ssh_key: str):
        self.region = region
        self.ami = ami
        self.instance_type = instance_type
        self.instance_name = instance_name
        self.ssh_key = ssh_key

    def create(self):
        return create_ec2_instance(
            self.region,
            self.ami,
            self.instance_type,
            self.instance_name,
            self.ssh_key,
            1,
            1
        )

    @staticmethod
    def destroy(instance_id: str, region: str):
        return destroy_ec2_instance(
            instance_id,
            region
        )


class AzureInstance:
    def __init__(self, rg_nam: str, vm_name: str, location: str, vm_size: str, vm_user: str, vm_pass: str, nic: str):
        self.rg_name = rg_nam
        self.location = location
        self.vm_name = vm_name
        self.vm_size = vm_size
        self.vm_user = vm_user
        self.vm_pass = vm_pass
        self.nic = nic

    def create(self):
        return create_vm(
            self.rg_name,
            self.vm_name,
            self.location,
            self.vm_size,
            self.vm_user,
            self.vm_pass,
            self.nic
        )

    @staticmethod
    def create_vnet_(rg_name: str):
        return create_vnet(rg_name)

    @staticmethod
    def create_sub_(rg_name: str):
        return create_subnet(rg_name)

    @staticmethod
    def create_ip_(rg_name: str):
        return create_ip(rg_name)

    @staticmethod
    def create_nic_(rg_name: str, subnet_id: str, ip_addr_id: str):
        return create_nic(
            rg_name,
            subnet_id,
            ip_addr_id
        )

    @staticmethod
    def destroy_rg_(rg_name: str):
        return destroy_rg(rg_name)

    @staticmethod
    def destroy_vm_(rg_name: str, vm_name: str):
        return destroy_vm(
            rg_name,
            vm_name
        )


async def main():
    try:
        api_resp = urlopen(ApiEndpoint.API1.url)
        api_resp = json.loads(api_resp.read().decode())
        api_check = api_resp['entries'][0]['API']

        logging.info(f'API: {api_check}')

        # AWS EC2 instance creation in us-east-1
        aws_use1 = AwsInstance(
            AwsResources.dev.region,
            AwsResources.dev.ami_id,
            AwsResources.dev.instance_type,
            USE1_INSTANCE_NAME[0],
            os.environ['SSH_KEY_USE1']
        )

        aws_use1_instance = asyncio.create_task(
            aws_use1.create()
        )

        if len(api_check) >= 15:
            # AWS EC2 instance creation in us-west-2
            aws_usw2 = AwsInstance(
                AwsResources.prod.region,
                AwsResources.prod.ami_id,
                AwsResources.prod.instance_type,
                USW2_INSTANCE_NAME[0],
                os.environ['SSH_KEY_USW2']
            )

            aws_usw2_instance = asyncio.create_task(
                aws_usw2.create()
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
            AzureInstance.create_vnet_(azure_eus_create_rg.result())
        )

        # Azure subnet creation
        azure_eus_create_sub = asyncio.create_task(
            AzureInstance.create_sub_(azure_eus_create_rg.result())
        )

        # Azure ip address creation
        azure_eus_create_ip = asyncio.create_task(
            AzureInstance.create_ip_(azure_eus_create_rg.result())
        )

        await azure_eus_create_vnet
        logging.info('created azure vnet'.upper())

        await azure_eus_create_sub
        logging.info('created azure subnet'.upper())

        await azure_eus_create_ip
        logging.info('created azure ip address'.upper())

        # Azure nic creation
        azure_eus_create_nic = asyncio.create_task(
            AzureInstance.create_nic_(
                azure_eus_create_rg.result(),
                azure_eus_create_sub.result().id,
                azure_eus_create_ip.result().id
            )
        )

        await azure_eus_create_nic
        logging.info('created azure nic'.upper())

        # Azure vm creation in eastus
        azure_eus = AzureInstance(
            azure_eus_create_rg.result(),
            EUS_VM_NAME[0],
            AzureResources.dev.location,
            AzureResources.dev.vm_size,
            os.environ['VM_USER'],
            os.environ['VM_PASS'],
            azure_eus_create_nic.result().id
        )

        azure_eus_vm = asyncio.create_task(
            azure_eus.create()
        )

        await aws_use1_instance and await azure_eus_vm

        logging.info(f'Azure EUS Instance: {azure_eus_vm.result().name} and ID: {azure_eus_vm.result().vm_id}')
        logging.info(f'AWS USE1 Instance: {aws_use1_instance.result()["Instances"][0]["InstanceId"]}')

        if len(api_check) >= 15:
            await aws_usw2_instance
            logging.info(f'AWS USW2 Instance: {aws_usw2_instance.result()["Instances"][0]["InstanceId"]}')

        if sys.argv[1] == 'test':
            DESTROY_MSG: Final = """

                    TEST COMPLETE
                    DESTROYING INSTANCES!!!

            """
            logging.info(DESTROY_MSG)

            aws_use1_destroy = AwsInstance.destroy(
                aws_use1_instance.result()["Instances"][0]["InstanceId"],
                AwsResources.dev.region
            )

            if aws_use1_destroy["ResponseMetadata"]["HTTPStatusCode"] != 200:
                raise logging.error(f'Destroy error code: {aws_use1_destroy["ResponseMetadata"]["HTTPStatusCode"]}')
            else:
                logging.info(f'AWS USE1 {aws_use1_destroy["TerminatingInstances"][0]["InstanceId"]} has been destroyed')

            if len(api_check) >= 15:
                aws_usw2_destroy = AwsInstance.destroy(
                    aws_usw2_instance.result()["Instances"][0]["InstanceId"],
                    AwsResources.prod.region
                )

                if aws_usw2_destroy["ResponseMetadata"]["HTTPStatusCode"] != 200:
                    raise logging.error(f'Destroy error code: {aws_usw2_destroy["ResponseMetadata"]["HTTPStatusCode"]}')
                else:
                    logging.info(
                      f'AWS USW2 {aws_usw2_destroy["TerminatingInstances"][0]["InstanceId"]} has been destroyed'
                     )

            AzureInstance.destroy_rg_(
                azure_eus_create_rg.result()
            )
            logging.info(f'Azure EUS {EUS_VM_NAME[0]} has been destroyed')

    except Exception as e:
        logging.error(e.with_traceback())

if __name__ == '__main__':
    asyncio.run(main())

logging.info(f'Total execution time: {round(perf_counter(), 2)} secs')
