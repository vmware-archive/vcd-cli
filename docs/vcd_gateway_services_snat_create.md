```
Usage: vcd gateway services snat create [OPTIONS] <gateway name>

Options:
  --action <snat/dnat>            action
  --type <User>                   type
  -o, --original-ip <ip/ip range>
                                  Original IP address/Range of SNAT Rule
  -t, --translated-ip <ip/ip range>
                                  Translated IP address/Range of SNAT Rule
  --enabled / --disable           enable/disable the SNAT rule
  --logging-enabled / --logging-disable
                                  enable logging
  --desc <description>            description
  -v <vnic>                       interface of gateway
  -h, --help                      Show this message and exit.

```
