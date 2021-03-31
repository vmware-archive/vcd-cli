```
Usage: vcd vapp network services firewall update [OPTIONS] <vapp-name>
                                                 <network-name> <firewall-
                                                 rule-name>

Options:
  --name <new_name>               new name of firewall rule
  --enable / --disable            enable firewall rule
  --policy <policy>               policy on firewall rule
  --protocols <protocols>         all protocol names in comma separated format
  --source-port-range <source_port_range>
                                  source port range on firewall rule
  --source-ip <source_ip>         source ip on firewall rule
  --destination-port-range <destination_port_range>
                                  destination port range on firewall rule
  --destination-ip <destination_ip>
                                  destination ip on firewall rule
  --enable-logging / --disable-logging
                                  enable logging on firewall rule
  -h, --help                      Show this message and exit.

```
