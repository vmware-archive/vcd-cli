```
Usage: vcd vc [OPTIONS] COMMAND [ARGS]...

  Manage vCenter Servers in vCloud Director.

      Examples
          vcd vc list
              Get list of vCenter Servers attached to the vCD system.
  
          vcd vc info vc1
              Get details of the vCenter Server 'vc1' attached to the vCD system.
  
          vcd vc attach vc-name
              --vc-host 'vc.server.example.com' (or something similar)
              --vc-user 'vc-admin-user-name'
              --vc-pwd 'vc-admin-user-password'
              --enable 'true' (or 'false')
              --vc-root-folder 'vc-root-folder' (for VCD API version 31.0)
              --nsx-server-name 'nsx-server-namespace'
              --nsx-host 'nsx.server.example.com' (or something similar)
              --nsx-user 'nsx-admin-user-name'
              --nsx-pwd 'nsx-admin-password'
                  Attaches Virtual Center (VC) server with the given
                  credentials to vCD.

          vcd vc enable vc-name             Enable specified Virtual Center.

          vcd vc disable vc-name             Disable specified Virtucal
          Center.

          vcd vc detach vc-name             Detach (unregister) Virtual
          Center.

          vcd vc list-available-port-groups vc-name             lists the
          available portgroups in a particular vCenter

Options:
  -h, --help  Show this message and exit.

Commands:
  attach                      attach vCenter Server
  detach                      detach vCenter
  disable                     disable vCenter
  enable                      enable vCenter
  info                        show vCenter details
  list                        list vCenter Servers
  list-available-port-groups  list avaliable portgroups in vc

```
