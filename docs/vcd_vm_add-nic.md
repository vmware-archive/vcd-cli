```
Usage: vcd vm add-nic [OPTIONS] <vapp-name> <vm-name>

Options:
  --adapter-type <adapter-type>   adapter type of nic - one of
                                  VLANCE|VMXNET|VMXNET2|VMXNET3|E1000
  --primary                       whether nic has to be a primary
  --connect                       whether nic has to be connected
  --network <network>             network to connect to
  --ip-address-mode <ip-address-mode>
                                  IP address allocation mode - one of
                                  DHCP|POOL|MANUAL|NONE
  --ip-address <ip-address>       nanual IP address that needs to be allocated
                                  to the nic
  -h, --help                      Show this message and exit.

```
