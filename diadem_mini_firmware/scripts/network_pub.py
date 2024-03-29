#!/usr/bin/python3

import rospy
from std_msgs.msg import String
import subprocess
import json
import os
import sys 


def connection_type() -> str:
    # Retuns a string containing which type is on
    try:
        active_connection = subprocess.check_output(["sudo","nmcli","connection","show","--active"],universal_newlines=True, text=True)
    except Exception as e:
        print("Something went wrong",e)
        sys.exit(1)
    if "wifi" in active_connection:
        if len(active_connection.splitlines()) == 3:
            if "Hotspot" in active_connection:
                return "dual"
            else:
                return "dualw"
        else:
            if "Hotspot" in active_connection:
                return "hotspot"
            elif "wifi" in active_connection:
                return "wifi"
            else:
                return "nocon"
    else:
        return "nocon"

def get_adapter_names():
    logical_output = subprocess.check_output(["sudo","lshw","-C","network"],stderr=subprocess.DEVNULL, universal_newlines=True)
    logical_names = re.findall(r'logical name: (\w+)', logical_output)
    return logical_names

def get_bus_names():
    bus_output = subprocess.check_output(["sudo","lshw","-C","network"], stderr=subprocess.DEVNULL,universal_newlines=True)
    bus_names = re.findall(r'bus info: (\S+)', bus_output)
    return bus_names


def hotspot_dev() -> str:
    devices = give_dict(get_adapter_names(), get_bus_names())

    for item in devices:
        if item.startswith('w') and "pci" in devices[item]:
            return item
        else:
            pass
    print("Hotspot Adapter Not Found")
    return None

def wifi_dev() -> str:
    devices = give_dict(get_adapter_names(), get_bus_names())

    for item in devices:
        if item.startswith('w') and "usb" in devices[item]:
            return item
        else:
            pass
    print("WiFi Adapter Not Found")
    return None

def grep_ssid():
    try:
        output = subprocess.check_output(["iwgetid"], text=True).strip()
        essid = output.split('ESSID:"', 1)[-1].split('"', 1)[0]
        if essid == "":
            return "CONNECTION LOST"
        return essid
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def center_ip_address(ip_address, total_width=15):
    padding = (total_width - len(ip_address)) // 2
    formatted_string = f"{padding * ' '}{ip_address}{padding * ' '}"
    return formatted_string
counter = 0
some_ip_address = "  Fetching IP  "


def get_ip_address():
    global counter,some_ip_address
    json_data = rospy.Publisher('/network_status', String, queue_size=10)
    rospy.init_node('network_status', anonymous=True)
    rate = rospy.Rate(1)
    connection = connection_type()
    if connection != "nocon":
        some_ip_address = subprocess.check_output(["robonet-getip"], stderr=subprocess.DEVNULL,universal_newlines=True,text=True)
        if "None" in some_ip_address:
            some_ip_address = "  Fetching IP  "
        else:
            pass
    while not rospy.is_shutdown():
        connection = connection_type()

        if counter > 10:
            some_ip_address = subprocess.check_output(["robonet-getip"], stderr=subprocess.DEVNULL,universal_newlines=True,text=True)
            counter = 0
        try:
            if connection == "wifi":
                network_status = 1
                status = connection
                temp_ssid = grep_ssid()
                if temp_ssid != None:
                    info =  f"{center_ip_address(grep_ssid())}"
                else:
                    info = center_ip_address("Lost Connection")
                ip = some_ip_address
            elif connection == "hotspot":
                network_status = 2
                status = connection
                info = f"{center_ip_address(subprocess.getoutput('echo $USER'))}"
                ip = some_ip_address
            elif connection == "dual":
                network_status = 3
                status = "wifi"
                info = f"{center_ip_address(grep_ssid())}"
                ip = some_ip_address
            elif connection == "dualw":
                network_status = 4
                status = "wifi"
                info = f"{center_ip_address(grep_ssid())}"
                ip = some_ip_address
            elif connection == "nocon":
                network_status = 0
                status = "nocon"
                info = center_ip_address(" No Connection ")
                ip = center_ip_address("    Trying    ")
            else:
                network_status = 69
                status = "IDK"
                info = "COURRPPTED"
                ip = center_ip_address("   CALL RBL   ")
        except subprocess.CalledProcessError:
            network_status = 4 
        ip = ip.replace('\n','')
        json_obj = {
                "mode" : network_status,
                "status": f"{status}",
                "info" : f"{info}",
                "ip"   : f"{ip}"
        }
        json_str = json.dumps(json_obj)
        msg = String()
        msg.data = json_str
        print(msg.data)
        print(counter)
        json_data.publish(msg)
        rate.sleep()
        counter += 1

if __name__ == '__main__':
    try:
        get_ip_address()
    except rospy.ROSInterruptException:
        pass
