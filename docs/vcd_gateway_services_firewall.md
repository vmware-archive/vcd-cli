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

          vcd gateway services firewall list-destination test_gateway1
                  rule_id
              List firewall rule's destination

          vcd gateway services firewall reorder test_gateway1 rule_id
                  --index new_index
              Reorder the firewall rule position on gateway

          vcd gateway services firewall delete-source test_gateway1 rule_id
                  source_value
              Delete all source value of firewall rule by providing
                  source_value

          vcd gateway services firewall delete-destination test_gateway1
                  rule_id destination_value
              Delete all destination value of firewall rule by providing
                  destination_value

          vcd gateway services firewall list-service test_gateway1 rule_id
              List firewall rule's services

          vcd gateway services firewall delete-service test_gateway1 rule_id
                  protocol
              Delete all services of firewall rule by providing protocol.

Options:
  -h, --help  Show this message and exit.

Commands:
  create              create new firewall rule
  delete              delete firewall rule
  delete-destination  delete firewall rule's destination value of a firewall
                      rule
  delete-service      delete firewall rule's service of a firewall rule
  delete-source       delete firewall rule's source value of a firewall rule
  disable             disable firewall rule
  enable              enable firewall rule
  info                info about firewall rule
  list                show all firewall rule
  list-destination    list of firewall rule's destination
  list-object-types   list object types
  list-objects        list objects for provided object type
  list-service        list firewall rule's services
  list-source         list of firewall rule's source
  reorder             reorder firewall rule position on gateway
  update              update firewall rule

```
