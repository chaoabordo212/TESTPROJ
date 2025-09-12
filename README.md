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

## Usage
1.  Start TESTPROJ. It will begin scanning your local network and populate the whitelist with all currently connected devices.
2.  Allow the system to run for the duration specified by `TIMEOUT`. During this period, ensure all legitimate devices you wish to whitelist are connected to the network.
3.  After `TIMEOUT` expires, TESTPROJ enters alarm mode. Any new device detected that is not in the whitelist will trigger the configured `ACTION`.

## Installation
(Instructions for installation would go here, e.g., `git clone ...`, `pip install -r requirements.txt`, etc.)

## Contributing
(Guidelines for contributing to the project would go here.)

## License
(Information about the project's license would go here.)