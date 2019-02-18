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
from vcd_cli.vcd import vcd  #NOQA
from vcd_cli.gateway import gateway  # NOQA
from vcd_cli.gateway import get_gateway
from vcd_cli.gateway import services
from vcd_cli.utils import restore_session
from vcd_cli.utils import tuple_to_dict


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
                    --service tcp any any
                    --name new_name
                Edit firewall rule

    \b
            vcd gateway services firewall enable test_gateway1 rule_id
                enabled firewall rule

    \b
            vcd gateway services firewall disable test_gateway1 rule_id
                disabled firewall rule

    \b
            vcd gateway services firewall delete test_gateway1 rule_id
                delete firewall rule

    \b
            vcd gateway services firewall info test_gateway1 rule_id
                Info firewall rule

    \b
            vcd gateway services firewall list-source test_gateway1 rule_id
                List firewall rule's source

    \b
            vcd gateway services firewall list-destination test_gateway1
                    rule_id
                List firewall rule's destination

    \b
            vcd gateway services firewall reorder test_gateway1 rule_id
                    --index new_index
                Reorder the firewall rule position on gateway

    \b
            vcd gateway services firewall delete-source test_gateway1 rule_id
                    source_value
                Delete all source value of firewall rule by providing
                    source_value

    \b
            vcd gateway services firewall delete-destination test_gateway1
                    rule_id destination_value
                Delete all destination value of firewall rule by providing
                    destination_value

    \b
            vcd gateway services firewall list-service test_gateway1 rule_id
                List firewall rule's services

    \b
            vcd gateway services firewall delete-service test_gateway1 rule_id
                    protocol
                Delete all services of firewall rule by providing protocol.
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
@click.option('--type', 'type', metavar='<str>', default='User', help='type')
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
def create_firewall_rule(ctx, gateway_name, name, action, type, enabled,
                         logging_enabled):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        gateway_resource.add_firewall_rule(name, action, type, enabled,
                                           logging_enabled)
        stdout('Firewall rule created successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command('list', short_help='show all firewall rule')
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
    type=click.Choice(['source', 'destination']),
    help='type. possible value will be source/destination')
def list_object_types(ctx, name, type):
    try:
        gateway_resource = get_gateway(ctx, name)
        object_types = gateway_resource.list_firewall_object_types(type)
        stdout(object_types, ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command(
    'list-objects', short_help='list objects for provided '
    'object type')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
@click.option(
    '--type',
    'type',
    metavar='<source/destination>',
    required=True,
    type=click.Choice(['source', 'destination']),
    help='type. possible value will be source/destination')
@click.option(
    '--object-type',
    'object_type',
    required=True,
    metavar='<object type>',
    type=click.Choice([
        'gatewayinterface', 'virtualmachine', 'network', 'ipset',
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
@click.option(
    '--service',
    'services',
    nargs=3,
    type=click.Tuple([str, str, str]),
    multiple=True,
    default=None,
    metavar='<protocol> <source port> <destination port>',
    help='configure services of firewall')
@click.option(
    '--name',
    'new_name',
    default=None,
    metavar='<name>',
    help='new name of the firewall rule')
def update_firewall(ctx, name, rule_id, source_values, destination_values,
                    services, new_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        firewall = FirewallRule(client, gateway_name=name, resource_id=rule_id)
        if source_values:
            firewall.validate_types(source_values, 'source')
        if destination_values:
            firewall.validate_types(destination_values, 'destination')
        application_services = []
        if services:
            for service in services:
                application_services.append(tuple_to_dict([service]))

        firewall.edit(source_values, destination_values, application_services,
                      new_name)

        stdout('Firewall rule updated successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


def get_firewall_rule(ctx, gateway_name, id):
    """Get the firewall rule resource.

    It will restore sessions if expired. It will reads the client and
    creates the FirewallRule resource object.
    """
    restore_session(ctx, vdc_required=True)
    client = ctx.obj['client']
    resource = FirewallRule(client, gateway_name, id)
    return resource


@firewall.command('enable', short_help='enable firewall rule')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('id', metavar='<id>', required=True)
def enabled_firewall_rule(ctx, name, id):
    try:
        firewall_rule_resource = get_firewall_rule(ctx, name, id)
        firewall_rule_resource.enable_disable_firewall_rule(True)
        stdout('Firewall rule enabled successfully', ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command('disable', short_help='disable firewall rule')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('id', metavar='<id>', required=True)
def disabled_firewall_rule(ctx, name, id):
    try:
        firewall_rule_resource = get_firewall_rule(ctx, name, id)
        firewall_rule_resource.enable_disable_firewall_rule(False)
        stdout('Firewall rule disabled successfully', ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command('delete', short_help='delete firewall rule')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('id', metavar='<id>', required=True)
def delete_firewall_rule(ctx, name, id):
    try:
        firewall_rule_resource = get_firewall_rule(ctx, name, id)
        firewall_rule_resource.delete()
        stdout('Firewall rule deleted successfully', ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command('info', short_help='info about firewall rule')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('id', metavar='<id>', required=True)
def info_firewall_rule(ctx, name, id):
    try:
        firewall_rule_resource = get_firewall_rule(ctx, name, id)
        result = firewall_rule_resource.info_firewall_rule()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command('list-source', short_help='list of firewall rule\'s source')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('id', metavar='<id>', required=True)
def list_firewall_rule_source(ctx, name, id):
    try:
        firewall_rule_resource = get_firewall_rule(ctx, name, id)
        result = firewall_rule_resource.list_firewall_rule_source_destination(
            'source')
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command(
    'reorder', short_help='reorder firewall rule position on gateway')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('id', metavar='<id>', required=True)
@click.option(
    '--index',
    'new_index',
    required=True,
    metavar='<int>',
    help='new index of the firewall rule')
def update_firewall_rule_sequence(ctx, name, id, new_index):
    try:
        firewall_rule_resource = get_firewall_rule(ctx, name, id)
        firewall_rule_resource.update_firewall_rule_sequence(new_index)
        stdout('Firewall rule sequence updated successfully', ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command(
    'delete-source',
    short_help='delete firewall rule\'s source value of a firewall rule')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('id', metavar='<id>', required=True)
@click.argument('source_value', metavar='<source_value>', required=True)
def delete_firewall_rule_source(ctx, name, id, source_value):
    try:
        firewall_rule_resource = get_firewall_rule(ctx, name, id)
        firewall_rule_resource.delete_firewall_rule_source_destination(
            source_value, 'source')
        stdout('Firewall rule source deleted successfully', ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command(
    'list-destination', short_help='list of firewall rule\'s destination')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('id', metavar='<id>', required=True)
def list_firewall_rule_destination(ctx, name, id):
    try:
        firewall_rule_resource = get_firewall_rule(ctx, name, id)
        result = firewall_rule_resource.list_firewall_rule_source_destination(
            'destination')
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command(
    'delete-destination',
    short_help='delete firewall rule\'s destination value of a firewall rule')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('id', metavar='<id>', required=True)
@click.argument(
    'destination_value', metavar='<destination_value>', required=True)
def delete_firewall_rule_destination(ctx, name, id, destination_value):
    try:
        firewall_rule_resource = get_firewall_rule(ctx, name, id)
        firewall_rule_resource.delete_firewall_rule_source_destination(
            destination_value, 'destination')
        stdout('Firewall rule destination deleted successfully', ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command('list-service', short_help='list firewall rule\'s services')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('id', metavar='<id>', required=True)
def list_firewall_rule_service(ctx, name, id):
    try:
        firewall_rule_resource = get_firewall_rule(ctx, name, id)
        result = firewall_rule_resource.list_firewall_rule_service()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command(
    'delete-service',
    short_help='delete firewall rule\'s service of a firewall rule')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('id', metavar='<id>', required=True)
@click.argument('protocol', metavar='<protocol>', required=True)
def delete_firewall_rule_service(ctx, name, id, protocol):
    try:
        firewall_rule_resource = get_firewall_rule(ctx, name, id)
        firewall_rule_resource.delete_firewall_rule_service(protocol)
        stdout('Firewall rule\'s service deleted successfully', ctx)
    except Exception as e:
        stderr(e, ctx)
