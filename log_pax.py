"""Simple program to demo how to use meshtastic library.
   To run: python examples/pub_sub_example2.py
"""

import os
import sys
import time
import json
import datetime

from pubsub import pub

import meshtastic
import meshtastic.tcp_interface
import meshtastic.serial_interface

host = "!ae61b02c";

# simple arg check
if len(sys.argv) >= 2:
    host = sys.argv[1];

def onReceive(packet, interface):  # pylint: disable=unused-argument
    """called when a packet arrives"""
    now = datetime.datetime.now()
    today = now.strftime('%m.%d.%Y')
    sender = packet["fromId"] #lets make this easier to read
    print(f"-------------------------------------------------------------------------------")
    print(f"Received: {packet}")
    print(f"-------------------------------------------------------------------------------")
    pax_data = packet["decoded"]["paxcounter"]
    if 'wifi' not in pax_data:
        pax_data['wifi'] = 0
    
    file_path = f"PAXLOG_{sender}_{today}.csv".replace('!','')
    if not os.path.exists(file_path):
        with open(file_path, 'w+') as file:
            file.write("Time,Bluetooth,Wifi,Total\n")
    with open(file_path, 'a') as file:
        file.write(f"{now},{pax_data['ble']},{pax_data['wifi']},{pax_data['ble'] + pax_data['wifi']}\n")

def onConnection(interface, topic=pub.AUTO_TOPIC):  # pylint: disable=unused-argument
    """called when we (re)connect to the radio"""
    # defaults to broadcast, specify a destination ID if you wish
    # interface.sendText("PAX Logger Online")


pub.subscribe(onReceive, "meshtastic.receive.paxcounter")
pub.subscribe(onConnection, "meshtastic.connection.established")
try:
    iface = meshtastic.serial_interface.SerialInterface()#meshtastic.tcp_interface.TCPInterface(hostname=host)
    while True:
        time.sleep(1000)
    iface.close()
except Exception as ex:
    print(f"Error: Could not connect to {sys.argv[1]} {ex}")
    sys.exit(1)
