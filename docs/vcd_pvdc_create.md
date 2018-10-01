```
Usage: vcd pvdc create [OPTIONS] <pvdc-name> <vc-name>

Options:
  -s, --storage-profile TEXT      storage profile name (required parameter,
                                  can have multiple)  [required]
  -r, --resource-pool TEXT        resource pool name (required parameter, can
                                  have multiple)  [required]
  -n, --vxlan-network-pool [vxlan-network-pool]
                                  vxlan network pool name
  -t, --nsxt-manager-name [nsxt-manager-name]
                                  nsx-t manager name (valid for vCD API
                                  version 31.0 and above)
  -d, --description [description]
                                  description of PVDC
  -e, --enable                    enable flag (enables PVDC when it is
                                  created)
  -v, --highest-supp-hw-vers [highest-supp-hw-vers]
                                  highest supported hw version, e.g. vmx-11,
                                  vmx-10, vmx-09, etc.
  -h, --help                      Show this message and exit.

```
