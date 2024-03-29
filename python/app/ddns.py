

def createDDNS():
    # Get the request data
    data = request.get_json()
    # Get the subdomain and IP address from the request data
    subdomain = data['subdomain']
    ip = data['ip']
    client_hash = data.get('hash')

    # Validate the request data
    is_valid, message = validate_inputs(subdomain, ip, client_hash)
    if not is_valid:
        return jsonify({'error': message}), 400

    # Remove the hash from data to compare only the relevant parts
    data.pop('hash', None)
    print(data)

    # Generate server-side hash
    server_hash = generate_hash((f"{data['subdomain']}-{data['ip']}"), secret_key)
    print(f"Client Hash: {client_hash}") # Print the client hash
    print(f"Server Hash: {server_hash}") # Print the server hash

    # Compare client and server hashes
    if client_hash != server_hash:
        return jsonify({"error": "Hash mismatch"}), 400

    # Fetch existing DNS records
    get_response = requests.get(domain_record_get, headers=headers)
    if get_response.status_code != 200:
        return jsonify({"error": "Failed to fetch existing DNS records"}), get_response.status_code

    # Get the existing records
    existing_records = get_response.json().get('data', [])
    record_id = None # Initialize record ID

    # Check if the record already exists
    for record in existing_records:
        if record['name'] == subdomain and record['type'] == 'A':
            record_id = record['id']
            break

    # Construct the request payload
    payload = {
        "type": "A",
        "name": f"{subdomain}",
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
        except: 
            return jsonify({"error": "Failed to update DNS record"}), 500
    else:
        try:
            # Create new record
            post_response = requests.post(domain_record_create, json=payload, headers=headers)
            response_content = post_response.json()
        except:
            return jsonify({"error": "Failed to create DNS record"}), 500
    

    # Return the response
    response_content.pop('name', None) # Remove the DDNS subdomain from the response
    return jsonify({"response": response_content}), 200
