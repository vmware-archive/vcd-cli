```
Usage: vcd pvdc [OPTIONS] COMMAND [ARGS]...

  Work with provider virtual datacenters in vCloud Director.

      Examples
          vcd pvdc list
              Get list of provider virtual datacenters.
  
          vcd pvdc info name
              Display provider virtual data center details.
  
          vcd pvdc create pvdc-name vc-name \
                  --storage-profile 'sp1' \
                  --storage-profile 'sp2' \
                  --resource-pool 'rp1' \
                  --resource-pool 'rp2' \
                  --vxlan-network-pool 'vnp1' \
                  --nsxt-manager-name 'nsx-t manager name' \ (API version 31.0)
                  --highest-supp-hw-vers 'vmx-11' \
                  --description 'description' \
                  --enable
              Create Provider Virtual Datacenter.
                  Parameters --storage-profile and --resource-pool are both
                  required parameters and each can have multiple entries.
  
          vcd pvdc attach-rp pvdc-name rp1 rp2 ... (one or more rp names)
              Attach one or more resource pools to a Provider vDC.
  
          vcd pvdc detach-rp pvdc-name rp1 rp2 ... (one or more rp names)
              Detach one or more resource pools from a Provider vDC.
  
          Caveat: The current implementation of the attach-rp and detach-rp
          functions take a list of RP "basenames" as input. A basename is the
          last element of a full pathname. For example, given a pathname /a/b/c,
          the basename of that pathname is "c". Since RP names are only required
          to have unique pathnames but not unique basenames, this function may
          not work correctly if there are non-unique RP basenames. Therefore, in
          order to use these functions, all RP basenames must be unique. It is
          up to the user of these functions to be aware of this limitation and
          name their RPs appropriately. This limitation will be fixed in a future
          version of these functions.
  
          vcd pvdc add-sp pvdc-name sp1 sp2 ... (one or more storage profiles)
              Add one or more storage profiles to a Provider vDC.
  
          vcd pvdc del-sp pvdc-name sp1 sp2 ... (one or more storage profiles)
              Delete one or more storage profiles from a Provider vDC.
  
          vcd pvdc migrate-vms pvdc-name rp1 vm1 vm2 ... --target-rp rp2
              Migrate one or more VMs from the source resource pool (rp1)
              to the target-rp (rp2 in this example, which is the target
              resource pool, an optional parameter). If the target-rp isn't
              specified, any available resource pool is chosen automatically.
      

Options:
  -h, --help  Show this message and exit.

Commands:
  add-sp       add storage profiles to a pvdc
  attach-rp    attach resource pools to a pvdc
  create       create pvdc
  del-sp       delete storage profiles from a pvdc
  detach-rp    detach resource pools from a pvdc
  info         show pvdc details
  list         list of provider virtual datacenters
  migrate-vms  migrate vms to another resource pool

```
