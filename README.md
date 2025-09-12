# TESTPROJ

## Description
TESTPROJ is a network monitoring tool designed to secure your local network by identifying and whitelisting trusted devices. After an initial learning phase, it transitions into an alarm mode, alerting you to any unauthorized devices attempting to connect.

## Features
*   **Local Network Scanning:** Actively scans the local network to discover connected devices.
*   **Automatic Whitelisting:** Automatically adds all devices found during the initial scan to a trusted whitelist.
*   **Configurable Alarm Mode:** Transitions into an alarm state after a specified `TIMEOUT` period.
*   **Unauthorized Device Detection:** In alarm mode, continuously monitors the network for devices not present in the whitelist.
*   **Customizable Action:** Triggers a predefined `ACTION` when an unauthorized device is detected.

## Configuration
The behavior of TESTPROJ can be customized using the following variables:

*   **`TIMEOUT`**: An integer representing the duration (e.g., in seconds, minutes, or hours, depending on implementation) after which the system transitions from the initial scanning/whitelisting phase to the alarm mode.
    *   *Example:* `TIMEOUT = 3600` (for 1 hour)
*   **`ACTION`**: A string or command defining the action to be taken when an unauthorized device is detected. This could be logging, sending an email, triggering an alert, or executing a script.
    *   *Example:* `ACTION = "send_email_alert('admin@example.com', 'Unauthorized device detected!')"`

## Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/chaoabordo212/TESTPROJ.git
cd TESTPROJ

# Install dependencies
pip install -r requirements.txt

# Configure your network range in config.json
# Edit the "network_range" field to match your network

# Run TESTPROJ (requires administrator/root privileges)
python main.py
```

### First Time Setup
1. **Configure your network**: Edit `config.json` and set `"network_range"` to match your network (e.g., `"192.168.1.0/24"`)
2. **Set learning duration**: Adjust `"timeout"` in `config.json` (default: 60 seconds for testing, recommended: 300+ seconds for production)
3. **Run with proper privileges**:
   - **Windows**: Run as Administrator
   - **Linux/macOS**: Use `sudo python main.py`

### What to Expect
1. **Learning Phase**: TESTPROJ scans your network and automatically whitelists all discovered devices
2. **Alarm Mode**: After the timeout period, any new unauthorized device triggers the configured action
3. **Alerts**: By default, alerts are logged to `alerts.log` file

📖 **For detailed installation instructions, troubleshooting, and advanced configuration, see [INSTALL.md](INSTALL.md)**

## Usage
1.  Start TESTPROJ. It will begin scanning your local network and populate the whitelist with all currently connected devices.
2.  Allow the system to run for the duration specified by `TIMEOUT`. During this period, ensure all legitimate devices you wish to whitelist are connected to the network.
3.  After `TIMEOUT` expires, TESTPROJ enters alarm mode. Any new device detected that is not in the whitelist will trigger the configured `ACTION`.

## Contributing
(Guidelines for contributing to the project would go here.)

## License
(Information about the project's license would go here.)
