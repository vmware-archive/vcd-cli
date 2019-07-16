```
Usage: vcd gateway services ipsec-vpn update [OPTIONS] <gateway name> <local
                                             end point-peer end point>

Options:
  --new-name <IPsec VPN name>     IPsec VPN name
  -lid, --local-id <local-id>     Local id of IPsec VPN.
  -pid, --peer-id <peer-id>       Peer id of IPsec VPN.
  -lip, --local-ip <local-ip>     Local IP/Local end point of IPsec VPN.
  -pip, --peer-ip <peer-ip>       Peer IP/Peer end point of IPsec VPN.
  -lsubnet, --local-subnet <local-subnet>
                                  Local subnets of IPsec VPN.These should be
                                  given comma separated.
  -psubnet, --peer-subnet <peer-subnet>
                                  Peer subnets of IPsec VPN.These should be
                                  given comma separated.
  -psk, --pre-shared-key <pre-shared-key>
                                  Pre shared key of IPsec VPN.
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
