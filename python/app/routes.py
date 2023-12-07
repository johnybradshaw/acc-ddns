from flask import jsonify, request
import requests, logging
from .utils import generate_hash, validate_inputs, logger
from .config import secret_key, linode_api_key, domainId, headers, domain_get, domain_record_get, domain_record_create, domain_record_update

# Assuming the createDDNS function and other route functions are here
def createDDNS():
    # Get the request data
    data = request.get_json()
    # Get the username and IP address from the request data
    username = data['username']
    ip = data['ip']
    client_hash = data.get('hash')

    # Validate the request data
    is_valid, message = validate_inputs(username, ip, client_hash)
    if not is_valid:
        logger.error(f"[{request.remote_addr}] Invalid request data: {message}")
        return jsonify({'error': message}), 400

    # Remove the hash from data to compare only the relevant parts
    data.pop('hash', None)
    logger.info(f"[{request.remote_addr}] Request data: {data}")

    # Generate server-side hash
    server_hash = generate_hash((f"{data['username']}-{data['ip']}"), secret_key)

    # Compare client and server hashes
    if client_hash != server_hash:
        logger.error(f"[{request.remote_addr}] Hash mismatch: {client_hash} != {server_hash}")
        return jsonify({"error": "Hash mismatch"}), 400

    # Fetch existing DNS records
    get_response = requests.get(domain_record_get, headers=headers)
    if get_response.status_code != 200:
        logger.error(f"[{request.remote_addr}] Failed to fetch existing DNS records: {get_response.json()}")
        return jsonify({"error": "Failed to fetch existing DNS records"}), get_response.status_code

    # Get the existing records
    existing_records = get_response.json().get('data', [])
    record_id = None # Initialize record ID

    # Check if the record already exists
    for record in existing_records:
        if record['name'] == username and record['type'] == 'A':
            record_id = record['id']
            break

    # Construct the request payload
    payload = {
        "type": "A",
        "name": f"{username}",
        "target": f"{ip}",
        "ttl_sec": 30
    }
    
    # Update if record exists, else add a new record
    if record_id:
        # Update existing record
        put_url = f"{domain_record_update}/{record_id}"
        try:
            put_response = requests.put(put_url, json=payload, headers=headers)
            response_content = put_response.json()
            logger.info(f"[{request.remote_addr}] Updated DNS record: {response_content}")
        except:
            logger.error(f"[{request.remote_addr}] Failed to update DNS record: {put_response.json()}") 
            return jsonify({"error": "Failed to update DNS record"}), 500
    else:
        try:
            # Create new record
            post_response = requests.post(domain_record_create, json=payload, headers=headers)
            response_content = post_response.json()
            logger.info(f"[{request.remote_addr}] Created DNS record: {response_content}")
        except:
            logger.error(f"[{request.remote_addr}] Failed to create DNS record: {post_response.json()}")
            return jsonify({"error": "Failed to create DNS record"}), 500
    
    # Return the response
    response_content.pop('name', None) # Remove the DDNS username from the response
    return jsonify({"response": response_content}), 200

# Update the DDNS record
def updateDDNS():
    logger.info(f"[{request.remote_addr}] Update DNS record")
    return jsonify({"error": "Not implemented"}), 501

# Delete the DDNS record
def deleteDDNS():
    logger.info(f"[{request.remote_addr}] Delete DNS record")
    return jsonify({"error": "Not implemented"}), 501

def pingDDNS():
    try:
        logger.info(f"[{request.remote_addr}] Fetching existing DNS records from domain ID {domainId}...")
        # Check if the domain exists and the user has access to it
        get_response = requests.get(domain_get, headers=headers)
        if get_response.status_code != 200:
            logger.error(f"[{request.remote_addr}] Failed to fetch existing DNS records: {get_response.json()}")
            return jsonify({"error": "Failed to fetch existing DNS records"}), get_response.status_code
        logger.info(get_response.json())
    except:
        logger.error(f"[{request.remote_addr}] Failed to fetch existing DNS records: {get_response.json()}")
        return jsonify({"error": "Failed to fetch existing DNS records"}), 500
    
    return jsonify({"response": "pong"}), 200

# Bind routes to app after function definitions
def init_app(app):
    # Log the startup of the app
    logger.info("Initializing routes...")
    # Log the secret key, Linode API key, and domain ID but hide most of the characters
    logger.info(f"Secret key: {secret_key[:4]}{'*'*(len(secret_key)-4)} [{len(secret_key)}]")
    logger.info(f"Linode API key: {linode_api_key[:4]}{'*'*(len(linode_api_key)-4)} [{len(linode_api_key)}]")
    logger.info(f"Domain ID: {domainId[:4]}{'*'*(len(domainId)-4)} [{len(domainId)}]")
    # Bind the createDDNS function to the /create route
    app.add_url_rule('/create', view_func=createDDNS, methods=['POST'])
    # Bind the updateDDNS function to the /update route
    app.add_url_rule('/update', view_func=updateDDNS, methods=['PUT'])
    # Bind the deleteDDNS function to the /delete route
    app.add_url_rule('/delete', view_func=deleteDDNS, methods=['DELETE'])
    # Bind the pingDDNS function to the /ping route
    app.add_url_rule('/ping', view_func=pingDDNS, methods=['GET'])

