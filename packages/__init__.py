from packages.app_contstants import ApiEndpoint, AwsResources, AzureResources
from packages.create_azure_network import create_ip, create_nic, create_subnet, create_vnet
from packages.create_azure_rg import create_rg
from packages.create_azure_vm import create_vm
from packages.destroy_azure_vm import destroy_vm
from packages.create_aws_ec2 import create_ec2_instance
from packages.destroy_aws_ec2 import destroy_ec2_instance
