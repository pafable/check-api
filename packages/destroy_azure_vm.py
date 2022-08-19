from packages import AzureResources
from azure.mgmt.compute import ComputeManagementClient

compute_client = ComputeManagementClient(AzureResources.dev.get_az_cred, AzureResources.dev.get_az_sub_id)


def destroy_vm(rg_name: str, vm_name: str) -> dict:
    """
    Destroys an Azure virtual machine
    :param rg_name: resource group name
    :param vm_name: virtual machine name
    :return:
    """
    vm = compute_client.virtual_machines.begin_delete(
        rg_name,
        vm_name
    )

    return vm.result()
