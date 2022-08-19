from azure.mgmt.network import NetworkManagementClient
from packages import AzureResources

network_client = NetworkManagementClient(AzureResources.dev.get_az_cred, AzureResources.dev.get_az_sub_id)


async def create_vnet(rg: str) -> str:
    """
    Creates an Azure vnet
    :param rg:
    :return:
    """
    vnet = network_client.virtual_networks.begin_create_or_update(
        rg,
        AzureResources.dev.vnet_name,
        {
            "location": AzureResources.dev.location,
            "address_space": {
                "address_prefixes": ["10.0.0.0/16"]
            }
        }
    )

    return vnet.result()


async def create_subnet(rg: str) -> str:
    """
    Creates an Azure subnet
    :param rg:
    :return:
    """
    subnet = network_client.subnets.begin_create_or_update(
        rg,
        AzureResources.dev.vnet_name,
        AzureResources.dev.subnet_name,
        {"address_prefix": "10.0.0.0/24"}
    )
    subnet_result = subnet.result()
    return subnet_result


async def create_ip(rg: str) -> str:
    """
    Creates an Azure ip address
    :param rg:
    :return:
    """
    ip = network_client.public_ip_addresses.begin_create_or_update(
        rg,
        AzureResources.dev.ip_name,
        {
            "location": AzureResources.dev.location,
            "sku": {"name": "Standard"},
            "public_ip_allocation_method": "Static",
            "public_ip_address_version": "IPV4"
        }
    )

    return ip.result()


async def create_nic(rg: str, subnet_id: str, ip_address_id: str) -> str:
    """
    Creates an Azure network interface
    :param rg:
    :param subnet_id:
    :param ip_address_id:
    :return:
    """
    nic = network_client.network_interfaces.begin_create_or_update(
        rg,
        AzureResources.dev.nic_name,
        {
            "location": AzureResources.dev.location,
            "ip_configurations": [{
                "name": AzureResources.dev.ip_conf_name,
                "subnet": {"id": subnet_id},
                "public_ip_address": {"id": ip_address_id}
            }]
        }
    )

    return nic.result()
