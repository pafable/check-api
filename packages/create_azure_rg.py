from azure.mgmt.resource import ResourceManagementClient
from packages import AzureResources


def create_rg(region: str) -> str:
    resource_client = ResourceManagementClient(AzureResources.dev.get_az_cred, AzureResources.dev.get_az_sub_id)
    rg = resource_client.resource_groups.create_or_update(
        AzureResources.dev.rg_name,
        {
            "location": region
        }
    )
    return f'Provisioned resource group {rg.name} in {rg.location}'
