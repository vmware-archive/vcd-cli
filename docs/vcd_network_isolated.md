```
Usage: vcd network isolated [OPTIONS] COMMAND [ARGS]...

  Work with isolated org vdc networks.

      Examples
          vcd network isolated create isolated-net1 --gateway-ip 192.168.1.1 \
              --netmask 255.255.255.0 --description 'Isolated VDC network' \
              --primary-dns-ip 8.8.8.8 --dns-suffix example.com \
              --ip-range-start 192.168.1.100 --ip-range-end 192.168.1.199 \
              --dhcp-enabled --default-lease-time 3600 \
              --max-lease-time 7200 --dhcp-ip-range-start 192.168.1.100 \
              --dhcp-ip-range-end 192.168.1.199
              Create an isolated org vdc network with an inbuilt dhcp service.
      

Options:
  -h, --help  Show this message and exit.

Commands:
  create  create a new isolated org vdc network in vcd

```
