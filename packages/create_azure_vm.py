from packages import AzureResources
from azure.mgmt.compute import ComputeManagementClient


async def create_vm(
        rg_name: str,
        vm_name: str,
        location: str,
        vm_size: str,
        ssh_user: str,
        ssh_pwd: str,
        nic_id: str) -> dict:
    """
    Creates Ubuntu 20.04.0-LTS virtual machine
    :param rg_name:
    :param vm_name:
    :param location:
    :param vm_size:
    :return:
    """
    compute_client = ComputeManagementClient(AzureResources.dev.get_az_cred, AzureResources.dev.get_az_sub_id)
    vm = compute_client.virtual_machines.begin_create_or_update(
        rg_name,
        vm_name,
        {
            "location": location,
            "storage_profile": {
                "image_reference": {
                    "publisher": 'canonical',
                    "offer": "0001-com-ubuntu-server-focal",
                    "sku": "20_04-lts-gen2",
                    "version": "latest"
                }
            },
            "hardware_profile": {
                "vm_size": vm_size
            },
            "os_profile": {
                "computer_name": vm_name,
                "admin_username": ssh_user,
                "admin_password": ssh_pwd
            },
            "network_profile": {
                "network_interfaces": [{
                    "id": nic_id,
                }]
            }
        }
    )
    return vm.result()
