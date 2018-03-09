```
Usage: vcd right [OPTIONS] COMMAND [ARGS]...

  Work with rights

      Note
         All sub-commands execute in the context of organization specified
         via --org option; it defaults to current organization-in-use
         if --org option is not specified.

      Examples
          vcd right list -o myOrg
              Gets list of rights associated with the organization

          vcd right list --all
              Gets list of all rights available in the System

          vcd right info 'vCenter: View'
              Shows details of a given right
  
          vcd right add 'vApp: Copy' 'General: View Error Details' -o myOrg
              Adds list of rights to the organization

          vcd right remove 'vApp: Copy' 'Disk: Create' -o myOrg
              Removes list of rights from the organization
      

Options:
  -h, --help  Show this message and exit.

Commands:
  add     Add rights to the organization
  info    show details of a right
  list    lists rights in the current organization or System
  remove  remove rights from the organization

```
