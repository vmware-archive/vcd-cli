```
Usage: vcd gateway services nat [OPTIONS] COMMAND [ARGS]...

  Manages SNAT/DNAT Rule of gateway.

          Examples
              vcd gateway services nat list test_gateway1
                  List all NAT rules

             vcd gateway services nat delete test_gateway1 196609
                 Deletes the NAT rule

             vcd gateway services nat info test_gateway1 196609
                 Get details of NAT rule
      

Options:
  -h, --help  Show this message and exit.

Commands:
  delete  Deletes the NAT rule
  info    show NAT rule details
  list    List all NAT rules on a gateway

```
