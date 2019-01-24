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
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
# Don't change the order of vcd  and gateway
from vcd_cli.vcd import vcd #NOQA
from vcd_cli.gateway import gateway # NOQA
from vcd_cli.gateway import get_gateway
from vcd_cli.gateway import services


@services.group('snat', short_help='manage snat rules of gateway')
@click.pass_context
def snat(ctx):
    """Manages SNAT Rule of gateway.

    \b
        Examples
            vcd gateway services snat create test_gateway1 --type User
            --original-ip 2.2.3.12 --translated-ip 2.2.3.14 --desc
            "SNAT Created" -v 0
            create new snat rule

    """


@snat.command("create", short_help="create new snat rule")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.option(
    '--action',
    'action',
    metavar='<snat/dnat>',
    default='snat',
    help='action')
@click.option(
    '--type',
    'type',
    metavar='<User>',
    default='User',
    help='type')
@click.option(
    '-o',
    '--original-ip',
    'original_address',
    default=None,
    metavar='<ip/ip range>',
    help='Original IP address/Range of SNAT Rule')
@click.option(
    '-t',
    '--translated-ip',
    'translated_address',
    default=None,
    metavar='<ip/ip range>',
    help='Translated IP address/Range of SNAT Rule')
@click.option(
    '--enabled/--disable',
    'enabled',
    is_flag=True,
    default=True,
    help='enable/disable the SNAT rule')
@click.option(
    '--logging-enabled/--logging-disable',
    'logging_enabled',
    is_flag=True,
    default=True,
    help='enable logging')
@click.option(
    '--desc',
    'description',
    default=None,
    metavar='<description>',
    help='description')
@click.option(
    '-v',
    'vnic',
    default=0,
    metavar='<vnic>',
    help='interface of gateway')
def create_snat_rule(ctx, gateway_name, action, type, original_address,
                     translated_address, enabled, logging_enabled,
                     description, vnic):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        gateway_resource.add_nat_rule(
            action=action,
            original_address=original_address,
            translated_address=translated_address,
            description=description,
            type=type,
            logging_enabled=logging_enabled,
            enabled=enabled,
            vnic=vnic)
        stdout('SNAT rule created successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@services.group('dnat', short_help='manage dnat rules of gateway')
@click.pass_context
def dnat(ctx):
    """Manages DNAT Rule of gateway.

    \b
        Examples
            vcd gateway services dnat create test_gateway1 --type User
            --original-ip 2.2.3.12 --translated-ip 2.2.3.14 --desc
             "DNAT Created" -v 0 --protocol tcp -op 80 -tp 80
            create new dnat rule

    """


@dnat.command("create", short_help="create new dnat rule")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.option(
    '--action',
    'action',
    metavar='<snat/dnat>',
    default='dnat',
    help='action')
@click.option(
    '--type',
    'type',
    metavar='<User>',
    default='User',
    help='type')
@click.option(
    '-o',
    '--original-ip',
    'original_address',
    default=None,
    metavar='<ip/ip range>',
    help='Original IP address/Range of DNAT Rule')
@click.option(
    '-t',
    '--translated-ip',
    'translated_address',
    default=None,
    metavar='<ip/ip range>',
    help='Translated IP address/Range of DNAT Rule')
@click.option(
    '--enabled/--disable',
    'enabled',
    is_flag=True,
    default=True,
    help='enable/disable the DNAT rule')
@click.option(
    '--logging-enabled/--logging-disable',
    'logging_enabled',
    is_flag=True,
    default=True,
    help='enable logging')
@click.option(
    '--desc',
    'description',
    default=None,
    metavar='<description>',
    help='description')
@click.option(
    '-v',
    'vnic',
    default=0,
    metavar='<vnic>',
    help='interface of gateway')
@click.option(
    '-p',
    '--protocol',
    'protocol',
    default=None,
    metavar='<tcp/udp/icmp>',
    help='interface of gateway')
@click.option(
    '-op',
    '--original-Port',
    'original_Port',
    default=None,
    metavar='<vnic>',
    help='original port')
@click.option(
    '-tp',
    '--translated-Port',
    'translated_Port',
    default=None,
    metavar='<vnic>',
    help='translated port')
def create_dnat_rule(ctx, gateway_name, action, type, original_address,
                     translated_address, enabled, logging_enabled,
                     description, vnic, protocol, original_Port,
                     translated_Port):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        gateway_resource.add_nat_rule(
            action=action,
            original_address=original_address,
            translated_address=translated_address,
            description=description,
            type=type,
            logging_enabled=logging_enabled,
            enabled=enabled,
            vnic=vnic,
            protocol=protocol,
            original_port=original_Port,
            translated_port=translated_Port)

        stdout('DNAT rule created successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@services.group('nat', short_help='manage snat/dnat rules of gateway')
@click.pass_context
def nat(ctx):
    """Manages SNAT/DNAT Rule of gateway.

    \b
        Examples
            vcd gateway services nat list test_gateway1

    """


@nat.command('list', short_help='List all nat rules on a gateway')
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
def list_nat_rules(ctx, gateway_name):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        nat_list = gateway_resource.list_nat_rules()
        stdout(nat_list, ctx)
    except Exception as e:
        stderr(e, ctx)
