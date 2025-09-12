# TESTPROJ Implementation Architecture

## Overview
TESTPROJ is a network monitoring tool for local networks, focused on automatic whitelisting and alerting for unauthorized devices. The architecture is designed for simplicity, extensibility, and ease of deployment in SOHO and home environments.

## Major Components

### 1. Network Scanner
- **Purpose:** Discover devices on the local network segment.
- **Implementation:** Uses ARP scanning via the `scapy` library for efficiency and reliability.
- **Extensibility:** Can be extended to support passive sniffing, nmap, or other protocols.

### 2. Whitelist Manager
- **Purpose:** Store and manage trusted device identifiers (primarily MAC addresses).
- **Implementation:**
  - Initial version: JSON file for simplicity.
  - Advanced: SQLite database for richer metadata (device name, last seen, IP history).
- **Features:** Add/remove devices, track device info, support for "forget device" functionality.

### 3. Configuration Loader
- **Purpose:** Load runtime parameters (`TIMEOUT`, `ACTION`, network range, etc.).
- **Implementation:**
  - Initial: Hardcoded or environment variables.
  - Advanced: Config file support (`config.ini`, `.env`, YAML).

### 4. Alarm Engine
- **Purpose:** Monitor for unauthorized devices and trigger actions.
- **Implementation:**
  - Periodic scan loop (using `time.sleep()` for scheduling).
  - On detection, triggers the configured `ACTION` (shell command, email, API call).
- **Extensibility:** Pluggable notification backends (email, push, SMS, Telegram, etc.).

### 5. Logging & Audit
- **Purpose:** Record events, detections, and errors for audit and debugging.
- **Implementation:** Python `logging` module, optionally logging to file or database.

### 6. Optional Web UI
- **Purpose:** User-friendly management of whitelist, configuration, and logs.
- **Implementation:** Flask or FastAPI for REST API and simple dashboard.

## Data Flow
1. **Startup:**
   - Load configuration and whitelist.
   - Begin learning phase (scan and populate whitelist).
2. **Learning Phase:**
   - Scan network periodically.
   - Add new devices to whitelist.
   - After `TIMEOUT`, switch to alarm mode.
3. **Alarm Mode:**
   - Scan network periodically.
   - If unknown device detected, log event and trigger `ACTION`.
   - Optionally notify via email, push, or other integrations.

## Key Files & Directories
- `network_scanner.py`: ARP scanning logic (Scapy).
- `whitelist_manager.py`: Whitelist CRUD and persistence.
- `config.py`: Configuration loader.
- `alarm_engine.py`: Main monitoring loop and action triggers.
- `logging_setup.py`: Logging configuration.
- `web_ui/`: Optional Flask/FastAPI app for management.
- `ARCHITECTURE.md`: This document.
- `README.md`: Project overview and usage.
- `PROPOSAL.md`: Extended concept and implementation notes.

## External Dependencies
- `scapy`: ARP scanning and packet manipulation.
- `sqlite3` or `json`: Whitelist storage.
- `smtplib`, `requests`, `subprocess`: Notification and action execution.
- `Flask`/`FastAPI`: Optional web interface.

## Integration Points
- **Notification Services:** Email (SMTP), Pushbullet, Pushover, Telegram, Twilio (SMS).
- **Home Automation:** Potential integration with Home Assistant via REST API or MQTT.
- **Containerization:** Dockerfile for easy deployment.

## Project-Specific Patterns
- **Automatic Whitelisting:** All devices present during learning phase are trusted.
- **Configurable Actions:** Any shell command or Python function can be triggered on unauthorized detection.
- **Extensible Storage:** Start simple (JSON), migrate to robust (SQLite) as needed.
- **Modular Design:** Each major function is a separate module for maintainability.

## Example Workflow
```python
# ...existing code...
if __name__ == "__main__":
    config = load_config()
    whitelist = load_whitelist()
    scanner = NetworkScanner(config.network_range)
    alarm = AlarmEngine(scanner, whitelist, config)
    alarm.run()
# ...existing code...
```

## Future Enhancements
- Web dashboard for device management and logs.
- Vendor lookup for MAC addresses (OUI).
- Persistent device history and advanced alerting.
- Unit and integration tests for reliability.
- Docker and systemd support for deployment.

---
This architecture is designed to be immediately actionable for AI coding agents and developers. For conventions, see `README.md` and `PROPOSAL.md`. For questions or improvements, update this file and notify maintainers.