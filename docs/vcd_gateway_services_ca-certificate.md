```
Usage: vcd gateway services ca-certificate [OPTIONS] COMMAND [ARGS]...

  Manages CA certificates of gateway.

      Examples
          vcd gateway services ca-certificate add test_gateway1
                  --certificate-path certificate.pem
                  --description CA_certificate
              Adds new CA certificate.

          vcd gateway services ca-certificate list test_gateway1
              Lists CA certificates.

          vcd gateway services ca-certificate delete test_gateway1 ca-1
              Deletes CA certificate.

Options:
  -h, --help  Show this message and exit.

Commands:
  add     adds new CA certificate
  delete  Deletes the CA certificate
  list    list CA certificates

```
