```
Usage: vcd network external [OPTIONS] COMMAND [ARGS]...

  Work with external networks.

      Note
          Only System Administrators can work with external networks.

      Examples
          vcd network external list
              List all external networks available in the system

          vcd network external create external-net1
                  --vc vc1
                  --port-group pg1
                  --gateway 192.168.1.1
                  --netmask 255.255.255.0
                  --ip-range 192.168.1.2-192.168.1.49
                  --ip-range 192.168.1.100-192.168.1.149
                  --description 'External network'
                  --dns1 8.8.8.8
                  --dns2 8.8.8.9
                  --dns-suffix example.com
              Create an external network.
                  Parameter --ip-range can have multiple entries.

          vcd network external delete external-net1
              Delete an external network.

          vcd network external update external-net1
                  --name 'new-external-net1'
                  --description 'New external network'
              Update name and description of an external network.

          vcd network external add-subnet external-net1
                  --gateway 192.168.1.1
                  --netmask 255.255.255.0
                  --ip-range 192.168.1.2-192.168.1.49
                  --dns1 8.8.8.8
                  --dns2 8.8.8.9
                  --dns-suffix example.com
              Add subnet to external network.
                  Parameter ip-range can have multiple entries.

          vcd network external enable-subnet external-net1
                  --gateway 192.168.1.1
                  --enable/--disable
              Enable/Disable subnet of an external network.

          vcd network external add-ip-range external-net1
                  --gateway 192.168.1.1
                  --ip-range 192.168.1.2-192.168.1.20
              Add an IP range to an external network.

          vcd network external update-ip-range external-net1
                  --gateway 192.168.1.1
                  --ip-range 192.168.1.2-192.168.1.20
                  --new-ip-range 192.168.1.25-192.168.1.50
              Update an IP range in an external network.

          vcd network external delete-ip-range external-net1
                  --gateway 192.168.1.1
                  --ip-range 192.168.1.2-192.168.1.20
              Delete an IP range from an external network.

          vcd network external attach-port-group external-net1
                  --vc vc1
                  --port-group pg1
              Attach a port group to an external network.

          vcd network external detach-port-group external-net1
                  --vc vc1
                  --port-group pg1
              Detach a port group from an external network.

          vcd network external list-pvdc external-net1
                  --filter name==pvdc*
              List available provider vdcs

          vcd network external list-gateway external-net1
                  --filter name==gateway*
              List associated gateways

          vcd network external list-allocated-ip external-net1
                  --filter name==gateway*
              List allocated ip

          vcd network external list-sub-allocated-ip external-net1
                  --filter name==gateway*
              List sub allocated ip

          vcd network external list-direct-org-vdc-network external-net1
                  --filter name==org-vdc-net*
              List associated direct org vDC networks

          vcd network external list-vsphere-network external-net1
                  --filter name==portgroup*
              List associated vSphere Networks

          vcd network external info external-net1
              Show external network details.
      

Options:
  -h, --help  Show this message and exit.

Commands:
  add-ip-range                 add an IP range to a subnet in an external
                               network
  add-subnet                   add subnet to an external network
  attach-port-group            attach a port group to an external network
  create                       create a new external network
  delete                       delete an external network
  delete-ip-range              delete an IP range of a subnet in an external
                               network
  detach-port-group            detach port group from an external network
  enable-subnet                enable subnet of an external network
  info                         show external network details
  list                         list all external networks in the system
  list-allocated-ip            list allocated IP
  list-direct-org-vdc-network  list associated direct org vDC networks.
  list-gateway                 list associated gateways
  list-pvdc                    list associated pvdcs
  list-sub-allocated-ip        list sub allocated IP
  list-vsphere-network         list associated vSphere networks
  update                       update name and description of an external
                               network
  update-ip-range              update an IP range of a subnet in an external
                               network

```
