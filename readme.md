# Check-API

This will deploy an instance/virtual machine in AWS and Azure.

REQUIRED PYTHON VERSION: 3.8

### Region deployment:
- AWS us-east-1
- AWS us-west-2 *
- Azure eastus

*Deployment to AWS us-east-2 will depend on the length of the name of the API that is checked.
*Any names that are 10 characters or longer will deploy to AWS USW2.

### Environment Variables
Set the following environment variables.
- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET
- AZURE_TENANT_ID
- SSH_KEY_USE1
- SSH_KEY_USW2
- VM_USER
- VM_PASS

### SDKs Used
- https://github.com/boto/boto3
- https://github.com/Azure/azure-sdk-for-python