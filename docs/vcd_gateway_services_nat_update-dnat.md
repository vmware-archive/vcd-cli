```
Usage: vcd gateway services nat update-dnat [OPTIONS] <gateway name> <nat rule
                                            id>

Options:
  -o, --original-ip <ip/ip range>
                                  Original IP address/Range of DNAT Rule
  -t, --translated-ip <ip/ip range>
                                  Translated IP address/Range of DNAT Rule
  --enabled / --disable           enable/disable the DNAT rule
  --logging-enabled / --logging-disable
                                  enable logging
  --desc <description>            description
  --vnic <vnic>                   interface of gateway
  -p, --protocol <tcp/udp/icmp>   interface of gateway
  -op, --original-Port <vnic>     original port
  -tp, --translated-Port <vnic>   translated port
  -h, --help                      Show this message and exit.

```
