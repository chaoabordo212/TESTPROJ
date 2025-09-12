import json
import logging

DEFAULT_CONFIG_PATH = "config.json"

def load_config(path=DEFAULT_CONFIG_PATH):
    """Loads the configuration from a JSON file."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error(f"Configuration file not found at {path}.")
        # Create a default one for the user
        default_config = {
            "timeout": 60,
            "action": "echo 'Unauthorized device detected! MAC: {mac}' >> alerts.log",
            "network_range": "192.168.1.0/24",
            "scan_interval_learning": 15,
            "scan_interval_alarm": 30
        }
        with open(path, 'w') as f:
            json.dump(default_config, f, indent=4)
        logging.info(f"A default config.json has been created. Please review it and adjust 'network_range' to match your network.")
        return default_config
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON in the configuration file: {path}")
        return None
