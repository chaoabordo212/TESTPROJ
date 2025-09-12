# TESTPROJ Minimal Viable Prototype & Next Steps

## Minimal Viable Prototype (MVP)

### Features
- **CLI Application:** Simple command-line interface for setup and monitoring.
- **Network Scanning:** ARP scan using `scapy` to discover devices.
- **Whitelist Storage:** Store trusted MAC addresses in a JSON file.
- **Learning Phase:** Initial scan period to populate whitelist.
- **Alarm Mode:** Periodic scan; trigger action if unknown device detected.
- **Configurable Timeout & Action:** Read from config file or environment variables.
- **Basic Logging:** Log events to file or stdout.

### Example Directory Structure
```
TESTPROJ/
├── prototype.py
├── config.json
├── whitelist.json
├── requirements.txt
├── README.md
```

### Example `config.json`
```json
{
  "timeout": 3600,
  "action": "echo 'Unauthorized device detected!' >> alerts.log",
  "network_range": "192.168.1.0/24"
}
```

### Example `prototype.py`
```python
import scapy.all as scapy
import time
import json
import os
import logging
import subprocess

CONFIG_FILE = "config.json"
WHITELIST_FILE = "whitelist.json"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def load_whitelist():
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE) as f:
            return json.load(f)
    return []

def save_whitelist(whitelist):
    with open(WHITELIST_FILE, "w") as f:
        json.dump(whitelist, f, indent=2)

def scan_network(ip_range):
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return [element[1].hwsrc for element in answered_list]

def execute_action(action, message):
    logging.info(f"Action triggered: {message}")
    subprocess.run(action, shell=True)

def main():
    config = load_config()
    whitelist = load_whitelist()
    learning_phase_end = time.time() + config["timeout"]
    logging.info("Learning phase started...")
    while time.time() < learning_phase_end:
        devices = scan_network(config["network_range"])
        for mac in devices:
            if mac not in whitelist:
                whitelist.append(mac)
                logging.info(f"Whitelisted: {mac}")
        save_whitelist(whitelist)
        time.sleep(30)
    logging.info("Alarm mode started...")
    while True:
        devices = scan_network(config["network_range"])
        for mac in devices:
            if mac not in whitelist:
                execute_action(config["action"], f"Unauthorized device: {mac}")
        time.sleep(60)

if __name__ == "__main__":
    main()
```

## Next Steps & Roadmap

1. **Testing:**
   - Add unit tests for scanning, whitelist management, and config loading.
   - Test on different OSes and network setups.
2. **Error Handling:**
   - Improve robustness for missing privileges, network errors, malformed config.
3. **Advanced Storage:**
   - Migrate whitelist to SQLite for richer metadata and history.
4. **Notification Integrations:**
   - Add support for email, push notifications, Telegram, Twilio SMS.
5. **Web UI:**
   - Build a simple Flask/FastAPI dashboard for device management and logs.
6. **Dockerization:**
   - Create Dockerfile for easy deployment.
7. **System Service:**
   - Add systemd/service support for auto-restart and background running.
8. **Vendor Lookup:**
   - Integrate OUI lookup for MAC addresses.
9. **Documentation:**
   - Expand README and add usage examples.
10. **CI/CD:**
    - Add GitHub Actions for linting, testing, and build automation.

---
This prototype provides a foundation for further development. Each next step can be implemented incrementally to improve reliability, usability, and feature set.