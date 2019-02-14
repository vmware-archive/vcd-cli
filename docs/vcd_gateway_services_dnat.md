```
Usage: vcd gateway services dnat [OPTIONS] COMMAND [ARGS]...

  Manages DNAT Rule of gateway.

      Examples
          vcd gateway services dnat create test_gateway1 --type User
          --original-ip 2.2.3.12 --translated-ip 2.2.3.14 --desc
           "DNAT Created" -v 0 --protocol tcp -op 80 -tp 80
          create new dnat rule

Options:
  -h, --help  Show this message and exit.

Commands:
  create  create new dnat rule

```
