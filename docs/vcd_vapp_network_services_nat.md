```
Usage: vcd vapp network services nat [OPTIONS] COMMAND [ARGS]...

  Manages NAT service of vapp network.

      Examples
          vcd vapp network services nat enable-nat vapp_name network_name
                  --enable
              Enable NAT service.

      vcd vapp network services nat set-nat-type vapp_name network_name
              --type ipTranslation --policy allowTrafficIn
          Set NAT type in NAT service.

      vcd vapp network services nat get-nat-type vapp_name network_name
          Get  NAT type and policy in NAT service.

      vcd vapp network services nat add vapp_name network_name
              --type ipTranslation --vm_id testvm1 --nic_id 1
          Add  NAT rule to NAT service.

      vcd vapp network services nat add vapp_name network_name
              --type ipTranslation --vm_id testvm1 --nic_id 1 --mapping_mode
               manual --ext_ip 10.1.1.1
          Add  NAT rule to NAT service.

      vcd vapp network services nat add vapp_name network_name
              --type portForwarding  --vm_id testvm1 --nic_id 1 --ext_port -1
              --int_port -1 --protocol TCP_UDP
          Add  NAT rule to NAT service.

      vcd vapp network services nat list vapp_name network_name
          List NAT rules in NAT service.

      vcd vapp network services nat delete vapp_name network_name id
          Delete NAT rule from NAT service.

      vcd vapp network services nat update vapp_name network_name rule_id
          --vm_id testvm1 --nic_id 1
          Update  NAT rule to NAT service.

      vcd vapp network services nat update vapp_name network_name rule_id
              --vm_id testvm1 --nic_id 1 --mapping_mode manual
              --ext_ip 10.1.1.1
          Update  NAT rule to NAT service.

      vcd vapp network services nat update vapp_name network_name rule_id
              --vm_id testvm1 --nic_id 1 --ext_port -1 --int_port -1
              --protocol TCP_UDP
          Update  NAT rule to NAT service.

Options:
  -h, --help  Show this message and exit.

Commands:
  add           add NAT rule
  delete        delete NAT rules
  enable-nat    enable NAT service
  get-nat-type  get NAT type
  list          list NAT rules
  set-nat-type  set NAT type
  update        update NAT rule

```
