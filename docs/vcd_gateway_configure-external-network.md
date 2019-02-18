```
Usage: vcd gateway configure-external-network [OPTIONS] COMMAND [ARGS]...

  Configures external networks of edge gateways in vCloud Director.

      Examples
          vcd gateway configure-external-network add gateway1
              --external_network extNw1
              --configure-ip-setting 10.10.10.1/28 10.10.10.9
              --configure-ip-setting 10.10.20.1/24 Auto
              Adds an external network to the edge gateway.

          vcd gateway configure-external-network remove gateway1
              -e extNw1
              Removes an external network from the edge gateway.
      

Options:
  -h, --help  Show this message and exit.

Commands:
  add     adds an external network to the edge gateway
  remove  removes an external network from the edge gateway

```
