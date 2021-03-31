```
Usage: vcd vapp network services nat add [OPTIONS] <vapp-name> <network-name>

Options:
  --type <type>                  type of NAT service  [required]
  --vm_id <vm_id>                VM local id  [required]
  --nic_id <nic_id>              NIC id of vapp network in vm   [required]
  --mapping_mode <mapping_mode>  mapping mode of NAT rule
  --ext_ip <ext_ip>              external IP address
  --ext_port <ext_port>          external port
  --int_port <int_port>          internal port
  --protocol <protocol>          protocol
  -h, --help                     Show this message and exit.

```
