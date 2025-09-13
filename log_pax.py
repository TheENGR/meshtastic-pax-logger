import os
import sys
import time
import json
import datetime

from pubsub import pub

import meshtastic
import meshtastic.tcp_interface
import meshtastic.serial_interface

script_directory = os.path.dirname(os.path.abspath(__file__))
log_directory = os.path.join(script_directory, "Logs")

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
    file_path = os.path.join(log_directory, f"PAXLOG_{sender}_{today}.csv")
    if not os.path.exists(file_path):
        with open(file_path, 'w+') as file:
            file.write("Time,Bluetooth,Wifi,Total\n")
    with open(file_path, 'a') as file:
        file.write(f"{iso_now},{pax_data['ble']},{pax_data['wifi']},{pax_data['ble'] + pax_data['wifi']}\n")

def onConnection(interface, topic=pub.AUTO_TOPIC):  # pylint: disable=unused-argument
    """called when we (re)connect to the radio"""
    # defaults to broadcast, specify a destination ID if you wish
    interface.sendText("PAX Logger Online")

pub.subscribe(onReceive, "meshtastic.receive.paxcounter")
pub.subscribe(onConnection, "meshtastic.connection.established")

try:
    print("Trying to connect to device via serial")
    iface = meshtastic.serial_interface.SerialInterface()
    print("Connected to: " + iface.getShortName())
    
    while True:
        time.sleep(1000)
except Exception as ex:
    print(f"Error: Could not connect to node via serial")
    print("Trying to connect to device at: meshtastic.local via internet")
    try:
        iface = meshtastic.tcp_interface.TCPInterface(hostname='meshtastic.local')
        print("Connected to: " + iface.getShortName())
        while True:
            time.sleep(1000)
    except Exception as ex:
        print("No meshtastic connection at: meshtastic.local via internet")
