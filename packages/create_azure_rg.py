from azure.mgmt.resource import ResourceManagementClient
from packages import AzureResources


async def create_rg(rg_name: str, location: str) -> str:
    """
    Creates Azure resource group
    :param rg_name: name of resource group
    :param location: Azure location
    :return:
    """
    resource_client = ResourceManagementClient(AzureResources.dev.get_az_cred, AzureResources.dev.get_az_sub_id)
    rg = resource_client.resource_groups.create_or_update(
        rg_name,
        {
            "location": location
        }
    )
    return rg.name
