```
Usage: vcd disk [OPTIONS] COMMAND [ARGS]...

  Manage independent disks in vCloud Director.

      Examples
          vcd disk list
              Get list of independent disks in the current virtual datacenter.
  
          vcd disk create disk1 10g --description '10 GB Disk'
              Create a 10 GB independent disk using the default storage profile.
  
          vcd disk info disk1
              Get details of the disk named 'disk1'.
  
          vcd disk info id:91b3a2e2-fd02-412b-9914-9974d60b2351
              Get details of the disk for a given id.
  
          vcd disk update disk1 --size 20g --description "new description"
              Update an existing independent disk with new size and description.
  
          vcd disk delete disk1
              Delete an existing independent disk named 'disk1'.
      

Options:
  -h, --help  Show this message and exit.

Commands:
  change-owner  change owner of disk
  create        create an independent disk
  delete        delete a disk
  info          show details of an independent disk
  list          list independent disks
  update        update disk

```
