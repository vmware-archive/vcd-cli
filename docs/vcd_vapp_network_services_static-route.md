```
Usage: vcd vapp network services static-route [OPTIONS] COMMAND [ARGS]...

  Manage static route service of vapp network.

      vcd vapp network services static-route enable-service vapp_name
              network_name --enable
          Enable static route service.

      vcd vapp network services static-route enable-service vapp_name
              network_name --disable
          Disable static route service.

      vcd vapp network services static-route add vapp_name network_name
              --name route_name
              --nhip next_hop_ip
              --network network_cidr
          Add static route in static route service.

      vcd vapp network services static-route list vapp_name network_name
          List static route in static route service.

      vcd vapp network services static-route update vapp_name network_name
              route_name
              --name new_route_name
              --network network_cidr
              --nhip next_hop_ip
          Update static route in static route service.

      vcd vapp network services static-route delete vapp_name network_name
              route_name
          Delete static route in static route service.

Options:
  -h, --help  Show this message and exit.

Commands:
  add             add static route in static route service
  delete          delete static route in static route service
  enable-service  enable static route service
  list            list static route in static route service
  update          update static route in static route service

```
