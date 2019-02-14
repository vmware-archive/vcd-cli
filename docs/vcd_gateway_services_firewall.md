```
Usage: vcd gateway services firewall [OPTIONS] COMMAND [ARGS]...

  Manages firewall Rule of gateway.

      Examples
          vcd gateway services firewall create test_gateway1 --name rule1
                  --action accept --type User
                  --enabled --logging-enabled

              create new firewall rule

          vcd gateway services firewall list test_gateway1
              List firewall rules

          vcd gateway services firewall list-object-types test_gateway1
                  --type source
              List of object types

          vcd gateway services firewall list-objects test_gateway1
                  --type source --object-type gatewayinterface
              List of object for provided object type

          vcd gateway services firewall update test_gateway1 rule_id
                  --destination ExtNw:gatewayinterface
                  --destination ExtNw1:gatewayinterface
                  --destination vm1:virtualmachine
                  --source ExtNw:gatewayinterface
                  --source 10.20.3.2:ip
                  --service tcp any any
                  --name new_name
              Edit firewall rule

          vcd gateway services firewall enable test_gateway1 rule_id
              enabled firewall rule

          vcd gateway services firewall disable test_gateway1 rule_id
              disabled firewall rule

          vcd gateway services firewall delete test_gateway1 rule_id
              delete firewall rule

          vcd gateway services firewall info test_gateway1 rule_id
              Info firewall rule

          vcd gateway services firewall list-source test_gateway1 rule_id
              List firewall rule's source

          vcd gateway services firewall update-sequence test_gateway1 rule_id
                  --index new_index
              Change sequence of firewall rule

Options:
  -h, --help  Show this message and exit.

Commands:
  create             create new firewall rule
  delete             delete firewall rule
  disable            disable firewall rule
  enable             enable firewall rule
  info               info about firewall rule
  list               show all firewall rule
  list-object-types  list object types
  list-objects       list objects for provided object type
  list-source        list of firewall rule's source
  update             update firewall rule
  update-sequence    update sequence of firewall rule

```
