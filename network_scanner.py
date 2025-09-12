import scapy.all as scapy
import logging

def scan_network(ip_range):
    """
    Scans the network using ARP requests and returns a list of MAC addresses.
    """
    try:
        arp_request = scapy.ARP(pdst=ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        
        answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
        
        devices = [element[1].hwsrc for element in answered_list]
        return devices
    except Exception as e:
        logging.error(f"An error occurred during network scan: {e}")
        logging.error("This might be due to insufficient privileges. Try running as root or with sudo.")
        return []
