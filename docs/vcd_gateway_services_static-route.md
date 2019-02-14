```
Usage: vcd gateway services static-route [OPTIONS] COMMAND [ARGS]...

  Manages static routes of gateway.

          Examples
              vcd gateway services static-route create test_gateway1 --type User
                      --network 192.169.1.0/24 --next-hop 2.2.3.30 --mtu 1500
                      --desc "Static Route Created" -v 0
                  Create a new static route

              vcd gateway services static-route list test_gateway1
                  List all static routes

              vcd gateway services static-route delete test_gateway1
                      192.169.1.0/24
                  Delete the static route

              vcd gateway services static-route update test_gateway1
                      192.169.1.0/24 --network 192.165.1.0/24 --next-hop 2.2.3.35
                      --mtu 1800 --desc "Static Route Updated" -v 0
                  Update the static route
      

Options:
  -h, --help  Show this message and exit.

Commands:
  create  create a new static route
  delete  Deletes the static route
  list    List all static routes on a gateway
  update  Update the static route

```
