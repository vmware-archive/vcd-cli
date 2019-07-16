```
Usage: vcd vapp network [OPTIONS] COMMAND [ARGS]...

  Work with vapp network.

     Description
          Work with the vapp networks.

          vdc vapp network create vapp1 vapp-network1
                  --subnet 192.168.1.1/24
                  --description 'vApp network'
                  --dns1 8.8.8.8
                  --dns2 8.8.8.9
                  --dns-suffix example.com
                  --ip-range 192.168.1.2-192.168.1.49
                  --ip-range 192.168.1.100-192.168.1.149
                  --guest-vlan-allowed-enabled
              Create a vApp network.

          vdc vapp network reset vapp1 vapp-network1
              Reset a vApp network.

          vdc vapp network delete vapp1 vapp-network1
              Delete a vApp network.

          vdc vapp network update vapp1 vapp-network1 -n NewName -d Description
              Update a vApp network.

          vdc vapp network add-ip-range vapp1 vapp-network1
                  --ip-range 6.6.5.2-6.6.5.20
              Add IP range to the vApp network.

          vdc vapp network delete-ip-range vapp1 vapp-network1
                  --ip-range 6.6.5.2-6.6.5.20
              Delete IP range from vApp network.

          vdc vapp network update-ip-range vapp1 vapp-network1
                  --ip-range 6.6.5.2-6.6.5.20 --new-ip-range 6.6.5.10-6.6.5.18
              Update IP range of vApp network.

          vdc vapp network add-dns vapp1 vapp-network1
                  --dns1 6.6.5.2 --dns2 6.6.5.10-6.6.5.18
                  --dns-suffix example.com
              Add DNS detail to vApp network.

          vdc vapp network update-dns vapp1 vapp-network1
                  --dns1 6.6.5.2 --dns2 6.6.5.10-6.6.5.18
                  --dns-suffix example.com
              Update DNS details of vApp network.

          vdc vapp network dns-info vapp1 vapp-network1
              Show DNS details of vapp network

          vcd vapp network list-allocated-ip vapp1 vapp-network1
              List allocated ip

          vcd vapp network list vapp1
              List vapp networks

          vcd vapp network connect-ovdc vapp1 vapp-network1 ovdc_network_name
              Connect a vapp network to org vdc network

          vcd vapp network sync-syslog-settings vapp1 vapp-network1
              Sync syslog settings of vapp network
      

Options:
  -h, --help  Show this message and exit.

Commands:
  add-dns               add DNS to vapp network
  add-ip-range          add IP range/s to the network
  connect-ovdc          connect a vapp network to org vdc network
  create                create a vApp network
  delete                delete a vApp network
  delete-ip-range       delete an IP range in network
  dns-info              show DNS details of vapp network
  list                  list vapp networks
  list-allocated-ip     list allocated IP
  reset                 reset a vApp network
  services              manage vapp network services
  sync-syslog-settings  sync syslog settings of vapp network
  update                update vapp network's name and description
  update-dns            update DNS details of vapp network
  update-ip-range       update IP range/s of the network

```
