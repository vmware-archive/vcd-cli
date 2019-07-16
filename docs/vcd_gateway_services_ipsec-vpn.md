```
Usage: vcd gateway services ipsec-vpn [OPTIONS] COMMAND [ARGS]...

  Manages IPsec VPN of gateway.

      Examples
          vcd gateway services ipsec-vpn create test_gateway1
                  --name name
                  --local-id lid1
                  --local-ip 2.2.3.2
                  --peer-id pid1
                  --peer-ip 2.2.3.4
                  --local-subnet 30.20.10.0/24
                  --peer-subnet 10.20.10.0/24
                  --desc "IPsec VPN"
                  --psk abcd1234
                  --enable
              Creates new IPsec VPN.

          vcd gateway services ipsec-vpn update test_gateway1 2.2.3.2-2.2.3.3
                  --new-name new_name
                  --enable
              Updates IPsec VPN with new values.

          vcd gateway services ipsec-vpn enable-activation-status test_gateway1
                  --enable
              Enable/disable activation status.

          vcd gateway services ipsec-vpn info-activation-status test_gateway1
              Info activation status.

          vcd gateway services ipsec-vpn enable-logging test_gateway1
                  --enable
              Enable/disable logging.

          vcd gateway services ipsec-vpn info-logging-settings test_gateway1
              Info logging settings.

          vcd gateway services ipsec-vpn set-log-level test_gateway1 warning
              Set global log level for IPsec VPN.

          vcd gateway services ipsec-vpn list test_gateway1
              List IPsec VPN of a gateway.

          vcd gateway services ipsec-vpn change-shared-key test_gateway1
                  new_shared_key
              Change shared key of IPsec VPN.

          vcd gateway services ipsec-vpn info test_gateway1
                  2.2.3.2-2.2.3.3
              Get details of IPsec VPN.

          vcd gateway services ipsec-vpn delete test_gateway1 2.2.3.2-2.2.3.3
              Deletes IPsec VPN.

Options:
  -h, --help  Show this message and exit.

Commands:
  change-shared-key         change shared key
  create                    create new IPsec VPN
  delete                    Deletes the IPsec VPN
  enable-activation-status  enable activation status
  enable-logging            enable logging of IPsec VPN.
  info                      get details of ipsec vpn
  info-activation-status    info activation status
  info-logging-settings     info logging settings
  list                      list ipsec vpn
  set-log-level             set log level of IPsec VPN. It's value should be
                            from the domain:{emergency, alert, critical,
                            error, warning, notice, info, debug)
  update                    update IPsec VPN

```
