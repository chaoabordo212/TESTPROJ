# TESTPROJ Project Expansion and Implementation Proposal

This document elaborates on the TESTPROJ concept, analyzes potential implementations, and provides a roadmap for future development.

## 1. Project Idea Expansion

TESTPROJ is envisioned as a proactive tool for local network security, focusing on identifying and controlling device access. The primary goal is to establish a whitelist of trusted devices and alert the administrator to any unauthorized connection attempts.

**Key Aspects:**

*   **Simplicity and Efficiency:** Designed for users who want basic yet effective protection without complex configurations.
*   **Learning/Whitelisting Phase:** An initial phase where all currently connected devices are automatically added to the whitelist. This is crucial for easy setup without manual entry of MAC addresses.
*   **Alarm/Monitoring Phase:** After a defined `TIMEOUT` period, the system transitions to active monitoring mode. Any device that appears on the network and is not on the whitelist triggers a defined `ACTION`.
*   **Customizable Action:** Flexibility in defining the action (e.g., sending an email, running a script, logging an event) allows for customization to user needs.
*   **Target Audience:** Small offices/home offices (SOHO), individuals concerned about the security of their Wi-Fi or LAN network.

**Potential Use Cases:**

*   **Home Security:** Ensuring only family devices (phones, computers, smart devices) can connect.
*   **Small Business:** Preventing unauthorized devices from connecting to the company network.
*   **IoT Monitoring:** Controlling access for IoT devices and detecting "shadow IT" devices.

## 2. Evaluation of Possible Implementations

Implementing TESTPROJ requires addressing several key technical challenges:

### a) Network Scanning and Device Detection

*   **ARP Scanning:** The most common and effective method for discovering devices on the local network segment. It involves sending ARP Who-has requests for all IP addresses in the network range (e.g., 192.168.1.1-254) and collecting ARP responses containing MAC addresses.
*   **DHCP Snooping/Monitoring:** More complex, requiring access to the DHCP server or the ability to passively intercept DHCP traffic. Less practical for a standalone tool.
*   **Nmap:** A powerful network scanning tool that can be called via Python's `subprocess` module. Nmap uses various techniques, including ARP scanning, but is often overkill for simple presence detection.
*   **Passive Sniffing:** Using libraries like Scapy to passively intercept ARP, ICMP, or other protocols to discover active devices. This can be less intrusive but requires more resources and privileges.

**Choice:** ARP scanning using the Scapy library is likely the best balance of simplicity, efficiency, and flexibility for a Python implementation.

### b) Device Identification and Storage

*   **MAC Address:** The most reliable identifier for a device on a local network. Each network adapter is assigned a unique MAC address.
*   **IP Address:** Dynamic IP addresses (assigned via DHCP) make the IP address less reliable for unique identification over time. It can be used as a secondary identifier or to track address changes for a known MAC.
*   **Hostname:** Can be obtained via DNS queries but is not always available or reliable for all devices.

**Whitelist Storage:**

*   **JSON/YAML File:** A simple format for storing a list of MAC addresses and optional device names. Easy to read and write in Python.
*   **SQLite Database:** A more robust solution for a larger number of devices or the need for additional data (e.g., last seen time, IP history). Built into Python.

**Choice:** For the initial version, a JSON file is sufficient. For more advanced features, transitioning to SQLite is recommended.

### c) Time Management and Monitoring Loop

*   **`TIMEOUT`:** A simple timer (e.g., `time.sleep()` in a loop) can be used to implement the `TIMEOUT` period before switching to alarm mode.
*   **Periodic Scanning:** In alarm mode, the system must periodically scan the network. This can be achieved within an infinite loop with a `time.sleep()` call between scans.

### d) Action Triggering Mechanism (`ACTION`)

*   **Executing Shell Commands:** Python's `subprocess` module allows for the execution of external commands or scripts. This is the most flexible approach for `ACTION`.
*   **Sending Email:** The `smtplib` module for sending emails via an SMTP server.
*   **API Calls:** Using the `requests` library to send notifications via services like Pushbullet, Pushover, Telegram bot API, or an SMS gateway.

## 3. Existing Tools and Solutions

Several tools partially or fully meet the objectives of TESTPROJ:

*   **ARPwatch:** A classic Unix tool that monitors ARP activity and warns of changes in MAC-IP mappings, which can indicate new devices or ARP spoofing. Robust but CLI-oriented.
*   **Nmap:** While primarily a scanner, Nmap can be scripted to detect new hosts. It is not an out-of-the-box solution for continuous monitoring.
*   **Fing:** A popular mobile and desktop application for network scanning and device identification. It offers detailed information but is not open-source for customization.
*   **Netdata / PRTG / Zabbix:** More complex network monitoring tools that can track host presence but are overkill for the simple task of TESTPROJ.
*   **Router-based Intrusion Detection:** Some advanced routers have built-in functions for detecting unknown devices, but they are often limited.
*   **Python Projects on GitHub:** Various open-source projects use Scapy for network scanning, but rarely with a focus on simple whitelisting and alarming as the primary function.

TESTPROJ stands out for its simplicity and focus on automatic whitelist generation and customizable actions, targeting users who need a specific solution to this problem without the complexity of full-fledged network monitoring tools.

## 4. Python Implementation/Integration

### a) Libraries

*   **`scapy`:** Essential for ARP scanning. Allows for the creation and sending of ARP packets, as well as intercepting responses.
    *   *Example:* `ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.0/24"), timeout=2)`
*   **`json` / `sqlite3`:** For storing the configuration and whitelist.
*   **`time`:** For implementing `TIMEOUT` and pauses between scans.
*   **`subprocess`:** For executing external commands defined in `ACTION`.
*   **`logging`:** For recording events and errors.
*   **`smtplib` / `requests`:** Optional, for more advanced notification mechanisms.

### b) Basic Code Structure (Pseudocode)

```python
import scapy.all as scapy
import time
import json
import os
import logging
# (other imports for ACTION, e.g., smtplib, subprocess)

# Configuration (can be from a file or environment variables)
TIMEOUT = 3600 # seconds for the learning phase
ACTION = "echo 'Unauthorized device detected!' >> alerts.log" # Example action
WHITELIST_FILE = "whitelist.json"

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_network_info():
    # Function to get the local network's IP range
    # E.g., 192.168.1.0/24
    # Can use the `netifaces` library or `ipconfig`/`ifconfig` commands
    return "192.168.1.0/24"

def scan_network(ip_range):
    # Scans the network and returns a list of active MAC addresses
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices = []
    for element in answered_list:
        devices.append(element[1].hwsrc) # MAC address
    return devices

def load_whitelist():
    if os.path.exists(WHITELIST_FILE):
        with open(WHITELIST_FILE, 'r') as f:
            return json.load(f)
    return []

def save_whitelist(whitelist):
    with open(WHITELIST_FILE, 'w') as f:
        json.dump(whitelist, f, indent=4)

def execute_action(message):
    logging.info(f"Executing action: {message}")
    # Here the ACTION string is executed, e.g.:
    # subprocess.run(ACTION, shell=True)
    # Or a call to smtplib, requests, etc.
    pass # Simulate action

def main():
    whitelist = load_whitelist()
    network_range = get_network_info()
    learning_phase_end = time.time() + TIMEOUT

    logging.info("TESTPROJ started. Learning phase...")

    # Learning phase
    while time.time() < learning_phase_end:
        current_devices = scan_network(network_range)
        for mac in current_devices:
            if mac not in whitelist:
                whitelist.append(mac)
                logging.info(f"Added new device to whitelist: {mac}")
        save_whitelist(whitelist)
        time.sleep(30) # Scan every 30 seconds during the learning phase

    logging.info(f"Learning phase finished. Whitelist contains {len(whitelist)} devices.")
    logging.info("Switching to alarm mode...")

    # Alarm mode
    while True:
        current_devices = scan_network(network_range)
        for mac in current_devices:
            if mac not in whitelist:
                alert_message = f"UNAUTHORIZED DEVICE DETECTED: {mac}"
                logging.warning(alert_message)
                execute_action(alert_message)
        time.sleep(60) # Scan every 60 seconds in alarm mode

if __name__ == "__main__":
    main()
```

## 5. Ideas for Further Development

1.  **Configuration File:** Instead of hardcoding `TIMEOUT` and `ACTION` variables, implement reading the configuration from a `config.ini`, `.env`, or YAML file.
2.  **Web Interface:** Develop a simple web interface (using Flask or FastAPI) to:
    *   Display currently connected devices.
    *   Manage the whitelist (manually add/remove MAC addresses).
    *   View logs and notifications.
    *   Configure `TIMEOUT` and `ACTION`.
3.  **Advanced Device Identification:**
    *   Look up MAC addresses for the manufacturer (OUI - Organizationally Unique Identifier) to display the device vendor.
    *   Attempt to resolve hostnames for detected IP addresses.
4.  **Persistent Data:** Use an SQLite database to store:
    *   The whitelist (with additional information like device name, last seen, IP history).
    *   Logs of unauthorized device detections.
5.  **Improved Notification Mechanisms:**
    *   Integration with a Telegram bot.
    *   Integration with push notification services (e.g., Pushover, Pushbullet).
    *   Sending SMS messages (via Twilio or similar services).
6.  **"Forget Device" Functionality:** Allow for the removal of devices from the whitelist.
7.  **Detailed Logging:** Record more details about detected devices, including IP address, detection time, etc.
8.  **Automatic Restart:** Configure the application as a `systemd` service on Linux to automatically start on system boot and recover from errors.
9.  **Dockerization:** Package the application in a Docker container for easier deployment and isolation.
10. **Tests:** Implement unit and integration tests for key components.
11. **Improved Stability:** Better error handling (e.g., network issues, missing privileges).
12. **Known Device Alerts:** Detect changes (e.g., a known IP's MAC address changes, or vice versa) for whitelisted devices, which could indicate ARP spoofing.
