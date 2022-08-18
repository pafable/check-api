from azure.identity import DefaultAzureCredential


cred = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
