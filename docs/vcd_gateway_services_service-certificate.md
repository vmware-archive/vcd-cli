```
Usage: vcd gateway services service-certificate [OPTIONS] COMMAND [ARGS]...

  Manages service certificates of gateway.

      Examples
          vcd gateway services service-certificate add test_gateway1
                  --certificate-path certificate.pem
                  --private-key-path private_key.pem
                  --pass-phrase 123234dkfs
                  --description description12
              Adds new service certificate.

          vcd gateway services service-certificate list test_gateway1
              Lists service certificates.

          vcd gateway services service-certificate delete test_gateway1 ca-1
              Deletes service certificate.

Options:
  -h, --help  Show this message and exit.

Commands:
  add     adds new service certificate
  delete  Deletes the service certificate
  list    list service certificates

```
