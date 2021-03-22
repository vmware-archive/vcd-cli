```
Usage: vcd vapp network services firewall [OPTIONS] COMMAND [ARGS]...

  Manages firewall service of vapp network.

      Examples
          vcd vapp network services firewall enable-firewall vapp_name
                  network_name --enable
              Enable firewall service.

      vcd vapp network services firewall set-default-action vapp_name
              network_name --action allow --log-action False
          Set deault action in firewall service.

      vcd vapp network services firewall list vapp_name network_name
          List firewall rules in firewall service.

      vcd vapp network services firewall add vapp_name network_name rule_name
              --enable --policy drop --protocols Tcp,Udp --source-ip Any
               --source-port-range Any --destination-port-range Any
              --destination-ip Any --enable-logging
          Add firewall rule in firewall service.

      vcd vapp network services firewall update vapp_name network_name
              rule_name --name rule_new_name --enable --policy
              drop --protocols Tcp,Udp --source-ip Any
              --source-port-range Any --destination-port-range Any
              --destination-ip Any --enable-logging
          Update firewall rule in firewall service.

      vcd vapp network services firewall delete vapp_name network_name
              --name firewall_rule_name
          Delete firewall rule in firewall service.

Options:
  -h, --help  Show this message and exit.

Commands:
  add                 add firewall rule to firewall service
  delete              delete firewall rule in firewall service
  enable-firewall     Enable firewall service
  list                list firewall rules in firewall service
  set-default-action  set default action of firewall service
  update              update firewall rule of firewall service

```
