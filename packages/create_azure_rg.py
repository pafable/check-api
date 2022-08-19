from azure.mgmt.resource import ResourceManagementClient
from packages import AzureResources


async def create_rg(rg_name: str, region: str) -> str:
    resource_client = ResourceManagementClient(AzureResources.dev.get_az_cred, AzureResources.dev.get_az_sub_id)
    rg = resource_client.resource_groups.create_or_update(
        rg_name,
        {
            "location": region
        }
    )
    return rg.name
