```
Usage: vcd network isolated create [OPTIONS] <name>

Options:
  -g, --gateway <ip>              IP address of the gateway of the new network
                                  [required]
  -n, --netmask <netmask>         network mask for the gateway  [required]
  -d, --description <description>
                                  Description of the network to be created
  --dns1 <ip>                     IP of the primary DNS server
  --dns2 <ip>                     IP of the secondary DNS server
  --dns-suffix <name>             DNS suffix
  --ip-range-start <ip>           Start address of the IP ranges used for
                                  static pool allocation in the network
  --ip-range-end <ip>             End address of the IP ranges used for static
                                  pool allocation in the network
  --dhcp-enabled / --dhcp-disabled
                                  Enable/Disable DHCP service on the new
                                  network
  --default-lease-time <integer>  Default lease in seconds for DHCP addresses
  --max-lease-time <integer>      Max lease in seconds for DHCP addresses
  --dhcp-ip-range-start <ip>      Start address of the IP range used for DHCP
                                  addresses
  --dhcp-ip-range-end <ip>        End address of the IP range used for DHCP
                                  addresses
  --shared / --not-shared         Share/Don't share the network with other
                                  VDC(s) in the organization
  -h, --help                      Show this message and exit.

```
