import os
import sys
import time
import json
import datetime

from pubsub import pub

import meshtastic
import meshtastic.tcp_interface
import meshtastic.serial_interface

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

def onReceive(packet, interface):  # pylint: disable=unused-argument
    """called when a packet arrives"""
    now = datetime.datetime.now()
    iso_now = now.isoformat(timespec='minutes')
    today = now.strftime('%m.%d.%Y')
    sender = iface.nodes[packet["fromId"]]['user']['shortName']
    pax_data = packet["decoded"]["paxcounter"]
    if 'wifi' not in pax_data:
        pax_data['wifi'] = 0
    if 'ble' not in pax_data:
        pax_data['ble'] = 0
    
    print(f"{sender}:\n    Time:{iso_now}\n    BLE:{pax_data['ble']}\n   WIFI:{pax_data['wifi']}\n  TOTAL:{pax_data['ble'] + pax_data['wifi']}")
    file_path = f"./Logs/PAXLOG_{sender}_{today}.csv"
    if not os.path.exists(file_path):
        with open(file_path, 'w+') as file:
            file.write("Time,Bluetooth,Wifi,Total\n")
    with open(file_path, 'a') as file:
        file.write(f"{iso_now},{pax_data['ble']},{pax_data['wifi']},{pax_data['ble'] + pax_data['wifi']}\n")

def onConnection(interface, topic=pub.AUTO_TOPIC):  # pylint: disable=unused-argument
    """called when we (re)connect to the radio"""
    # defaults to broadcast, specify a destination ID if you wish
    # interface.sendText("PAX Logger Online")

pub.subscribe(onReceive, "meshtastic.receive.paxcounter")
pub.subscribe(onConnection, "meshtastic.connection.established")
try:
    print("Trying to connect to device via serial")
    iface = meshtastic.serial_interface.SerialInterface()
    print("Connected to: " + iface.getShortName())
    while True:
                time.sleep(1000)
    # iface.close()
except Exception as ex:
    print(f"Error: Could not connect to node via serial")

    target_ip = "192.168.4.132"#"192.168.4.1/24"
    local_devices = scan(target_ip)
    display_result(local_devices)

    for client in local_devices:
        print("Trying to connect to device at: " + client["ip"])
        try:
            iface = meshtastic.tcp_interface.TCPInterface(hostname=client["ip"])#'192.168.4.132')
            print("Connected to: " + client["ip"])
            while True:
                time.sleep(1000)
            break
        except Exception as ex:
            print("No meshtastic connection at: " + client["ip"])
