"""
example2.py
Illustrate the following concepts:
- Send <get> to retrieve config and state data
- Process and leverage XML within Python
- Report back current state of interface
"""

from device_info import ios_xe1
from ncclient import manager
import xmltodict
import xml.dom.minidom

# NETCONF filter to use
netconf_filter = open("filter-ietf-interfaces.xml").read()

if __name__ == '__main__':
    with manager.connect(
                        host=ios_xe1["address"], 
                        port=ios_xe1["port"],
                        username=ios_xe1["username"],
                        password=ios_xe1["password"],
                        hostkey_verify=False
                         ) as m:

        # Get Configuration and State Info for Interface
        netconf_reply = m.get(netconf_filter)

        print (netconf_reply)
        #netconf_reply = m.get_config(source = 'running', filter = netconf_filter)

        # Process the XML and store in useful dictionaries
        intf_details = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
        intf_config = intf_details["interfaces"]["interface"]
        intf_info = intf_details["interfaces-state"]["interface"]

        print("")
        print("Interface Details:")
        print("  Name: {}".format(intf_config["name"]["#text"]))
        print("  Description: {}".format(intf_config["description"]))
        print("  Type: {}".format(intf_config["type"]["#text"]))
        print("  MAC Address: {}".format(intf_info["phys-address"]))
        print("  Packets Input: {}".format(intf_info["statistics"]["in-unicast-pkts"]))
        print("  Packets Output: {}".format(intf_info["statistics"]["out-unicast-pkts"]))
