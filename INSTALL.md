# TESTPROJ Installation & Setup Guide

This guide provides comprehensive instructions for installing and setting up TESTPROJ on your system.

## Table of Contents
- [System Requirements](#system-requirements)
- [Quick Installation](#quick-installation)
- [Platform-Specific Setup](#platform-specific-setup)
- [Initial Configuration](#initial-configuration)
- [First Run Guide](#first-run-guide)
- [Troubleshooting](#troubleshooting)
- [Advanced Configuration](#advanced-configuration)
- [Security Considerations](#security-considerations)

## System Requirements

### Minimum Requirements
- **Python**: 3.6 or higher
- **Memory**: 256MB RAM
- **Storage**: 50MB free space
- **Network**: Local network access with broadcast capability

### Platform Compatibility
- ✅ **Windows 10/11**
- ✅ **Linux** (Ubuntu, Debian, CentOS, Fedora)
- ✅ **macOS** (10.14+)

### Required Privileges
- **Windows**: Administrator privileges (for raw socket access)
- **Linux**: Root privileges or CAP_NET_RAW capability
- **macOS**: Root privileges or network access permissions

## Quick Installation

### 1. Clone the Repository
```bash
git clone https://github.com/chaoabordo212/TESTPROJ.git
cd TESTPROJ
```

### 2. Set Up Python Environment (Recommended)
```bash
# Create virtual environment
python -m venv testproj-env

# Activate virtual environment
# On Windows:
testproj-env\Scripts\activate
# On Linux/macOS:
source testproj-env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Network Settings
```bash
# Edit config.json to match your network
# Example: Change "192.168.1.0/24" to your network range
```

### 5. Run TESTPROJ
```bash
python main.py
```

## Platform-Specific Setup

### Windows Setup

#### Prerequisites
1. **Install Python 3.6+** from [python.org](https://www.python.org/downloads/)
2. **Install Npcap** (required for Scapy):
   - Download from [npcap.org](https://npcap.org/#download)
   - Install with WinPcap API compatibility enabled
   - Restart your computer after installation

#### Running with Administrator Privileges
```powershell
# Option 1: Run PowerShell as Administrator, then:
python main.py

# Option 2: Run from elevated Command Prompt
# Right-click Command Prompt → "Run as administrator"
cd path\to\TESTPROJ
python main.py
```

#### Windows-Specific Issues
- **"Access Denied" errors**: Always run as Administrator
- **"WinPcap not found"**: Install Npcap with WinPcap compatibility
- **Firewall warnings**: Allow Python through Windows Firewall

### Linux Setup

#### Prerequisites
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS/Fedora
sudo yum install python3 python3-pip
# or
sudo dnf install python3 python3-pip
```

#### Running with Proper Privileges
```bash
# Option 1: Run with sudo (simplest)
sudo python main.py

# Option 2: Set capabilities (recommended for production)
sudo setcap cap_net_raw+ep $(which python3)
python main.py

# Option 3: Add user to specific groups (distribution-dependent)
sudo usermod -a -G wireshark $USER
# Logout and login again, then:
python main.py
```

### macOS Setup

#### Prerequisites
```bash
# Install Python 3 (if not already installed)
brew install python3

# Alternative: Download from python.org
```

#### Running with Privileges
```bash
# Run with sudo
sudo python main.py

# For permanent setup, you may need to adjust security settings
# System Preferences → Security & Privacy → Privacy → Full Disk Access
```

## Initial Configuration

### 1. Network Range Detection

First, identify your network range:

#### Windows
```cmd
ipconfig
# Look for your network adapter and note the IP and subnet mask
# Example: IP 192.168.1.100, Subnet 255.255.255.0 = 192.168.1.0/24
```

#### Linux/macOS
```bash
ip route show
# or
ifconfig
# Look for your main network interface
```

### 2. Configuration File Setup

Edit `config.json` to match your environment:

```json
{
  "timeout": 300,                    // Learning phase duration (5 minutes)
  "action": "echo 'Alert: Unauthorized device {mac}' >> alerts.log",
  "network_range": "192.168.1.0/24", // YOUR network range
  "scan_interval_learning": 30,      // Scan every 30 seconds during learning
  "scan_interval_alarm": 60          // Scan every 60 seconds in alarm mode
}
```

### 3. Timeout Configuration Guidelines

Choose timeout based on your use case:
- **Testing**: 60-300 seconds (1-5 minutes)
- **Home network**: 1800-3600 seconds (30-60 minutes)
- **Office environment**: 3600-7200 seconds (1-2 hours)

## First Run Guide

### Step 1: Initial Launch
```bash
python main.py
```

**Expected output:**
```
2024-01-01 12:00:00,000 - INFO - Starting TESTPROJ application...
2024-01-01 12:00:00,001 - INFO - AlarmEngine initialized.
2024-01-01 12:00:00,002 - INFO - TESTPROJ started.
2024-01-01 12:00:00,003 - INFO - Entering learning phase...
```

### Step 2: Learning Phase (First 5 Minutes)
During this phase, TESTPROJ will:
- Scan your network every 30 seconds
- Automatically add all discovered devices to the whitelist
- Log each new device found

**Expected behavior:**
```
2024-01-01 12:00:05,100 - INFO - Scanning network during learning phase...
2024-01-01 12:00:06,200 - INFO - Added aa:bb:cc:dd:ee:ff to whitelist.
2024-01-01 12:00:06,201 - INFO - Added 11:22:33:44:55:66 to whitelist.
```

### Step 3: Alarm Mode
After the timeout period:
```
2024-01-01 12:05:00,000 - INFO - Learning phase finished. Whitelist contains 5 devices.
2024-01-01 12:05:00,001 - INFO - Saving final whitelist from learning phase.
2024-01-01 12:05:00,002 - INFO - Entering alarm mode...
```

### Step 4: Testing
To test the alarm functionality:
1. Connect a new device to your network (phone, laptop, etc.)
2. Wait for the next scan cycle
3. Check for alert messages in the console and `alerts.log` file

## Troubleshooting

### Common Issues

#### "Permission denied" or "Access denied"
**Problem**: Insufficient privileges for raw socket access
**Solution**:
- **Windows**: Run as Administrator
- **Linux**: Use `sudo` or set capabilities
- **macOS**: Use `sudo` or adjust security settings

#### "No devices found during scan"
**Problem**: Network range misconfigured or network connectivity issues
**Solutions**:
1. Verify network range in `config.json`
2. Check network connectivity: `ping 8.8.8.8`
3. Ensure you're on the correct network interface
4. Try a smaller network range first (e.g., `192.168.1.1/32`)

#### "WinPcap/Npcap not found" (Windows)
**Problem**: Missing packet capture library
**Solution**:
1. Download and install Npcap from [npcap.org](https://npcap.org/)
2. Enable "WinPcap API compatibility" during installation
3. Restart computer
4. Reinstall Python dependencies: `pip install --force-reinstall scapy`

#### "ImportError: No module named scapy"
**Problem**: Dependencies not installed
**Solution**:
```bash
pip install -r requirements.txt
# or
pip install scapy
```

#### Application exits with "Failed to load configuration"
**Problem**: Missing or corrupted `config.json`
**Solution**:
1. Check if `config.json` exists in the project directory
2. Validate JSON syntax using an online JSON validator
3. Delete `config.json` to regenerate default configuration

### Network-Specific Issues

#### Virtual Machines
- Ensure VM network is in "Bridged" mode, not "NAT"
- VM may need promiscuous mode enabled
- Some hypervisors block ARP scanning

#### Docker/Containers
- Use `--net=host` mode for network scanning
- May require `--privileged` flag
- Consider running on host system instead

#### Corporate Networks
- Some corporate firewalls block ARP traffic
- May need network administrator approval
- Consider using passive monitoring mode (future feature)

### Debug Mode

Enable verbose logging for troubleshooting:

```python
# Add to main.py temporarily
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Advanced Configuration

### Custom Actions

#### Email Alerts
```json
{
  "action": "python -c \"import smtplib; server=smtplib.SMTP('smtp.gmail.com',587); server.starttls(); server.login('user@gmail.com','password'); server.sendmail('user@gmail.com','admin@company.com','Unauthorized device: {mac}'); server.quit()\""
}
```

#### Webhook Notifications
```json
{
  "action": "curl -X POST https://hooks.slack.com/your-webhook-url -d '{\"text\":\"Unauthorized device detected: {mac}\"}'"
}
```

#### Custom Script Execution
```json
{
  "action": "python alert_script.py {mac}"
}
```

### Multiple Action Commands
```json
{
  "action": "echo 'Alert: {mac}' >> alerts.log && curl -X POST https://api.example.com/alert -d 'mac={mac}'"
}
```

### Production Deployment

#### Running as a Service (Linux)
Create `/etc/systemd/system/testproj.service`:
```ini
[Unit]
Description=TESTPROJ Network Monitor
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/path/to/TESTPROJ
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable testproj.service
sudo systemctl start testproj.service
```

#### Running as a Service (Windows)
Use NSSM (Non-Sucking Service Manager):
```cmd
nssm install TESTPROJ "C:\Python39\python.exe" "C:\path\to\TESTPROJ\main.py"
nssm start TESTPROJ
```

### Performance Tuning

For large networks:
```json
{
  "timeout": 7200,                    // 2 hours learning phase
  "scan_interval_learning": 60,      // Less frequent scanning
  "scan_interval_alarm": 120,        // Even less frequent in alarm mode
  "network_range": "192.168.1.0/25" // Smaller network range if possible
}
```

## Security Considerations

### Principle of Least Privilege
- Create dedicated service account for TESTPROJ
- Use capability-based permissions on Linux instead of full root
- Limit file system access

### Network Security
- Monitor TESTPROJ logs for suspicious activity
- Regularly review whitelist contents
- Consider network segmentation for critical devices

### Action Security
- Validate action commands for injection vulnerabilities
- Use absolute paths in action scripts
- Avoid shell metacharacters in action strings

### Data Protection
- Secure `config.json` and `whitelist.json` files
- Consider encrypting configuration files
- Implement log rotation to prevent disk space issues

---

## Need Help?

- **Issues**: Report bugs at [GitHub Issues](https://github.com/chaoabordo212/TESTPROJ/issues)
- **Documentation**: Check `README.md` and `ARCHITECTURE.md`
- **Community**: Join discussions in GitHub Discussions
- **Security**: Report security issues privately via email

## Version Notes

This installation guide is for TESTPROJ v1.0+. For older versions, please check the appropriate branch or tag documentation.
