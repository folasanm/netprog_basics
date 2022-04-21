"""
example2.py
Illustrate the following concepts:
- Send <get> to retrieve config and state data
- Process and leverage XML within Python
- Report back current state of interface
"""

from device_info import  csr1
from ncclient import manager
import xmltodict
import xml.dom.minidom
from pprint import pp, pprint

# NETCONF filter to use
netconf_filter = open("filter-ietf-interfaces.xml").read()


if __name__ == '__main__':
    with manager.connect(host = csr1 ["address"], 
                            port = csr1 ["port"],
                            username = csr1 ["username"],
                            password = csr1 ["password"],
                            hostkey_verify=False,) as m:


        # Get Configuration and State Info for Interface
        netconf_reply = m.get(netconf_filter)
        #print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

        intf_details = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]  
        intf_config = intf_details["interfaces"]["interface"]
        intf_info = intf_details["interfaces-state"]["interface"]


        for intf in intf_config:
            print("")
            print("Interface Details:")
            print("  Name: {}".format(intf["name"]))
            print("  Link Enabled: {}".format(intf["enabled"]))
            try:
                print("  IP Address: {} {}".format(intf["ipv4"]["address"]['ip'], intf['ipv4']['address']['netmask']))
            except:
                print("  NO IP Address")
            for state in intf_info:
                if state['name'] == intf['name']:
                    #print("  Description: {}".format(intf_config["description"]))
                    print("  MAC Address: {}".format(state["phys-address"]))
                    print("  Packets Input: {}".format(state["statistics"]["in-unicast-pkts"]))
                    print("  Packets Output: {}".format(state["statistics"]["out-unicast-pkts"]))

       