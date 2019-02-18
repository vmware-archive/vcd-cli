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
from vcd_cli.vcd import vcd #NOQA
from vcd_cli.gateway import gateway # NOQA
from vcd_cli.gateway import get_gateway
from vcd_cli.gateway import services

from pyvcloud.vcd.nat_rule import NatRule


@services.group('nat', short_help='manage snat/dnat rules of gateway')
@click.pass_context
def nat(ctx):
    """Manages SNAT/DNAT Rule of gateway.

\b
        Examples
            vcd gateway services nat create-snat test_gateway1
                    --original-ip 2.2.3.12 --translated-ip 2.2.3.14 --desc
                    "SNAT Created" --vnic 0 --enabled --logging-enabled
                Create new SNAT rule

\b
             vcd gateway services nat update-snat test_gateway1 196609
                     --original-ip 2.2.3.12 --translated-ip 2.2.3.14 --desc
                     "SNAT Updated" --vnic 0
                 Update SNAT rule

\b
            vcd gateway services nat create-dnat test_gateway1
                    --original-ip 2.2.3.12 --translated-ip 2.2.3.14 --desc
                    "DNAT Created" --vnic 0 --protocol tcp -op 80 -tp 80
                    --enabled --logging-enabled
                Create new DNAT rule

\b
            vcd gateway services nat update-dnat test_gateway1 196609
                     --original-ip 2.2.3.12 --translated-ip 2.2.3.14 --desc
                     "DNAT Updated" --vnic 0 --protocol udp -op 80 -tp 80
                Update DNAT rule

\b
            vcd gateway services nat list test_gateway1
                List all NAT rules

\b
           vcd gateway services nat delete test_gateway1 196609
               Deletes the NAT rule

\b
           vcd gateway services nat info test_gateway1 196609
               Get details of NAT rule

\b
           vcd gateway services nat reorder test_gateway1 196609 --index 2
               Reorder the NAT rule position on gateway
    """


@nat.command('list', short_help='List all NAT rules on a gateway')
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
def list(ctx, gateway_name):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        nat_list = gateway_resource.list_nat_rules()
        stdout(nat_list, ctx)
    except Exception as e:
        stderr(e, ctx)


def get_nat_rule(ctx, gateway_name, rule_id):
    """Get the Nat Rule resource.

    It will restore sessions if expired. It will reads the client and
    creates the Nat Rule resource object.
    """
    restore_session(ctx, vdc_required=True)
    client = ctx.obj['client']
    resource = NatRule(client, gateway_name, rule_id)
    return resource


@nat.command("delete", short_help="Deletes the NAT rule")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.argument('rule_id', metavar='<nat rule id>', required=True)
def delete(ctx, gateway_name, rule_id):
    try:
        resource = get_nat_rule(ctx, gateway_name, rule_id)
        resource.delete_nat_rule()
        stdout('Nat Rule deleted successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@nat.command("info", short_help="show NAT rule details")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.argument('rule_id', metavar='<nat rule id>', required=True)
def info(ctx, gateway_name, rule_id):
    try:
        resource = get_nat_rule(ctx, gateway_name, rule_id)
        result = resource.get_nat_rule_info()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@nat.command("create-snat", short_help="create new SNAT rule")
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
    metavar='<bool>',
    help='enable/disable the SNAT rule')
@click.option(
    '--logging-enabled/--logging-disable',
    'logging_enabled',
    is_flag=True,
    default=True,
    metavar='<bool>',
    help='enable logging')
@click.option(
    '--desc',
    'description',
    default=None,
    metavar='<description>',
    help='description')
@click.option(
    '--vnic',
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


@nat.command("update-snat", short_help="update SNAT rule")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.argument('rule_id', metavar='<nat rule id>', required=True)
@click.option(
    '-o',
    '--original-ip',
    'original_address',
    default=None,
    metavar='<ip/ip range>',
    help='original IP address/Range of SNAT Rule')
@click.option(
    '-t',
    '--translated-ip',
    'translated_address',
    default=None,
    metavar='<ip/ip range>',
    help='translated IP address/Range of SNAT Rule')
@click.option(
    '--enabled/--disable',
    'enabled',
    default=None,
    metavar='<bool>',
    help='enable/disable the SNAT rule')
@click.option(
    '--logging-enabled/--logging-disable',
    'logging_enabled',
    default=None,
    metavar='<bool>',
    help='enable logging')
@click.option(
    '--desc',
    'description',
    default=None,
    metavar='<str>',
    help='description of SNAT Rule')
@click.option(
    '--vnic',
    'vnic',
    default=None,
    metavar='<vnic>',
    help='interface of gateway')
def update_snat_rule(ctx, gateway_name, rule_id, original_address,
                     translated_address, enabled, logging_enabled,
                     description, vnic):
    try:
        resource = get_nat_rule(ctx, gateway_name, rule_id)
        resource.update_nat_rule(
            original_address=original_address,
            translated_address=translated_address,
            description=description,
            logging_enabled=logging_enabled,
            enabled=enabled,
            vnic=vnic)
        stdout('SNAT rule updated successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@nat.command("create-dnat", short_help="create new DNAT rule")
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
    metavar='<bool>',
    help='enable/disable the DNAT rule')
@click.option(
    '--logging-enabled/--logging-disable',
    'logging_enabled',
    is_flag=True,
    default=True,
    metavar='<bool>',
    help='enable logging')
@click.option(
    '--desc',
    'description',
    default=None,
    metavar='<description>',
    help='description')
@click.option(
    '--vnic',
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


@nat.command("update-dnat", short_help="update DNAT rule")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.argument('rule_id', metavar='<nat rule id>', required=True)
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
    default=None,
    help='enable/disable the DNAT rule')
@click.option(
    '--logging-enabled/--logging-disable',
    'logging_enabled',
    default=None,
    help='enable logging')
@click.option(
    '--desc',
    'description',
    default=None,
    metavar='<description>',
    help='description')
@click.option(
    '--vnic',
    'vnic',
    default=None,
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
def update_dnat_rule(ctx, gateway_name, rule_id, original_address,
                     translated_address, enabled, logging_enabled,
                     description, vnic, protocol, original_Port,
                     translated_Port):
    try:
        resource = get_nat_rule(ctx, gateway_name, rule_id)
        resource.update_nat_rule(
            original_address=original_address,
            translated_address=translated_address,
            description=description,
            logging_enabled=logging_enabled,
            enabled=enabled,
            vnic=vnic,
            protocol=protocol,
            original_port=original_Port,
            translated_port=translated_Port)
        stdout('DNAT rule updated successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@nat.command('reorder', short_help='reorder NAT rule position on gateway')
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.argument('rule_id', metavar='<nat rule id>', required=True)
@click.option(
    '--index',
    'index',
    metavar='<int>',
    type=int,
    help='index where NAT rule will be moved/shifted')
def reorder_nat_rule(ctx, gateway_name, rule_id, index):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        gateway_resource.reorder_nat_rule(rule_id, position=index)
        stdout('NAT rule reordered successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)
