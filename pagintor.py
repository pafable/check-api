import boto3

REGION = 'eu-west-1'
MARKER = None


def get_policies(region: str) -> dict:
    iam = boto3.client('iam', region_name=region)
    paginator = iam.get_paginator('list_policies')

    iterator = paginator.paginate(
        PaginationConfig={
            'PageSize': 2,
            'StartingToken': MARKER
        }
    )
    return iterator


policies_iter = get_policies(REGION)
count = 1
for list_of_policies in policies_iter:
    for policy in list_of_policies['Policies']:
        print(f'{count}. policy: {policy["PolicyName"]}')
        count += 1
