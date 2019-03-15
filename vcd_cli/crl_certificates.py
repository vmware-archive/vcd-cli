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
from pyvcloud.vcd.crl import Crl
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
# Don't change the order of vcd  and gateway
from vcd_cli.vcd import vcd  # NOQA
from vcd_cli.gateway import gateway  # NOQA
from vcd_cli.gateway import get_gateway
from vcd_cli.gateway import services


@services.group('crl-certificate', short_help='Manage '
                                             'CRL certificates of gateway')
@click.pass_context
def crl_certificates(ctx):
    """Manages CRL certificates of gateway.

    \b
        Examples
            vcd gateway services crl-certificate add test_gateway1
                    --certificate-path certificate.pem
                    --description CRL_certificate
                Adds new CRL certificate.

    \b
            vcd gateway services crl-certificate list test_gateway1
                Lists CRL certificates.

    \b
            vcd gateway services crl-certificate delete test_gateway1 ca-1
                Deletes CRL certificate.
    """


@crl_certificates.command("add", short_help="adds new CRL certificate")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.option(
    '--certificate-path',
    'certificate_file_path',
    required=True,
    metavar='<>',
    help='certificate file path')
@click.option(
    '--description',
    'desc',
    metavar='<>',
    help='description')
def add_crl_certificate(ctx, gateway_name, certificate_file_path, desc):
    try:
        restore_session(ctx, vdc_required=True)
        gateway_resource = get_gateway(ctx, gateway_name)
        gateway_resource. \
            add_crl_certificate(crl_certificate_file_path=
                                certificate_file_path,
                                description=desc)
        stdout('CRL certificate added successfully', ctx)
    except Exception as e:
        stderr(e, ctx)


@crl_certificates.command("list",
                          short_help="list CRL certificates")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
def list_crl_certificate(ctx, gateway_name):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        result = gateway_resource.list_crl_certificates()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@crl_certificates.command("delete", short_help="Deletes the CRL certificate")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.argument('id', metavar='certificate-id', required=True)
def delete_crl_certificate(ctx, gateway_name, id):
    try:
        certificate_obj = get_crl_certificate(ctx, gateway_name, id)
        certificate_obj.delete_certificate()
        stdout('CRL certificate deleted successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


def get_crl_certificate(ctx, gateway_name, id):
    """Get the sdk's certificate object.

    It will restore sessions if expired. It will read the client.
    """
    restore_session(ctx, vdc_required=True)
    client = ctx.obj['client']
    certificate = Crl(client=client,
                      gateway_name=gateway_name,
                      resource_id=id)
    return certificate
