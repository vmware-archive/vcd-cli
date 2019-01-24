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
from vcd_cli.gateway import gateway # NOQA
from vcd_cli.gateway import get_gateway
from vcd_cli.gateway import services


@services.group('firewall', short_help='manage firewall rules of gateway')
@click.pass_context
def firewall(ctx):
    """Manages firewall Rule of gateway.

    \b
        Examples
            vcd gateway services firewall create test_gateway1 --name rule1
            --action accept --type User --enabled --logging-enabled

            create new firewall rule

    """


@firewall.command("create", short_help="create new firewall rule")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.option(
    '--name',
    'name',
    metavar='<firewall rule name>',
    help='firewall rule name')
@click.option(
    '--action',
    'action',
    metavar='<accept/deny>',
    default='accept',
    help='action. possible values accept/deny')
@click.option(
    '--type',
    'type',
    metavar='<str>',
    default='User',
    help='type')
@click.option(
    '--enabled/--disabled',
    'enabled',
    metavar='<bool>',
    is_flag=True,
    default=True,
    help='enable')
@click.option(
    '--logging-enabled/--logging-disabled',
    'logging_enabled',
    metavar='<bool>',
    is_flag=True,
    default=True,
    help='logging enabled')
def create_firewall_rule(ctx, gateway_name, name, action, type,
                         enabled, logging_enabled):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        gateway_resource.add_firewall_rule(name, action, type, enabled,
                                           logging_enabled)
        stdout('Firewall rule created successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)

@firewall.command('list', short_help='displays all firewall rules.')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
def rules_list(ctx, name):
    try:
        gateway_resource = get_gateway(ctx, name)
        firewall_rules = gateway_resource.get_firewall_rules_list()
        stdout(firewall_rules, ctx)
    except Exception as e:
        stderr(e, ctx)
