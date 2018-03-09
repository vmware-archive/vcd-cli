```
Usage: vcd pvdc [OPTIONS] COMMAND [ARGS]...

  Work with provider virtual datacenter in vCloud Director.

      Examples
          vcd pvdc list
              Get list of provider virtual datacenters.
  
          vcd pvdc info name
              Display provider virtual data center details.
  
          vcd pvdc create pvdc-name vc-name
              --storage-profile 'sp1'
              --storage-profile 'sp2'
              --resource-pool 'rp1'
              --resource-pool 'rp2'
              --vxlan-network-pool 'vnp1'
              --highest-supported-hw-version 'vmx-11'
              --description 'description'
              --enable
                  Create Provider Virtual Datacenter.
                     Parameters --storage-profile and --resource-pool are both
                     required parameters and each can have multiple entries.
      

Options:
  -h, --help  Show this message and exit.

Commands:
  create  create pvdc
  info    show pvdc details
  list    list of provider virtual datacenters

```
