```
Usage: vcd vapp network services dhcp [OPTIONS] COMMAND [ARGS]...

  Manages DHCP service of vapp network.

      Examples
          vcd vapp network services dhcp set vapp_name network_name --i
                  10.11.11.1-10.11.11.100 --default-lease-time 4500
                  --max-lease-time 7000
              Set dhcp service information

          vcd vapp network services dhcp enable-dhcp vapp_name network_name
                  --enable
              Enable DHCP service.

Options:
  -h, --help  Show this message and exit.

Commands:
  enable-dhcp  Enable DHCP Service
  set          Set DHCP service information

```
