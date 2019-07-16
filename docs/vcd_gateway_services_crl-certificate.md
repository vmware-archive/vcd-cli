```
Usage: vcd gateway services crl-certificate [OPTIONS] COMMAND [ARGS]...

  Manages CRL certificates of gateway.

      Examples
          vcd gateway services crl-certificate add test_gateway1
                  --certificate-path certificate.pem
                  --description CRL_certificate
              Adds new CRL certificate.

          vcd gateway services crl-certificate list test_gateway1
              Lists CRL certificates.

          vcd gateway services crl-certificate delete test_gateway1 ca-1
              Deletes CRL certificate.

Options:
  -h, --help  Show this message and exit.

Commands:
  add     adds new CRL certificate
  delete  Deletes the CRL certificate
  list    list CRL certificates

```
