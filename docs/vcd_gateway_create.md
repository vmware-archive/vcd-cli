```
Usage: vcd gateway create [OPTIONS] <name>

Options:
  -e, --external-network <external network>
                                  list of external networks to which the new
                                  gateway can connect.  [required]
  --description <description>     description
  --default-gateway <external_network>
                                  name of external network for default gateway
                                  configuration
  --default-gateway-ip <default gateway IP>
                                  IP from the external network for the default
                                  gateway
  --dns-relay-enabled / --dns-relay-disabled
                                  DNS relay enabled/disabled
  -c, --gateway-config <gateway_config>
                                  gateway configuration
  --ha-enabled / --ha-disabled    HA enabled
  --advanced-enabled / --advanced-disabled
                                  advanced gateway
  --distributed-routing-enabled / --distributed-routing-disabled
                                  enable distributed routing for networks
                                  connected to this gateway.
  --configure-ip-setting <external network> <subnet> <configured IP>
                                  configuring multiple ip settings
  --sub-allocate-ip <external network>
                                  sub-allocate the IP Pools provided by the
                                  externally connected interfaces
  --subnet <external network subnet>
                                  subnet for the selected external network for
                                  IP sub allocation
  --ip-range <IP ranges>          IP ranges pertaining to external network's
                                  IP Pool
  --configure-rate-limit <external network> <incoming rate limit> <outgoing rate limit>
                                  specify the inbound and outbound rate limits
                                  for each externally connected interface.
  --flip-flop-enabled / --flip-flop-disabled
                                  flip flip mode
  --gateway-type NSXV_BACKED/NSXT_BACKED/NSXT_IMPORTED
                                  gateway type
  -h, --help                      Show this message and exit.

```
