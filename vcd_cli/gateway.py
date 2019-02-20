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
from pyvcloud.vcd.client import ApiVersion
from pyvcloud.vcd.client import EdgeGatewayType
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
                --description test_gateway
                --external-network external-net1
                --external-network external-net2
                --default-gateway external-net1
                --default-gateway-ip 10.10.20.1
                --dns-relay-enabled
                --gateway-config full
                --ha-disabled
                --advanced-enabled
                --distributed-routing-enabled
                --configure-ip-setting external-net1 10.10.20.1/24 10.10.20.3
                --sub-allocate-ip external-net1
                --subnet 10.10.20.1/28 --ip-range 10.10.20.5-10.10.20.10
                --configure-rate-limit external-net1 100 200
                --flip-flop-disabled
                --gateway-type NSXT_BACKED
            Create gateway.
                Parameters:
                    --external-network is a required parameter and can have
                    multiple entries.
                   --gateway-config values can be compact/full/x-large/full4.
                   --gateway-type values can be
                   NSXV_BACKED/NSXT_BACKED/NSXT_IMPORTED.

\b
        vcd gateway delete gateway1
             Delete gateway by providing gateway name.

\b
        vcd gateway enable-distributed-routing gateway1 --disable
            Enable/Disable Distributed routing for gateway.

\b
        vcd gateway modify-form-factor gateway1 full4
            Possible value for gateway configuration are
            compact/full/x-large/full4

\b
        vcd gateway convert-to-advanced gateway1
             Convert gateway to advanced by providing gateway name

\b
        vcd gateway redeploy gateway1
             Redeploys the gateway with given name

\b
        vcd gateway sync-syslog-settings gateway1
             Synchronizes syslog settings of the gateway with given name

\b
        vcd gateway set-syslog-server gateway1 10.11.11.11
             Set syslog server ip address of the gateway

\b
        vcd gateway list-syslog-server gateway1
             List syslog server of the gateway with given name

\b
        vcd gateway list-config-ip-settings gateway1
             Lists the config ip settings of the gateway with given name
\b
        vcd gateway update gateway1 -n gateway2 --description description
                --ha-enabled
            Update name, description and HA of gateway

\b
        vcd gateway configure-ip-settings gateway1 --external-network
                extNetwork --subnet-available 10.20.30.1/24 True 10.20.30.3
             Edits the config ip settings of the gateway with given name
             Parameter:
                 --subnet-available is a required parameter and can have
                 multiple entries
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
    '--description',
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
@click.option(
    '--gateway-type',
    'gateway_type',
    default=EdgeGatewayType.NSXV_BACKED.value,
    metavar='NSXV_BACKED/NSXT_BACKED/NSXT_IMPORTED',
    help='gateway type')
def create_gateway(ctx, name, external_networks_name, description,
                   default_gateway_external_network, default_gw_ip,
                   is_dns_relay, is_ha, is_advanced, is_distributed_routing,
                   configure_ip_settings, sub_allocated_ext_net_name,
                   sub_allocated_subnet, ip_ranges, configure_rate_limits,
                   is_flip_flop, gateway_config, gateway_type):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        api_version = ctx.obj['profiles'].get('api_version')
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

        if float(api_version) <= float(ApiVersion.VERSION_30.value):
            result = vdc.create_gateway_api_version_30(
                name, external_networks_name, gateway_config, description,
                is_configured_default_gw, default_gateway_external_network,
                default_gw_ip, is_dns_relay, is_ha, is_advanced,
                is_distributed_routing, is_ip_settings_configured,
                ext_net_to_participated_subnet_with_ip_settings,
                is_sub_allocate_ip_pools_enabled,
                ext_net_to_subnet_with_ip_range, ext_net_to_rate_limit)
        elif float(api_version) <= float(ApiVersion.VERSION_31.value):
            result = vdc.create_gateway_api_version_31(
                name, external_networks_name, gateway_config, description,
                is_configured_default_gw, default_gateway_external_network,
                default_gw_ip, is_dns_relay, is_ha, is_advanced,
                is_distributed_routing, is_ip_settings_configured,
                ext_net_to_participated_subnet_with_ip_settings,
                is_sub_allocate_ip_pools_enabled,
                ext_net_to_subnet_with_ip_range, ext_net_to_rate_limit,
                is_flip_flop)
        else:
            result = vdc.create_gateway_api_version_32(
                name, external_networks_name, gateway_config, description,
                is_configured_default_gw, default_gateway_external_network,
                default_gw_ip, is_dns_relay, is_ha, is_advanced,
                is_distributed_routing, is_ip_settings_configured,
                ext_net_to_participated_subnet_with_ip_settings,
                is_sub_allocate_ip_pools_enabled,
                ext_net_to_subnet_with_ip_range, ext_net_to_rate_limit,
                is_flip_flop, gateway_type)
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
        gateway_resource = get_gateway(ctx, name)
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
        gateway_resource = get_gateway(ctx, name)
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
        gateway_resource = get_gateway(ctx, name)
        task = gateway_resource.modify_form_factor(gateway_configuration)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


def get_gateway(ctx, name):
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
        gateway_resource = get_gateway(ctx, name)
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
        gateway_resource = get_gateway(ctx, name)
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
        gateway_resource = get_gateway(ctx, name)
        task = gateway_resource.sync_syslog_settings()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.command(
    'list-config-ip-settings', short_help='shows config ip settings.')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
def list_config_ip_settings(ctx, name):
    try:
        gateway_resource = get_gateway(ctx, name)
        ip_allocs = gateway_resource.list_configure_ip_settings()
        stdout(ip_allocs, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.command(
    'set-syslog-server',
    short_help='set syslog server ip of the given gateway')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('ip', metavar='<ip>', required=True)
def set_syslog_server(ctx, name, ip):
    try:
        gateway_resource = get_gateway(ctx, name)
        gateway_resource.set_tenant_syslog_server_ip(ip)
        stdout('Syslog server ip set succesfully', ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.group(
    'configure-external-network',
    short_help='configures external networks of an edge gateway')
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
        gateway_resource = get_gateway(ctx, name)
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
        gateway_resource = get_gateway(ctx, name)
        task = gateway_resource.remove_external_network(external_network_name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.command(
    'update', short_help='update name, description and HA of gateway.')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-n',
    '--new-name',
    'new_name',
    metavar='<str>',
    help='new name of the gateway')
@click.option(
    '--description',
    'desc',
    metavar='<str>',
    help='description of the gateway')
@click.option(
    '--ha-enabled/--ha-disabled',
    'is_enabled',
    default=False,
    metavar='<bool>',
    help='enable/disable HA for gateway.')
def edit_gateway(ctx, name, new_name, desc, is_enabled):
    try:
        gateway_resource = get_gateway(ctx, name)
        task = gateway_resource.edit_gateway(new_name, desc, is_enabled)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.command(
    'configure-ip-settings', short_help='edit config ip settings.')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
@click.option(
    '-e',
    '--external-network',
    'external_networks_name',
    metavar='<external network>',
    required=True,
    help='external networks to which the new gateway can connect.')
@click.option(
    '-s',
    '--subnet-available',
    'subnet_settings',
    nargs=3,
    type=click.Tuple([str, bool, str]),
    multiple=True,
    required=True,
    metavar='<subnet> <enable> <ip>',
    help='set the subnet settings')
def edit_gateway_config_ip_settings(ctx, name, external_networks_name,
                                    subnet_settings):
    try:
        gateway_resource = get_gateway(ctx, name)
        ext_network = dict()
        subnet_participation = dict()
        for setting in subnet_settings:
            subnet_participation_settings = dict()
            subnet_participation_settings['enable'] = setting[1]
            subnet_participation_settings['ip_address'] = setting[2]
            subnet_participation[setting[0]] = subnet_participation_settings

        ext_network[external_networks_name] = subnet_participation
        task = gateway_resource.edit_config_ip_settings(ext_network)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.group(
    'sub-allocate-ip',
    short_help='configures Sub allocate ip pools of gateway')
@click.pass_context
def sub_allocate_ip(ctx):
    """Configures sub-allocate ip pools of gateway in vCloud Director.

\b
    Examples
        vcd gateway sub-allocate-ip add gateway1
            --external-network extNw1
            --ip-range  10.10.10.20-10.10.10.30
            Adds sub allocate ip pools to the edge gateway.

\b
        vcd gateway sub-allocate-ip update gateway1
            -e extNw1
            --old-ip-range 10.10.10.20-10.10.10.30
            --new-ip-range 10.10.10.40-10.10.10.50
            Updates sub allocate ip pools of the edge gateway.
\b
        vcd gateway sub-allocate-ip remove gateway1
            -e extNetwork -i 10.10.10.40-10.10.10.50
            Removes the provided IP range
    """
    pass


@sub_allocate_ip.command(
    'add', short_help='Adds sub allocate ip pools to the edge gateway')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-e',
    '--external-network',
    'external_network_name',
    metavar='<external network>',
    multiple=False,
    required=True,
    help='external network connected to the gateway.')
@click.option(
    '-i',
    '--ip-range',
    'ip_range',
    metavar='<ip range>',
    multiple=True,
    required=True,
    help='ip ranges used for static pool allocation in the network.')
def add_sub_allocated_ip_pools(ctx, name, external_network_name, ip_range):
    try:
        gateway_resource = get_gateway(ctx, name)
        task = gateway_resource.add_sub_allocated_ip_pools(
            external_network_name, list(ip_range))
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@sub_allocate_ip.command(
    'update', short_help='Edits sub allocate IP pools to the edge gateway')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-e',
    '--external-network',
    'external_network_name',
    metavar='<external network>',
    multiple=False,
    required=True,
    help='external network connected to the gateway.')
@click.option(
    '-o',
    '--old-ip-range',
    'old_ip_range',
    metavar='<old-ip-range>',
    multiple=False,
    required=True,
    help='existing IP ranges used for static pool allocation in the network.')
@click.option(
    '-n',
    '--new-ip-range',
    'new_ip_range',
    metavar='<new-ip-range>',
    multiple=False,
    required=True,
    help='new IP range to replace the existing IP range.')
def edit_sub_allocated_ip_pools(ctx, name, external_network_name, old_ip_range,
                                new_ip_range):
    try:
        gateway_resource = get_gateway(ctx, name)
        task = gateway_resource.edit_sub_allocated_ip_pools(
            external_network_name, old_ip_range, new_ip_range)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@sub_allocate_ip.command(
    'remove', short_help='Removes the given IP ranges from existing IP ranges')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-e',
    '--external-network',
    'external_network_name',
    metavar='<external network>',
    multiple=False,
    required=True,
    help='external network connected to the gateway.')
@click.option(
    '-i',
    '--ip-range',
    'ip_range',
    metavar='<old-ip-range>',
    multiple=False,
    required=True,
    help='IP ranges that needs to be removed.')
def remove_sub_allocated_ip_pools(ctx, name, external_network_name, ip_range):
    try:
        gateway_resource = get_gateway(ctx, name)
        task = gateway_resource.remove_sub_allocated_ip_pools(
            external_network_name, [ip_range])
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.group(
    'configure-rate-limits', short_help='configures rate limits of'
    ' gateway')
@click.pass_context
def configure_rate_limits(ctx):
    """Configures rate limit of gateway in vCloud Director.

\b
    Examples
        vcd gateway configure-rate-limits update gateway1
            -r extNw1 101.0 101.0
            updates the rate limit of gateway.
\b
        vcd gateway configure-rate-limits list test_gateway1
\b
        vcd gateway configure-rate-limits disable test_gateway1 -e ExtNw
    """
    pass


@configure_rate_limits.command(
    'update', short_help='updates rate limit of '
    'gateway.')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
@click.option(
    '-r',
    'rate_limit_config',
    nargs=3,
    type=click.Tuple([str, str, str]),
    multiple=True,
    default=None,
    required=True,
    metavar='<external network> <rate limit start> <rate limit end>',
    help='Updates existing rate limits')
def update_configure_rate_limits(ctx, name, rate_limit_config):
    try:
        rate_limit_conf = dict()
        for config in rate_limit_config:
            rate_limit_conf[config[0]] = [config[1], config[2]]
        gateway_resource = get_gateway(ctx, name)
        task = gateway_resource.edit_rate_limits(rate_limit_conf)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@configure_rate_limits.command(
    'list', short_help='list rate limit of gateway.')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
def list_rate_limits(ctx, name):
    try:
        gateway_resource = get_gateway(ctx, name)
        rate_limits = gateway_resource.list_rate_limits()
        stdout(rate_limits, ctx)
    except Exception as e:
        stderr(e, ctx)


@configure_rate_limits.command(
    'disable', short_help=' Disable rate limit of '
    'gateway.')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
@click.option(
    '-e',
    '--external-network',
    'external_network_name',
    metavar='<external network>',
    multiple=True,
    required=True,
    help='external network connected to the gateway.')
def disable_rate_limits(ctx, name, external_network_name):
    try:
        gateway_resource = get_gateway(ctx, name)
        task = gateway_resource.disable_rate_limits(external_network_name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.command(
    'list-syslog-server',
    short_help='list tenant syslog server of the given gateway')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
def list_syslog_server(ctx, name):
    try:
        gateway_resource = get_gateway(ctx, name)
        syslog_server = gateway_resource.list_syslog_server_ip()
        stdout(syslog_server, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.group(
    'configure-default-gateway', short_help='configures the default'
    'gateway')
@click.pass_context
def configure_default_gateway(ctx):
    """Configures the default gateway in vCloud Director.

\b
    Examples
        vcd gateway configure-default-gateway update gateway1
            -e extNw1 --gateway-ip 2.2.3.1 --enable
            updates default gateway.
\b
        vcd gateway configure-default-gateway enable-dns-relay gateway1
            --enable
            enables the dns relay.
\b
        vcd gateway configure-default-gateway list gateway1
            lists the configured default gateway.

    """
    pass


@configure_default_gateway.command(
    'update', short_help='configures the '
    'default gateway')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
@click.option(
    '-e',
    '--external-network',
    'external_network_name',
    metavar='<external network>',
    multiple=False,
    required=True,
    help='external network connected to the gateway.')
@click.option(
    '-i',
    '--gateway-ip',
    'gateway_ip',
    metavar='<ip>',
    multiple=False,
    required=True,
    help='IP of the gateway.')
@click.option(
    '--enable/--disable',
    'is_enable',
    default=None,
    metavar='<bool>',
    help='enables/disables the default gateway')
def configure_default_gateways(ctx, name, external_network_name, gateway_ip,
                               is_enable):
    try:
        gateway_resource = get_gateway(ctx, name)
        task = gateway_resource.configure_default_gateway(
            external_network_name, gateway_ip, is_enable)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@configure_default_gateway.command(
    'enable-dns-relay', short_help='enables/disables the dns relay')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
@click.option(
    '--enable/-disable',
    'is_enable',
    default=None,
    metavar='<bool>',
    help='enables/disables the dns relay')
def enable_dns_relay(ctx, name, is_enable):
    try:
        gateway_resource = get_gateway(ctx, name)
        task = gateway_resource.configure_dns_default_gateway(is_enable)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@configure_default_gateway.command(
    'list', short_help='lists the configure default'
    ' gateway')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
def list_configure_default_gateways(ctx, name):
    try:
        gateway_resource = get_gateway(ctx, name)
        configured_list = gateway_resource.list_configure_default_gateway()
        stdout(configured_list, ctx)
    except Exception as e:
        stderr(e, ctx)


@gateway.group('services', short_help='manage gateway configure services')
@click.pass_context
def services(ctx):
    """Configure services of gateway."""
    pass
