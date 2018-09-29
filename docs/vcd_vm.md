```
Usage: vcd vm [OPTIONS] COMMAND [ARGS]...

  Manage VMs in vCloud Director.

      Examples
          vcd vm list
              Get list of VMs in current virtual datacenter.
  
          vcd vm info vapp1 vm1
              Get details of the VM 'vm1' in vApp 'vapp1'.
  
          vcd vm update vapp1 vm1 --cpu 2 --core 2
              Modifies the VM 'vm1' in vApp 'vapp1' to be configured
              with 2 cpu and 2 cores .
  
          vcd vm update vapp1 vm1 --memory 512
              Modifies the VM 'vm1' in vApp 'vapp1' to be configured
              with the specified memory .
  
          vcd vm update vapp1 vm1 --cpu 2 --memory 512
              Modifies the VM 'vm1' in vApp 'vapp1' to be configured
              with 2 cpu and the specified memory .
      

Options:
  -h, --help  Show this message and exit.

Commands:
  info    show VM details
  list    list VMs
  update  Update the VM properties and configurations

```
