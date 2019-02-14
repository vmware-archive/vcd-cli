```
Usage: vcd network routed [OPTIONS] COMMAND [ARGS]...

  Work with routed org vdc networks.

      Examples
          vcd network routed create routed_net1
                  --gateway-name gateway1
                  --subnet 5.5.6.1/20
                  --description 'Routed VDC network'
                  --dns1 7.7.7.3
                  --dns2 7.7.7.4
                  --dns-suffix example.com
                  --ip-range 5.5.6.2-5.5.6.100
                  --shared-enabled
                  --guest-vlan-allowed-enabled
                  --sub-interface-enabled
                  --distributed-interface-enabled
                  --retain-net-info-across-deployments-enabled
              Creates a routed org vdc network
  
          vcd network routed update routed_net1
                  --name new_name
                  --description new_description
                  --shared-enabled/--shared-disabled
              Update name, description and shared state of org vdc network

          vcd network routed add-ip-range routed_net1
                  --ip-range  2.2.3.1-2.2.3.2
                  --ip-range 2.2.4.1-2.2.4.2
              Add IP range/s to a routed org vdc network

          vcd network routed update-ip-range routed_net1
                  --ip-range 192.168.1.2-192.168.1.20
                  --new-ip-range 192.168.1.25-192.168.1.50
              Update an IP range of a routed org vdc network

          vcd network routed delete-ip-range routed_net1
                  --ip-range 192.168.1.2-192.168.1.20
              Delete an IP range from a routed org vdc network

          vcd network routed list
              List all routed org vdc networks in the selected vdc

          vcd network routed set-metadata routed_net1 --key key1 --value value1
              Set a metadata entry in a routed org vdc network with default
              domain, visibility and metadata value type

          vcd network routed remove-metadata routed_net1 --key key1
              Remove a metadata entry from a routed org vdc network

          vcd network routed list-metadata routed_net1
              List all metadata entries in a routed org vdc network

          vcd network routed list-allocated-ip routed_net1
              List all allocated IP in a routed org vdc network

          vcd network routed list-connected-vapps routed_net1
              List all connected vApps in a routed org vdc network

          vcd network routed add-dns routed_net1
                  --dns1 2.2.3.1
                  --dns2 2.2.3.2
                  --dns-suffix domain.com
              Add DNS details to a routed org vdc network

          vcd network routed convert-to-sub-interface routed_net1
              Convert routed org vdc network to sub interface

          vcd network routed convert-to-internal-interface routed_net1
              Convert routed org vdc network to internal interface

          vcd network routed convert-to-distributed-interface routed_net1
              Convert routed org vdc network to distributed interface

          vcd network routed info routed_net1
              Show routed vdc network details



Options:
  -h, --help  Show this message and exit.

Commands:
  add-dns                         add DNS to routed org vdc network
  add-ip-range                    add IP range/s to routed org vdc network
  convert-to-distributed-interface
                                  convert to distributed interface
  convert-to-internal-interface   convert to internal interface
  convert-to-sub-interface        convert to sub interface
  create                          create a routed org vdc network
  delete                          delete org vdc routed network
  delete-ip-range                 delete an IP range from a routed org vdc
                                  network
  edit                            Edit a routed org vdc network
  info                            show routed network information
  list                            list all routed org vdc networks in the
                                  selected vdc
  list-allocated-ip               list allocated IP addresses
  list-connected-vapps            list connected vApps
  list-metadata                   list metadata of a routed org vdc network
  remove-metadata                 remove metadata from a routed org vdc
                                  network
  set-metadata                    set metadata to a routed org vdc network
  update-ip-range                 Update IP range of routed org vdc network.

```
