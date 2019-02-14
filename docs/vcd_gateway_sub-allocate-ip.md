```
Usage: vcd gateway sub-allocate-ip [OPTIONS] COMMAND [ARGS]...

  Configures sub-allocate ip pools of gateway in vCloud Director.

      Examples
          vcd gateway sub-allocate-ip add gateway1
              --external-network extNw1
              --ip-range  10.10.10.20-10.10.10.30
              Adds sub allocate ip pools to the edge gateway.

          vcd gateway sub-allocate-ip update gateway1
              -e extNw1
              --old-ip-range 10.10.10.20-10.10.10.30
              --new-ip-range 10.10.10.40-10.10.10.50
              Updates sub allocate ip pools of the edge gateway.
  
          vcd gateway sub-allocate-ip remove gateway1
              -e extNetwork -i 10.10.10.40-10.10.10.50
              Removes the provided IP range
      

Options:
  -h, --help  Show this message and exit.

Commands:
  add     Adds sub allocate ip pools to the edge gateway
  remove  Removes the given IP ranges from existing IP ranges
  update  Edits sub allocate IP pools to the edge gateway

```
