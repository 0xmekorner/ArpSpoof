class Host:
    def __init__(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac

class NetworkSimulator:
    def __init__(self):
        self.hosts = {
            "client": Host("Client", "192.168.1.10", "AA:AA:AA:AA:AA:10"),
            "gateway": Host("Gateway", "192.168.1.1", "GG:GG:GG:GG:GG:01"),
            "attacker": Host("Attacker", "192.168.1.50", "CC:CC:CC:CC:CC:50"),
        }
        self.arp_table = {
            "192.168.1.1": self.hosts["gateway"].mac,
            "192.168.1.50": self.hosts["attacker"].mac,
        }

    def show_table(self):
        print("\nARP table:")
        for ip, mac in self.arp_table.items():
            print(f"  {ip} -> {mac}")

    def simulate_poisoning(self):
        attacker_mac = self.hosts["attacker"].mac
        gateway_ip = self.hosts["gateway"].ip
        print("\n[SIMULATION] Forged ARP reply is delivered virtually.")
        print(f"Mapping changes: {gateway_ip} -> {attacker_mac}")
        self.arp_table[gateway_ip] = attacker_mac

    def reset(self):
        gateway = self.hosts["gateway"]
        self.arp_table[gateway.ip] = gateway.mac
        print("\nARP table restored.")

def main():
    network = NetworkSimulator()

    while True:
        print("\n1. Show ARP table")
        print("2. Simulate ARP poisoning")
        print("3. Reset ARP table")
        print("4. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            network.show_table()
        elif choice == "2":
            network.simulate_poisoning()
        elif choice == "3":
            network.reset()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
