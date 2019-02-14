```
Usage: vcd gateway [OPTIONS] COMMAND [ARGS]...

  Manage edge gateways in vCloud Director.

      Examples
          vcd gateway list
              Get list of edge gateways in current virtual datacenter.

          vcd gateway info name
              Display gateway details.

          vcd gateway create gateway1
                  --description test_gateway
                  --external-network external-net1
                  --external-network external-net2
                  --default-gateway external-net1
                  --default-gateway-ip 10.10.20.1
                  --dns-relay-enabled
                  --gateway-config full
                  --ha-disabled
                  --advanced-enabled
                  --distributed-routing-enabled
                  --configure-ip-setting external-net1 10.10.20.1/24 10.10.20.3
                  --sub-allocate-ip external-net1
                  --subnet 10.10.20.1/28 --ip-range 10.10.20.5-10.10.20.10
                  --configure-rate-limit external-net1 100 200
                  --flip-flop-disabled
                  --gateway-type NSXT_BACKED
              Create gateway.
                  Parameters:
                      --external-network is a required parameter and can have
                      multiple entries.
                     --gateway-config values can be compact/full/x-large/full4.
                     --gateway-type values can be
                     NSXV_BACKED/NSXT_BACKED/NSXT_IMPORTED.

          vcd gateway delete gateway1
               Delete gateway by providing gateway name.

          vcd gateway enable-distributed-routing gateway1 --disable
              Enable/Disable Distributed routing for gateway.

          vcd gateway modify-form-factor gateway1 full4
              Possible value for gateway configuration are
              compact/full/x-large/full4

          vcd gateway convert-to-advanced gateway1
               Convert gateway to advanced by providing gateway name

          vcd gateway redeploy gateway1
               Redeploys the gateway with given name

          vcd gateway sync-syslog-settings gateway1
               Synchronizes syslog settings of the gateway with given name

          vcd gateway list-syslog-server gateway1
               List syslog server of the gateway with given name

          vcd gateway list-config-ip-settings gateway1
               Lists the config ip settings of the gateway with given name
  
          vcd gateway update gateway1 -n gateway2 --description description
                  --ha-enabled
              Update name, description and HA of gateway

          vcd gateway configure-ip-settings gateway1 --external-network
                  extNetwork --subnet-available 10.20.30.1/24 True 10.20.30.3
               Edits the config ip settings of the gateway with given name
               Parameter:
                   --subnet-available is a required parameter and can have
                   multiple entries
      

Options:
  -h, --help  Show this message and exit.

Commands:
  configure-default-gateway   configures the defaultgateway
  configure-external-network  configures external networks of an edge gateway
  configure-ip-settings       edit config ip settings.
  configure-rate-limits       configures rate limits of gateway
  convert-to-advanced         convert to advanced gateway
  create                      create edge gateway
  delete                      delete edge gateway
  enable-distributed-routing  enable distributed routing for gateway
  info                        show gateway information.
  list                        list edge gateways
  list-config-ip-settings     shows config ip settings.
  list-syslog-server          list tenant syslog server of the given gateway
  modify-form-factor          modify form factor for gateway
  redeploy                    redeploy the given gateway
  services                    manage gateway configure services
  sub-allocate-ip             configures Sub allocate ip pools of gateway
  sync-syslog-settings        sync syslog settings of the given gateway
  update                      update name, description and HA of gateway.

```
