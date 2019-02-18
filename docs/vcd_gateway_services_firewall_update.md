```
Usage: vcd gateway services firewall update [OPTIONS] <gateway name> <rule id>

Options:
  --source <value:value_type>     it should be in value:value_type format. for
                                  ex: Extnw:gatewayinterface
  --destination <value:value_type>
                                  it should be in value:value_type format. for
                                  ex: Extnw:gatewayinterface
  --service <protocol> <source port> <destination port>
                                  configure services of firewall
  --name <name>                   new name of the firewall rule
  -h, --help                      Show this message and exit.

```
