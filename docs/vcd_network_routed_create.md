```
Usage: vcd network routed create [OPTIONS] <name>

Options:
  -g, --gateway-name <name>       name of gateway to which this network will
                                  connect  [required]
  --subnet <CIDR format. e.g.,x.x.x.x/20>
                                  Network CIDR  [required]
  --description <description>     description
  --dns1 <IP>                     primary DNS IP
  --dns2 <IP>                     secondary DNS IP
  --dns-suffix <Name>             dns suffix
  --ip-range <ip_range_start-ip_range_end>
                                  IP range
  --shared-enabled / --shared-disabled
                                  shared enabled
  --guest-vlan-allowed-enabled / --guest-vlan-allowed-disabled
                                  guest vlan allowed
  --sub-interface-enabled / --sub-interface-disabled
                                  create as sub interface
  --distributed-interface-enabled / --distributed-interface-disabled
                                  create as distributed interface
  --retain-net-info-across-deployments-enabled / --retain-net-info-across-deployments-disabled
                                  retain net info across deployment
  -h, --help                      Show this message and exit.

```
