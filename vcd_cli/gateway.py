# vCloud CLI 0.1
#
# Copyright (c) 2014-2018 VMware, Inc. All Rights Reserved.
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
from pyvcloud.vcd.client import GatewayBackingConfigType
from pyvcloud.vcd.vdc import VDC

from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import vcd
from pyvcloud.vcd.gateway import Gateway
from vcd_cli.utils import tuple_to_dict


@vcd.group(short_help='manage edge gateways')
@click.pass_context
def gateway(ctx):
    """Manage edge gateways in vCloud Director.

\b
    Examples
        vcd gateway list
            Get list of edge gateways in current virtual datacenter.

\b
        vcd gateway info name
            Display gateway details.

\b
        vcd gateway create gateway1
            --external_network extnw1
            --external_network extnw2
            --default-gateway extnw1
            --default-gw-ip 10.10.20.1
            --dns-relay-enabled
            --gateway-config full
            --ha-disabled
            --advanced-enabled
            --distributed-routing-enabled
            --configure-ip-setting extnw1 10.10.20.1/24 10.10.20.3
            --sub-allocate-ip extnw1
            --subnet 10.10.20.1/28 --ip-range 10.10.20.5-10.10.20.10
            --configure-rate-limit extnw1 100 200
            --flips-mode-disabled
            Create gateway.
                Parameter --external-network is a required parameter and
                can have multiple entries.

\b
        vcd gateway delete gateway1
             Delete gateway by providing gateway name.

\b
        vcd gateway enable-distributed-routing  gateway1 --disable
            Enable/Disable Distributed routing for gateway.

\b
        vcd gateway modify-form-factor  gateway1 full4
            Possible value for gatewy configuration are
            compact/full/full4/x-large

\b
        vcd gateway convert-to-advanced gateway1
             Convert gateway to advanced by providing gateway name

\b
        vcd gateway redeploy gateway1
             Redeploys the gateway with given name

\b
        vcd gateway sync-syslog-settings gateway1
             Synchronizes syslog settings of the gateway with given name
    """
    pass


@gateway.command('list', short_help='list edge gateways')
@click.pass_context
def list_gateways(ctx):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        result = vdc.list_edge_gateways()
        for e in result:
            del e['href']
        stdout(result, ctx, show_id=False)
    except Exception as e:
        stderr(e, ctx)


@gateway.command('create', short_help='create edge gateway')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-e',
    '--external-network',
    'external_networks_name',
    metavar='<external network>',
    multiple=True,
    required=True,
    help='list of external networks to which the new gateway can connect.')
@click.option(
    '--desc',
    'description',
    default=None,
    metavar='<description>',
    help='description')
@click.option(
    '--default-gateway',
    'default_gateway_external_network',
    default=None,
    metavar='<external_network>',
    help='name of external network for default gateway configuration')
@click.option(
    '--default-gateway-ip',
    'default_gw_ip',
    default=None,
    metavar='<default gateway IP>',
    help='IP from the external network for the default gateway')
@click.option(
    '--dns-relay-enabled/--dns-relay-disabled',
    'is_dns_relay',
    is_flag=True,
    default=False,
    metavar='<dns-relay>',
    help='DNS relay enabled/disabled')
@click.option(
    '-c',
    '--gateway-config',
    'gateway_config',
    default=GatewayBackingConfigType.COMPACT.value,
    type=click.Choice([
        GatewayBackingConfigType.COMPACT.value,
        GatewayBackingConfigType.FULL.value,
        GatewayBackingConfigType.FULL4.value,
        GatewayBackingConfigType.XLARGE.value
    ]),
    metavar='<gateway_config>',
    help='gateway configuration')
@click.option(
    '--ha-enabled/--ha-disabled',
    'is_ha',
    default=False,
    metavar='<is_ha>',
    help='HA enabled')
@click.option(
    '--advanced-enabled/--advanced-disabled',
    'is_advanced',
    default=False,
    metavar='<is_advanced>',
    help='advanced gateway')
@click.option(
    '--distributed-routing-enabled/--distributed-routing-disabled',
    'is_distributed_routing',
    default=False,
    metavar='<is_distributed>',
    help='enable distributed routing for networks connected to this gateway.')
@click.option(
    '--configure-ip-setting',
    'configure_ip_settings',
    nargs=3,
    type=click.Tuple([str, str, str]),
    multiple=True,
    default=None,
    metavar='<external network> <subnet> <configured IP>',
    help='configuring multiple ip settings')
@click.option(
    '--sub-allocate-ip',
    'sub_allocated_ext_net_name',
    metavar='<external network>',
    default=None,
    help='sub-allocate the IP Pools provided by the externally connected'
    ' interfaces')
@click.option(
    '--subnet',
    'sub_allocated_subnet',
    default=None,
    metavar='<external network subnet>',
    help='subnet for the selected external network for IP sub allocation')
@click.option(
    '--ip-range',
    'ip_ranges',
    metavar='<IP ranges>',
    multiple=True,
    default=None,
    help='IP ranges pertaining to external network\'s IP Pool')
@click.option(
    '--configure-rate-limit',
    'configure_rate_limits',
    metavar='<external network> <incoming rate limit> <outgoing rate limit>',
    multiple=True,
    default=None,
    nargs=3,
    type=click.Tuple([str, float, float]),
    help='specify the inbound and outbound rate limits for each externally'
    ' connected interface.')
@click.option(
    '--flip-flop-enabled/--flip-flop-disabled',
    'is_flip_flop',
    is_flag=True,
    default=False,
    metavar='<is flip flop mode>',
    help='flip flip mode')
def create_gateway(ctx, name, external_networks_name, description,
                   default_gateway_external_network, default_gw_ip,
                   is_dns_relay, is_ha, is_advanced, is_distributed_routing,
                   configure_ip_settings, sub_allocated_ext_net_name,
                   sub_allocated_subnet, ip_ranges, configure_rate_limits,
                   is_flip_flop, gateway_config):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        is_configured_default_gw = False
        if default_gateway_external_network is not None and len(
                default_gateway_external_network) > 0:
            is_configured_default_gw = True
        is_ip_settings_configured = False
        ext_net_to_participated_subnet_with_ip_settings = {}
        if configure_ip_settings is not None and len(configure_ip_settings) \
                > 0:
            is_ip_settings_configured = True
            ext_net_to_participated_subnet_with_ip_settings = tuple_to_dict(
                configure_ip_settings)
        is_sub_allocate_ip_pools_enabled = False
        ext_net_to_subnet_with_ip_range = {}
        if sub_allocated_ext_net_name is not None and len(
                sub_allocated_ext_net_name) > 0 and sub_allocated_subnet is \
                not None and len(sub_allocated_subnet) > 0 and ip_ranges is \
                not None and len(sub_allocated_subnet) > 0:
            is_sub_allocate_ip_pools_enabled = True
            ext_net_to_subnet_with_ip_range = {
                sub_allocated_ext_net_name: {
                    sub_allocated_subnet: list(ip_ranges)
                }
            }
        ext_net_to_rate_limit = {}
        if configure_rate_limits is not None and len(configure_rate_limits) \
                > 0:
            ext_net_to_rate_limit = tuple_to_dict(configure_rate_limits)

        result = vdc.create_gateway(
            name, external_networks_name, gateway_config, description,
            is_configured_default_gw, default_gateway_external_network,
            default_gw_ip, is_dns_relay, is_ha, is_advanced,
            is_distributed_routing, is_ip_settings_configured,
            ext_net_to_participated_subnet_with_ip_settings,
            is_sub_allocate_ip_pools_enabled, ext_net_to_subnet_with_ip_range,
            ext_net_to_rate_limit, is_flip_flop)
        stdout(result.Tasks.Task[0], ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.command('delete', short_help='delete edge gateway')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
def delete_gateway(ctx, name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        task = vdc.delete_gateway(name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.command(
    'convert-to-advanced', short_help='convert to advanced '
    'gateway')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
def convert_to_advanced_gateway(ctx, name):
    try:
        gateway_resource = _get_gateway(ctx, name)
        task = gateway_resource.convert_to_advanced()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.command(
    'enable-distributed-routing',
    short_help='enable '
    'distributed '
    'routing for '
    'gateway')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
@click.option(
    '--enable/--disable',
    'is_enabled',
    default=False,
    metavar='<is_distributed>',
    help='Enable distributed routing for networks connected to this gateway.')
def enable_distributed_routing(ctx, name, is_enabled=False):
    try:
        gateway_resource = _get_gateway(ctx, name)
        task = gateway_resource.enable_distributed_routing(is_enabled)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.command(
    'modify-form-factor', short_help='modify form factor for gateway')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
@click.argument(
    'gateway_configuration',
    metavar='<gateway configuration>',
    required=True,
    type=click.Choice([
        GatewayBackingConfigType.COMPACT.value,
        GatewayBackingConfigType.FULL.value,
        GatewayBackingConfigType.FULL4.value,
        GatewayBackingConfigType.XLARGE.value
    ]))
def modify_form_factor(ctx, name, gateway_configuration):
    try:
        gateway_resource = _get_gateway(ctx, name)
        task = gateway_resource.modify_form_factor(gateway_configuration)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


def _get_gateway(ctx, name):
    """Get the sdk's gateway resource.

    It will restore sessions if expired. It will read the client and vdc
    from context and make get_gateway call to VDC for gateway object.
    """
    restore_session(ctx, vdc_required=True)
    client = ctx.obj['client']
    vdc_href = ctx.obj['profiles'].get('vdc_href')
    vdc = VDC(client, href=vdc_href)
    gateway = vdc.get_gateway(name)
    gateway_resource = Gateway(client, href=gateway.get('href'))
    return gateway_resource


@gateway.command('info', short_help='show gateway information.')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
def info(ctx, name):
    try:
        gateway_resource = _get_gateway(ctx, name)
        ip_allocs = gateway_resource.list_external_network_ip_allocations()
        output = {}
        output['external_network_ip_allocations'] = ip_allocs
        stdout(output, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.command('redeploy', short_help='redeploy the given gateway')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
def redeploy_gateway(ctx, name):
    try:
        gateway_resource = _get_gateway(ctx, name)
        task = gateway_resource.redeploy()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.command(
    'sync-syslog-settings',
    short_help='sync syslog settings of the given gateway')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
def sync_syslog_settings(ctx, name):
    try:
        gateway_resource = _get_gateway(ctx, name)
        task = gateway_resource.sync_syslog_settings()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.group(short_help='configures external networks of an edge gateway')
@click.pass_context
def configure_external_network(ctx):
    """Configures external networks of edge gateways in vCloud Director.

\b
    Examples
        vcd gateway configure-external-network add gateway1
            --external_network extNw1
            --configure-ip-setting 10.10.10.1/28 10.10.10.9
            --configure-ip-setting 10.10.20.1/24 Auto
            Adds an external network to the edge gateway.

\b
        vcd gateway configure-external-network remove gateway1
            -e extNw1
            Removes an external network from the edge gateway.
    """
    pass


@configure_external_network.command(
    'add', short_help='adds an external network to the edge gateway')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-e',
    '--external-network',
    'external_network_name',
    metavar='<external network>',
    multiple=False,
    required=True,
    help='external network to which the gateway can connect.')
@click.option(
    '--configure-ip-setting',
    'configure_ip_settings',
    nargs=2,
    type=click.Tuple([str, str]),
    multiple=True,
    default=None,
    metavar='<subnet> <configured IP>',
    help='configuring multiple IP settings')
def add_external_network(ctx, name, external_network_name,
                         configure_ip_settings):
    try:
        gateway_resource = _get_gateway(ctx, name)
        task = gateway_resource.add_external_network(external_network_name,
                                                     configure_ip_settings)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@configure_external_network.command(
    'remove', short_help='removes an external network from the edge gateway')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-e',
    '--external-network',
    'external_network_name',
    metavar='<external network>',
    multiple=False,
    required=True,
    help='external network that needs to be removed from the gateway.')
def remove_external_network(ctx, name, external_network_name):
    try:
        gateway_resource = _get_gateway(ctx, name)
        task = gateway_resource.remove_external_network(external_network_name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)
