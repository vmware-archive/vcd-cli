```
Usage: vcd nsxt [OPTIONS] COMMAND [ARGS]...

  Manage NSX-T managers in vCloud Director (for VCD API v31.0)

      Examples
          vcd nsxt register nsxt-name
              --url 'https://<FQDN or IP address> of NSX-T host'
              --user 'nsxt-admin-user-name'
              --password 'nsxt-admin-user-password'
              --desc 'description of nsxt-manager'
                  Register an NSX-T manager.
  
          vcd nsxt unregister nsxt-name
              Unregister an NSX-T manager.
  
          vcd nsxt list
              List all registered NSX-T managers.
      

Options:
  -h, --help  Show this message and exit.

Commands:
  list        list NSX-T managers
  register    register NSX-T manager
  unregister  unregister NSX-T manager

```
