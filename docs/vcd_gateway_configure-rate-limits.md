```
Usage: vcd gateway configure-rate-limits [OPTIONS] COMMAND [ARGS]...

  Configures rate limit of gateway in vCloud Director.

      Examples
          vcd gateway configure-rate-limits update gateway1
              -r extNw1 101.0 101.0
              updates the rate limit of gateway.
  
          vcd gateway configure-rate-limits list test_gateway1
  
          vcd gateway configure-rate-limits disable test_gateway1 -e ExtNw
      

Options:
  -h, --help  Show this message and exit.

Commands:
  disable   Disable rate limit of gateway.
  list     list rate limit of gateway.
  update   updates rate limit of gateway.

```
