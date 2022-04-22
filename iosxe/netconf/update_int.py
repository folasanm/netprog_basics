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
netconf_template = open("config-temp-ietf-interface.xml").read()

if __name__ == '__main__':

    # Build the XML Configuration to Send
    '''
    netconf_payload = netconf_template.format(intf_name="GigabitEthernet3",
                                              intf_desc="Configured by NETCONF",
                                              ip_address="10.255.255.1",
                                              subnet_mask="255.255.255.0"
                                             )
    '''
    intf_name = input('Interface name: ')
    intf_desc = input('Description to use: ')
    ip_address = input('IP address: ')
    subnet_mask = input('Network Mask: ')
    intf_status = input('Enabled(True/False): ')


    netconf_payload = netconf_template.format(int_name=intf_name, 
                                                int_desc=intf_desc,
                                                ip_address=ip_address,
                                                subnet_mask=subnet_mask,
                                                status=intf_status.lower())
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