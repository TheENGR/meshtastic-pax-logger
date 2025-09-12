# scapy==2.6.1

import scapy.all as scapy

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=10, verbose=False)[0]
    
    clients_list = []
    for element in answered_list:
        clients_list.append({"ip": element[1].psrc, "mac": element[1].hwsrc})
    return clients_list


def display_result(results):
    print("IP Address\t\tMAC Address\n")
    for client in results:
        print(client["ip"] + "\t\t" + client["mac"])


    #print("Trying to connect to device at: " + client["ip"])

    ##target_ip = "192.168.4.132"
    #target_ip = "192.168.4.100/24"
    #local_devices = scan(target_ip)
    #display_result(local_devices)

    #for client in local_devices:
    #    print("Trying to connect to device at: " + client["ip"])
    #    try:
    #        iface = meshtastic.tcp_interface.TCPInterface(hostname='meshtastic.local')
    #        #iface = meshtastic.tcp_interface.TCPInterface(hostname='192.168.4.132')
    #        #iface = meshtastic.tcp_interface.TCPInterface(hostname=client["ip"])
    #        print("Connected to: " + client["ip"] + "\n\n")
    #        while True:
    #            time.sleep(1000)
    #        break
    #    except Exception as ex:
    #        print("No meshtastic connection at: " + client["ip"])
