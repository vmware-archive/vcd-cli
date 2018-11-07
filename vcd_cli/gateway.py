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
from vcd_cli.utils import tuple_to_dict


@vcd.group(short_help='manage edge gateways')
@click.pass_context
def gateway(ctx):
    """Manage edge gateways in vCloud Director.

\b
    Examples
        vcd gateway list
            Get list of edge gateways in current virtual datacenter.
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
@click.argument('name', metavar='<new gateway name>', required=True)
@click.option(
    '-e',
    '--external-nw',
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
    help='Name of external network for Default gateway configuration')
@click.option(
    '--default-gw-ip',
    'default_gw_ip',
    default=None,
    metavar='<default gateway IP>',
    help='Name of external network for Default gateway configuration')
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
    type=click.Choice([GatewayBackingConfigType.COMPACT.value,
                       GatewayBackingConfigType.FULL.value,
                       GatewayBackingConfigType.FULL4.value,
                       GatewayBackingConfigType.XLARGE.value]),
    metavar='<gateway_config>',
    help='Gateway configuration')
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
    help='Advanced gateway')
@click.option(
    '--distributed-routing-enabled/--distributed-routing-disabled',
    'is_distributed_routing',
    default=False,
    metavar='<is_distributed>',
    help='Enable distributed routing for networks connected to this gateway.')
@click.option(
    '--configure-ip-setting',
    'configure_ip_settings',
    nargs=3,
    type=click.Tuple([str, str, str]),
    multiple=True,
    default=None,
    metavar='<External Network> <subnet> <configured IP>',
    help='Configuring multiple ip settings')
@click.option(
    '--sub-allocate-ip',
    'sub_allocated_ext_net_name',
    metavar='<External Network>',
    default=None,
    help='Sub-allocate the IP Pools provided by the externally connected'
         ' interfaces')
@click.option(
    '--subnet',
    'sub_allocated_subnet',
    default=None,
    metavar='<External Network Subnet>',
    help='Subnet for the selected external network for IP sub allocation')
@click.option(
    '--ip-range',
    'ip_ranges',
    metavar='<IP Ranges>',
    multiple=True,
    default=None,
    help='IP Ranges pertaining to External networks IP Pool')
@click.option(
    '--configure-rate-limit',
    'configure_rate_limits',
    metavar='<External Network> <incoming rate limit> <outgoing rate limit>',
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
                   is_dns_relay,
                   is_ha, is_advanced,
                   is_distributed_routing, configure_ip_settings,
                   sub_allocated_ext_net_name, sub_allocated_subnet, ip_ranges,
                   configure_rate_limits,
                   is_flip_flop, gateway_config):
    """Create a gateway.
    \b
        Note
            Both System Administrators and Organization Administrators can
            create gateway.

    \b
        Examples
            vcd gateway create <gateway-name> -e <External-Network-Name1>
             Create gateway by providing new gateway name, external networks.
             It will create Compact by default without Default gateway
             configuration

    \b
            vcd gateway create <gateway-name> -e <External-Network-Name1> \\
             -e <External-Network-Name1>
            Create gateway by providing multiple external networks

    \b
            vcd gateway create <gateway-name> -e <External-Network-Name1> \\
            --default-gateway <External Network> --default-gw-ip <default
            gateway IP> --dns-relay-enabled/--dns-relay-disabled
            Create gateway by providing Default gateway configuration

    \b
            vcd gateway create <gateway-name> -e <External-Network-Name1> \\
            --c <compact/full/full4/x-large>
            Create gateway by providing gateway config.

    \b
            vcd gateway create <gateway-name> -e <External-Network-Name1> \\
            --ha-enabled/--ha-disabled
            Create gateway with HA enabled

    \b
            vcd gateway create <gateway-name> -e <External-Network-Name1> \\
            --advanced-enabled/--advanced-disabled
            Create advanced gateway

    \b
            vcd gateway create <gateway-name> -e <External-Network-Name1> \\
            --distributed-routing-enabled/--distributed-routing-disabled
            Create gateway with enable distributed routing for networks
            connected to this gateway

    \b
            vcd gateway create <gateway-name> -e <External-Network-Name1> \\
            --distributed-routing-enabled/--distributed-routing-disabled

    \b
            vcd gateway create <gateway-name> -e <External-Network-Name1> \\
            --configure-ip-setting <External Network Name1> <subnet1> \\
            <IP>
            --configure-ip-setting <External Network Name2> <subnet1> \\
            <IP> ...(One or more ip settings)
            For ex: --configure-ip-setting ext_net 10.3.2.1/24 Auto or
                    --configure-ip-setting ext_net 10.3.2.1/24 10.3.2.3
            Create gateway with Configure IP settings

    \b
            vcd gateway create <gateway-name> -e <External-Network-Name1> \\
            --sub-allocate-ip <External Network Name> --subnet
            <subnet> --ip-range <IP Range> \\
            --ip-range <IP Range> ...(one or more IP Ranges)
            For ex: --sub-allocate-ip <External Network Name>
            --subnet 10.3.2.1/20 --ip-range 10.3.2.3-10.3.2.4

    \b
            vcd gateway create <gateway-name> -e <External-Network-Name1> \\
            --configure-rate-limit <External_Network_Name1> \\
             <incoming rate limit> <outgoing rate limit>
            --configure-rate-limit  <External_Network_Name2> \\
             <incoming rate limit> <outgoing rate limit> ... (One or more
             rate limits)
             Create gateway with Rate Limits Configured

    \b
            \b
            vcd gateway create <gateway-name> -e <External-Network-Name1> \\
            --flips-mode-enabled/--flips-mode-disabled
            flips flop mode
        """
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
            ext_net_to_participated_subnet_with_ip_settings = tuple_to_dict \
                (configure_ip_settings)
        is_sub_allocate_ip_pools_enabled = False
        ext_net_to_subnet_with_ip_range = {}
        if sub_allocated_ext_net_name is not None and len(
                sub_allocated_ext_net_name) > 0 and sub_allocated_subnet is \
                not None and len(sub_allocated_subnet) > 0 and ip_ranges is \
                not None and len(sub_allocated_subnet) > 0:
            is_sub_allocate_ip_pools_enabled = True
            ext_net_to_subnet_with_ip_range = {sub_allocated_ext_net_name :
                                                   {sub_allocated_subnet :
                                                        list(ip_ranges)}}
        ext_net_to_rate_limit = {}
        if configure_rate_limits is not None and len(configure_rate_limits) \
                > 0:
            ext_net_to_rate_limit = tuple_to_dict(configure_rate_limits)

        result = vdc.create_gateway(name, external_networks_name,
                    gateway_config,
                    description,
                    is_configured_default_gw,
                    default_gateway_external_network,
                    default_gw_ip,
                    is_dns_relay,
                    is_ha,
                    is_advanced,
                    is_distributed_routing,
                    is_ip_settings_configured,
                    ext_net_to_participated_subnet_with_ip_settings,
                    is_sub_allocate_ip_pools_enabled,
                    ext_net_to_subnet_with_ip_range,
                    ext_net_to_rate_limit,
                    is_flip_flop)
        stdout(result.Tasks.Task[0], ctx)
    except Exception as e:
        stderr(e, ctx)

@gateway.command('delete', short_help='delete edge gateway')
@click.pass_context
@click.argument('name', metavar='<gateway name>', required=True)
def delete_gateway(ctx, name):
    """delete a gateway.
        \b
            Note
                Both System Administrators and Organization Administrators can
                delete gateway.
        \b
            Examples
                vcd gateway delete <gateway-name>
                 Delete gateway by providing gateway name
    """
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        task = vdc.delete_gateway(name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)