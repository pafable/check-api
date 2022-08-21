from azure.mgmt.resource import ResourceManagementClient
from packages import AzureResources


def destroy_rg(rg_name: str):
    """
    Destroys Azure resource group
    :param rg_name: name of resource group
    :return:
    """
    resource_client = ResourceManagementClient(AzureResources.dev.get_az_cred, AzureResources.dev.get_az_sub_id)
    rg = resource_client.resource_groups.begin_delete(
        rg_name
    )
    return rg_name
