```
Usage: vcd gateway services ipsec_vpn create [OPTIONS] <gateway name>

Options:
  --name <IPsec VPN name>         IPsec VPN name  [required]
  -lid, --local-id <local-id>     Local id of IPsec VPN.  [required]
  -pid, --peer-id <peer-id>       Peer id of IPsec VPN.  [required]
  -lip, --local-ip <local-ip>     Local ip of IPsec VPN.  [required]
  -pip, --peer-ip <peer-ip>       Peer ip of IPsec VPN.  [required]
  -lsubnet, --local-subnet <local-subnet>
                                  Local subnets of IPsec VPN.These should be
                                  given comma separated.  [required]
  -psubnet, --peer-subnet <peer-subnet>
                                  Peer subnets of IPsec VPN.These should be
                                  given comma separated.  [required]
  -psk, --pre-shared-key <pre-shared-key>
                                  Pre shared key of IPsec VPN.  [required]
  --description <description>     Description of IPsec VPN.
  --encryption-protocol <encryption protocol>
                                  encryption protocol of IPsec VPN.
  --authentication-mode <authentication_mode>
                                  authentication_mode of IPsec VPN.
  --dh-group <dh group>           dh group for IPsec VPN.
  --mtu <mtu>                     mtu for IPsec VPN.
  --enable / --disable            enable/disable IPsec VPN
  --enable_pfs / --disable_pfs    enable/disable PFS of IPsec VPN
  -h, --help                      Show this message and exit.

```
