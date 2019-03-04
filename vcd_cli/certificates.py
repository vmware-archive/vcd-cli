# vCloud CLI 0.1
#
# Copyright (c) 2014-2019 VMware, Inc. All Rights Reserved.
#
# This product is licensed to you under the
# Apache License, Version 2.0 (the "License").
# You may not use this product except in compliance with the License.
#
# This product may include a number of subcomponents with
# separate copyright notices and license terms. Your use of the source
# code for the these subcomponents is subject to the terms and
# conditions of the subcomponent's license, as noted in the LICENSE file.
#

import click
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
# Don't change the order of vcd  and gateway
from vcd_cli.vcd import vcd  # NOQA
from vcd_cli.gateway import gateway  # NOQA
from vcd_cli.gateway import get_gateway
from vcd_cli.gateway import services


@services.group('service-certificate', short_help='Manage '
                                                  'certificates of gateway')
@click.pass_context
def certificates(ctx):
    """Manages certificates of gateway.

    \b
        Examples
            vcd gateway services service-certificate add test_gateway1
                    --certificate-file-path certificate.pem
                    --private-key-file-path private_key.pem
                    --pass-phrase 123234dkfs
                    --description description12
                Adds new service certificate.

    """

@certificates.command("add", short_help="adds new service certificate")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.option(
    '--certificate-path',
    'certificate_file_path',
    required=True,
    metavar='<>',
    help='certificate file path')
@click.option(
    '--private-key-path',
    'private_key_file_path',
    required=True,
    metavar='<>',
    help='private key file path')
@click.option(
    '--pass-phrase',
    'pass_phrase',
    metavar='<>',
    help='private key passphrase')
@click.option(
    '--description',
    'desc',
    metavar='<>',
    help='description')
def add_service_certificate(ctx, gateway_name, certificate_file_path,
                            private_key_file_path, pass_phrase, desc):
    try:
        restore_session(ctx, vdc_required=True)
        gateway_resource = get_gateway(ctx, gateway_name)
        gateway_resource.\
            add_service_certificate(service_certificate_file_path=
                                            certificate_file_path,
                                    private_key_file_path=private_key_file_path,
                                    private_key_passphrase=pass_phrase,
                                    description=desc)
        stdout('Service certificate added successfully', ctx)
    except Exception as e:
        stderr(e, ctx)
