import json
import os
import logging

WHITELIST_FILE = "whitelist.json"

def load_whitelist(path=WHITELIST_FILE):
    """Loads the whitelist from a JSON file."""
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in the whitelist file: {path}")
            return []
    return []

def save_whitelist(whitelist, path=WHITELIST_FILE):
    """Saves the whitelist to a JSON file."""
    try:
        with open(path, 'w') as f:
            json.dump(whitelist, f, indent=4)
    except IOError as e:
        logging.error(f"Error saving whitelist to {path}: {e}")

def add_to_whitelist(mac_address, whitelist):
    """Adds a MAC address to the whitelist if not already present."""
    if mac_address not in whitelist:
        whitelist.append(mac_address)
        logging.info(f"Added {mac_address} to whitelist.")
        return True
    return False

def remove_from_whitelist(mac_address, whitelist):
    """Removes a MAC address from the whitelist if present."""
    if mac_address in whitelist:
        whitelist.remove(mac_address)
        logging.info(f"Removed {mac_address} from whitelist.")
        return True
    return False
