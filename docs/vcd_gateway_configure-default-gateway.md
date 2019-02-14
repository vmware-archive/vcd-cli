```
Usage: vcd gateway configure-default-gateway [OPTIONS] COMMAND [ARGS]...

  Configures the default gateway in vCloud Director.

      Examples
          vcd gateway configure-default-gateway update gateway1
              -e extNw1 --gateway-ip 2.2.3.1 --enable
              updates default gateway.
  
          vcd gateway configure-default-gateway enable-dns-relay gateway1
              --enable
              enables the dns relay.
  
          vcd gateway configure-default-gateway list gateway1
              lists the configured default gateway.



Options:
  -h, --help  Show this message and exit.

Commands:
  enable-dns-relay  enables/disables the dns relay
  list              lists the configure default gateway
  update            configures the default gateway

```
