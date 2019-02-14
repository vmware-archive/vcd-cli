```
Usage: vcd gateway services snat [OPTIONS] COMMAND [ARGS]...

  Manages SNAT Rule of gateway.

      Examples
          vcd gateway services snat create test_gateway1 --type User
          --original-ip 2.2.3.12 --translated-ip 2.2.3.14 --desc
          "SNAT Created" -v 0
          create new snat rule

Options:
  -h, --help  Show this message and exit.

Commands:
  create  create new snat rule

```
