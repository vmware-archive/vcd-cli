```
Usage: vcd gateway services dhcp-pool create [OPTIONS] <gateway name>

Options:
  -r, --range <IP range of the pool>
                                  IP range of the DHCP pool  [required]
  --enable-auto-dns / --disable-auto-dns
                                  Auto configure DNS
  -g--gateway-ip <default-gateway-ip>
                                  Default gateway ip
  -d--domain <domain-name>        domain name
  -p--primary-server <primary-name-server>
                                  primary server ip
  -s--secondary-server <secondary-name-server>
                                  secondary server ip
  -l--lease <lease-time>          lease time
  --never-expire-lease / --expire-lease
                                  lease lease expire
  --subnet <subnet>               subnet mask
  -h, --help                      Show this message and exit.

```
