"""
example2.py
Illustrate the following concepts:
- Send <get> to retrieve config and state data
- Process and leverage XML within Python
- Report back current state of interface
"""

from device_info import csr1
from ncclient import manager
import xmltodict
import xml.dom.minidom

# NETCONF filter to use
netconf_filter = open("filter-ietf-interfaces.xml").read()

with manager.connect(host =csr1 ["address"], 
                        port =csr1 ["port"],
                        username =csr1 ["username"],
                        password =csr1 ["password"],
                        hostkey_verify=False,) as m:


    # Get Configuration and State Info for Interface
    netconf_reply = m.get_config('running')

    print(netconf_reply)
    # Process the XML and store in useful dictionaries
    intf_details = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
    #intf_details = xml.dom.minidom.parseString(netconf_reply)["rpc-reply"]["data"]
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