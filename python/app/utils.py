import hashlib
import re
import ipaddress
import logging
from logging.config import dictConfig

# Logging configuration
logging_config = dict(
    version=1,
    formatters={
        'default': {
            'format': '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S %z',
        },
    },
    handlers={
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        },
    },
    root={
        'level': 'INFO',
        'handlers': ['console'],
    },
)

dictConfig(logging_config)

logger = logging.getLogger(__name__)

# Function to generate a hash
def generate_hash(data, secret_key):
    hash_obj = hashlib.sha256() # Create a hash object
    hash_obj.update(f"{data}-{secret_key}".encode()) # Update the hash object with the data and secret key
    return hash_obj.hexdigest() # Return the hex digest of the hash object

def validate_inputs(username, ip, hash_value):
    # Check if username, ip, and hash_value are provided
    if not username or not ip or not hash_value:
        return False, "Missing inputs"

    # Validate username
    if not re.match("^[a-zA-Z0-9_-]*$", username):
        return False, "Invalid username"

    # Validate IP address
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return False, "Invalid IP address"

    # Validate hash (example: checking length and allowed characters)
    if not re.match("^[a-f0-9]{64}$", hash_value):
        return False, "Invalid hash"

    return True, "Valid inputs"