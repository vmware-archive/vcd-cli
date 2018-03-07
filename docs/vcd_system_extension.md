```
Usage: vcd system extension [OPTIONS] COMMAND [ARGS]...

  Manage Extension Services in vCloud Director.

      Examples
          vcd system extension list
              List available extension services.
  
          vcd system extension create cse cse-ns cse vcdext \
              '/api/cse, /api/cse/.*, /api/cse/.*/.*'
              Register a new extension service named 'cse' in namespace 'cse-ns'.
  
          vcd system extension delete cse cse-ns
              Unregister an extension service named 'cse' in namespace 'cse-ns'.
  
          vcd system extension info cse cse-ns
              Get details of an extension service named 'cse'
              in namespace 'cse-ns'.
      

Options:
  -h, --help  Show this message and exit.

Commands:
  create  register new extension
  delete  unregister extension
  info    show extension details
  list    list extensions

```
