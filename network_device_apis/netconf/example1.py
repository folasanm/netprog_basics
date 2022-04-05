"""
example1.py
Illustrate the following concepts:
- Opening a NETCONF connection with ncclient
- Saying <hello> and review capabilities
"""

from device_info import csr1 
from ncclient import manager

if __name__ == '__main__':
    with manager.connect(host = csr1 ["address"], 
                         port = csr1 ["port"],
                         username = csr1 ["username"],
                         password = csr1 ["password"],
                         hostkey_verify=False) as m:

        print("Here are the NETCONF Capabilities")
        for capability in m.server_capabilities:
            print(capability)
