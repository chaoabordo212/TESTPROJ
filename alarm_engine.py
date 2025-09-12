import time
import logging
import subprocess

from network_scanner import scan_network
from whitelist_manager import load_whitelist, save_whitelist, add_to_whitelist

class AlarmEngine:
    def __init__(self, config):
        self.config = config
        self.whitelist = load_whitelist()
        self.learning_phase_end = time.time() + self.config.get("timeout", 3600)
        logging.info("AlarmEngine initialized.")

    def _execute_action(self, mac_address):
        action_command = self.config.get("action", "echo 'Unauthorized device detected! MAC: {mac}'").format(mac=mac_address)
        logging.warning(f"Executing action for unauthorized device: {mac_address}")
        try:
            subprocess.run(action_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Action command failed with error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred while executing action: {e}")

    def run(self):
        logging.info("TESTPROJ started.")
        self._learning_phase()
        self._alarm_mode()

    def _learning_phase(self):
        logging.info("Entering learning phase...")
        while time.time() < self.learning_phase_end:
            logging.info("Scanning network during learning phase...")
            current_devices = scan_network(self.config.get("network_range", "192.168.1.0/24"))
            for mac in current_devices:
                if add_to_whitelist(mac, self.whitelist):
                    save_whitelist(self.whitelist)
            time.sleep(self.config.get("scan_interval_learning", 15))
        logging.info(f"Learning phase finished. Whitelist contains {len(self.whitelist)} devices.")
        logging.info("Saving final whitelist from learning phase.")
        save_whitelist(self.whitelist) # Ensure whitelist is saved after learning phase

    def _alarm_mode(self):
        logging.info("Entering alarm mode...")
        while True:
            logging.info("Scanning network during alarm mode...")
            current_devices = scan_network(self.config.get("network_range", "192.168.1.0/24"))
            for mac in current_devices:
                if mac not in self.whitelist:
                    self._execute_action(mac)
            time.sleep(self.config.get("scan_interval_alarm", 30))
