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

from pyvcloud.vcd.firewall_rule import FirewallRule
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.gateway import gateway # NOQA
from vcd_cli.gateway import get_gateway
from vcd_cli.gateway import services
from vcd_cli.utils import restore_session


@services.group('firewall', short_help='manage firewall rules of gateway')
@click.pass_context
def firewall(ctx):
    """Manages firewall Rule of gateway.

    \b
        Examples
            vcd gateway services firewall create test_gateway1 --name rule1
                    --action accept --type User
                    --enabled --logging-enabled

                create new firewall rule

    \b
            vcd gateway services firewall list test_gateway1
                List firewall rules

    \b
            vcd gateway services firewall list-object-types test_gateway1
                    --type source
                List of object types

    \b
            vcd gateway services firewall list-objects test_gateway1
                    --type source --object-type gatewayinterface
                List of object for provided object type

    \b
            vcd gateway services firewall update test_gateway1 rule_id
                    --destination ExtNw:gatewayinterface
                    --destination ExtNw1:gatewayinterface
                    --destination vm1:virtualmachine
                    --source ExtNw:gatewayinterface
                    --source 10.20.3.2:ip
                Edit firewall rule
    """


@firewall.command("create", short_help="create new firewall rule")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.option(
    '--name',
    'name',
    required=True,
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

@firewall.command('list', short_help='displays all firewall rules')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
def rules_list(ctx, name):
    try:
        gateway_resource = get_gateway(ctx, name)
        firewall_rules = gateway_resource.get_firewall_rules_list()
        stdout(firewall_rules, ctx)
    except Exception as e:
        stderr(e, ctx)

@firewall.command('list-object-types', short_help='list object types')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
@click.option(
    '--type',
    'type',
    metavar='<source/destination>',
    required=True,
    type=click.Choice([
        'source',
        'destination'
    ]),
    help='type. possible value will be source/destination')
def list_object_types(ctx, name, type):
    try:
        gateway_resource = get_gateway(ctx, name)
        object_types = gateway_resource.list_firewall_object_types(type)
        stdout(object_types, ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command('list-objects', short_help='list objects for provided '
                                             'object type')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
@click.option(
    '--type',
    'type',
    metavar='<source/destination>',
    required=True,
    type=click.Choice([
        'source',
        'destination'
    ]),
    help='type. possible value will be source/destination')
@click.option(
    '--object-type',
    'object_type',
    required=True,
    metavar='<object type>',
    type=click.Choice([
        'gatewayinterface',
        'virtualmachine',
        'network',
        'ipset',
        'securitygroup'
    ]),
    help='object type')
def list_objects(ctx, name, type, object_type):
    try:
        gateway_resource = get_gateway(ctx, name)
        objects = gateway_resource.list_firewall_objects(type, object_type)
        stdout(objects, ctx)
    except Exception as e:
        stderr(e, ctx)

@firewall.command('update', short_help='update firewall rule')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
@click.argument('rule_id', metavar='<rule id>', required=True)
@click.option(
    '--source',
    'source_values',
    multiple=True,
    default=None,
    metavar='<value:value_type>',
    help='it should be in value:value_type format. for ex: '
         'Extnw:gatewayinterface')
@click.option(
    '--destination',
    'destination_values',
    default=None,
    metavar='<value:value_type>',
    multiple=True,
    help='it should be in value:value_type format. for ex: '
         'Extnw:gatewayinterface')
def update_firewall(ctx, name, rule_id, source_values, destination_values):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        firewall = FirewallRule(client, gateway_name=name, resource_id=rule_id)
        if source_values:
            firewall.validate_types(source_values, 'source')
        if destination_values:
            firewall.validate_types(destination_values, 'destination')
        firewall.edit(source_values, destination_values)

        stdout('Firewall rule updated successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)
