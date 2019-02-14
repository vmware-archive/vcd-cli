```
Usage: vcd network direct [OPTIONS] COMMAND [ARGS]...

  Work with directly connected org vdc networks.

      Note
          System Administrators have full control on direct org vdc networks.
          Organization Administrators can only list direct org vdc networks.
  
      Examples
          vcd network direct create direct-net1
                  --description 'Directly connected VDC network'
                  --parent ext-net1
              Create an org vdc network which is directly connected
              to an external network.
  
          vcd network direct list
              List all directly connected org vdc networks in the selected vdc
  
          vcd network direct delete direct-net1
              Delete directly connected network 'direct-net1' in the selected vdc
      

Options:
  -h, --help  Show this message and exit.

Commands:
  create  create a new directly connected org vdc network in vcd
  delete  delete a directly connected org vdc network in the selected vdc
  list    list all directly connected org vdc networks in the selected vdc

```
