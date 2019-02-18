```
Usage: vcd vapp acl [OPTIONS] COMMAND [ARGS]...

  Work with vapp access control list.

     Description
          Work with vapp access control list in the current Organization.
  
          vcd vapp acl add my-vapp 'user:TestUser1:Change'
              'user:TestUser2:FullControl' 'user:TestUser3'
              Add one or more access setting to the specified vapp.
              access-list is specified in the format
              'user:<username>:<access-level>'
              access-level is one of 'ReadOnly', 'Change', 'FullControl'
              'ReadOnly' by default. eg. 'user:TestUser3'
  
          vcd vapp acl remove my-vapp 'user:TestUser1' 'user:TestUser2'
              Remove one or more acl from the specified vapp. access-list is
              specified in the format 'user:username'
  
          vcd vapp acl share my-vapp --access-level ReadOnly
              Share vapp access to all members of the current organization.
              access-level is one of 'ReadOnly', 'Change', 'FullControl'.
              'ReadOnly' by default.
  
          vcd vapp acl unshare my-vapp
              Unshare  vapp access from  all members of the current
              organization.
  
          vcd vapp acl list my-vapp
              List acl of a vapp.
      

Options:
  -h, --help  Show this message and exit.

Commands:
  add      add access settings to a particular vapp
  list     list vapp access control list
  remove   remove access settings from a particular vapp
  share    share vapp access to all members of the current vorganization
  unshare  unshare vapp access from members of the current organization

```
