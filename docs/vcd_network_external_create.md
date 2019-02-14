```
Usage: vcd network external create [OPTIONS] <name>

Options:
  -v, --vc <vc-name>              name of the vCenter  [required]
  -p, --port-group <name>         portgroup to create external network
                                  [required]
  -g, --gateway <ip>              gateway of the subnet  [required]
  -n, --netmask <netmask>         network mask of the subnet  [required]
  -i, --ip-range <ip>             IP range in StartAddress-EndAddress format
                                  [required]
  -d, --description <description>
                                  Description of the external network to be
                                  created
  --dns1 <ip>                     IP of the primary DNS server of the subnet
  --dns2 <ip>                     IP of the secondary DNS server of the subnet
  --dns-suffix <name>             DNS suffix
  -h, --help                      Show this message and exit.

```
