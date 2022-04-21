"""
example3.py
Illustrate the following concepts:
- Constructing XML Config Payload for NETCONF
- Sending <edit-config> operation with ncclient
- Verify result
"""

from device_info import csr1
from ncclient import manager

# NETCONF Config Template to use
netconf_template = open("config-temp-ietf-interfaces.xml").read()

if __name__ == '__main__':
    # Build the XML Configuration to Send
    netconf_payload = netconf_template.format(int_name="GigabitEthernet3",
                                              int_desc="Configured by NETCONF",
                                              ip_address="10.255.255.1",
                                              subnet_mask="255.255.255.0"
                                              )
    print("Configuration Payload:")
    print("----------------------")
    print(netconf_payload)

    with manager.connect(host=csr1["address"], port=csr1["port"],
                         username=csr1["username"],
                         password=csr1["password"],
                         hostkey_verify=False) as m:

        # Send NETCONF <edit-config>
        netconf_reply = m.edit_config(netconf_payload, target="running")

        # Print the NETCONF Reply
        print(netconf_reply)
