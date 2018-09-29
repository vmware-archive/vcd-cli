```
Usage: vcd vdc acl [OPTIONS] COMMAND [ARGS]...

  Work with vdc access control list.

     Description
          Work with vapp access control list in the current Organization.
          Access should be present to at least 1 user in the org all the time.

          vcd vdc acl add my-vdc 'user:TestUser1:ReadOnly'  \
              'user:TestUser2' 'user:TestUser3'
              Add one or more access setting to the specified vdc.
              access-list is specified in the format
              'user:<username>:<access-level>'
              access-level is only'ReadOnly' for vdc access setting.
              'ReadOnly' by default. eg. 'user:TestUser3'
  
          vcd vdc acl remove my-vdc 'user:TestUser1' 'user:TestUser2'
              Remove one or more access setting from the specified vdc.
              access-list is specified in the format 'user:username'.
  
          vcd vdc acl share my-vdc
              Share vdc access to all members of the current organization at
              access-level 'ReadOnly'.
  
          vcd vdc acl unshare my-vdc
              Unshare  vdc access from  all members of the current
              organization. Should give individual access to at least one user
              before this operation.
  
          vcd vdc acl list my-vdc
              List acl of a vdc.



Options:
  -h, --help  Show this message and exit.

Commands:
  add      add access settings to a particular vdc
  list     list vdc access control list
  remove   remove access settings from a particular vdc
  share    share vdc access to all members of the current organization
  unshare  unshare vdc access from members of the current organization

```
