```
Usage: vcd network isolated [OPTIONS] COMMAND [ARGS]...

  Work with isolated org vdc networks.

      Note
          Both System Administrators and Organization Administrators can create,
          delete or list isolated org vdc networks.
  
      Examples
          vcd network isolated create isolated-net1 --gateway 192.168.1.1
                  --netmask 255.255.255.0 --description 'Isolated VDC network'
                  --dns1 8.8.8.8 --dns2 8.8.8.9 --dns-suffix example.com
                  --ip-range-start 192.168.1.100 --ip-range-end 192.168.1.199
                  --dhcp-enabled --default-lease-time 3600
                  --max-lease-time 7200 --dhcp-ip-range-start 192.168.1.100
                  --dhcp-ip-range-end 192.168.1.199
              Create an isolated org vdc network with an inbuilt dhcp service.
  
          vcd network isolated list
              List all isolated org vdc networks in the selected vdc
  
          vcd network isolated delete isolated-net1
              Delete isolated network 'isoalted-net1' in the selected vdc
      

Options:
  -h, --help  Show this message and exit.

Commands:
  create  create a new isolated org vdc network in vcd
  delete  delete an isolated org vdc network in the selected vdc
  list    list all isolated org vdc networks in the selected vdc

```
