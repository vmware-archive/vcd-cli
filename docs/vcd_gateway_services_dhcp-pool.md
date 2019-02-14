```
Usage: vcd gateway services dhcp-pool [OPTIONS] COMMAND [ARGS]...

  Manages DHCP pool of gateway.

      Examples
          vcd gateway services dhcp-pool create gateway1 --range 30.20.10.11-
          30.20.10.15 --enable-auto-dns --gateway-ip 30.20.10.1 --domain
          abc.com --primary-server 30.20.10.20 --secondary-server 30.20.10.21
          --expire-lease --lease 8640 --subnet 255.255.255.0

          Create dhcp rule.          vcd gateway services dhcp-pool delete
          test_gateway1 pool-1             Deletes the DHCP pool 
          vcd gateway services dhcp-pool list test_gateway1
          Lists the DHCP pool          vcd gateway services dhcp-pool info
          test_gateway1 pool-1             Info DHCP pool

Options:
  -h, --help  Show this message and exit.

Commands:
  create  create new DHCP pool
  delete  deletes the DHCP pool
  info    info about DHCP pool
  list    lists the DHCP pool

```
