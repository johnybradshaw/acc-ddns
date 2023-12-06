import os

# Load environment variables
secret_key = os.environ.get('SECRET_KEY', 'default_secret')
linode_api_key = os.environ.get('LINODE_API_KEY', 'default_linode_api_key')
domainId = os.environ.get('DOMAIN_ID', 'default_domain_id')

# Akamai Connected Cloud
recordId = "" # setting for use later
domain_get = f"https://api.linode.com/v4/domains/{domainId}" # GET
domain_record_get = f"https://api.linode.com/v4/domains/{domainId}/records" # GET
domain_record_create = f"https://api.linode.com/v4/domains/{domainId}/records" # POST
domain_record_update = f"https://api.linode.com/v4/domains/{domainId}/records/{recordId}" # PUT
domain_record_delete = f"https://api.linode.com/v4/domains/{domainId}/records/{recordId}" # DELETE

# Other configuration variables
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {linode_api_key}"
}
