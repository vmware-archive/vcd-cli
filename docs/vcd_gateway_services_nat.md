```
Usage: vcd gateway services nat [OPTIONS] COMMAND [ARGS]...

  Manages SNAT/DNAT Rule of gateway.

          Examples
              vcd gateway services nat create-snat test_gateway1
                      --original-ip 2.2.3.12 --translated-ip 2.2.3.14 --desc
                      "SNAT Created" --vnic 0 --enabled --logging-enabled
                  Create new SNAT rule

               vcd gateway services nat update-snat test_gateway1 196609
                       --original-ip 2.2.3.12 --translated-ip 2.2.3.14 --desc
                       "SNAT Updated" --vnic 0
                   Update SNAT rule

              vcd gateway services nat create-dnat test_gateway1
                      --original-ip 2.2.3.12 --translated-ip 2.2.3.14 --desc
                      "DNAT Created" --vnic 0 --protocol tcp -op 80 -tp 80
                      --enabled --logging-enabled
                  Create new DNAT rule

              vcd gateway services nat update-dnat test_gateway1 196609
                       --original-ip 2.2.3.12 --translated-ip 2.2.3.14 --desc
                       "DNAT Updated" --vnic 0 --protocol udp -op 80 -tp 80
                  Update DNAT rule

              vcd gateway services nat list test_gateway1
                  List all NAT rules

             vcd gateway services nat delete test_gateway1 196609
                 Deletes the NAT rule

             vcd gateway services nat info test_gateway1 196609
                 Get details of NAT rule

             vcd gateway services nat reorder test_gateway1 196609 --index 2
                 Reorder the NAT rule position on gateway
      

Options:
  -h, --help  Show this message and exit.

Commands:
  create-dnat  create new DNAT rule
  create-snat  create new SNAT rule
  delete       Deletes the NAT rule
  info         show NAT rule details
  list         List all NAT rules on a gateway
  reorder      reorder NAT rule position on gateway
  update-dnat  update DNAT rule
  update-snat  update SNAT rule

```
