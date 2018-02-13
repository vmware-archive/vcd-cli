# VMware vCloud Director CLI
#
# Copyright (c) 2017-2018 VMware, Inc. All Rights Reserved.
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
from pyvcloud.vcd.platform import Platform
from pyvcloud.vcd.vdc import VDC

from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import abort_if_false
from vcd_cli.vcd import vcd


@vcd.group(short_help='work with vcd networks')
@click.pass_context
def network(ctx):
    """Work with networks in vCloud Director.

    """
    pass


@network.group(short_help='work with external networks')
@click.pass_context
def external(ctx):
    """Work with external networks.

\b
    Note
        Only System Administrators can work with external networks.
\b
    Examples
        vcd network external list
            List all external networks available in the system
    """
    pass


@network.group(short_help='work with directly connected org vdc networks')
@click.pass_context
def direct(ctx):
    """Work with directly connected org vdc networks.

\b
    Note
        System Administrators have full control on direct org vdc networks.
        Organization Administrators can only list direct org vdc networks.
\b
    Examples
        vcd network direct create direct-net1 \\
                --description 'Directly connected VDC network' \\
                --parent ext-net1 \\
            Create an org vdc network which is directly connected
            to an external network.
\b
        vcd network direct list
            List all directly connected org vdc networks in the selected vdc
\b
        vcd network direct delete direct-net1
            Delete directly connected network 'direct-net1' in the selected vdc
    """
    pass


@network.group(short_help='work with isolated org vdc networks')
@click.pass_context
def isolated(ctx):
    """Work with isolated org vdc networks.

\b
    Note
        Both System Administrators and Organization Administrators can create,
        delete or list isolated org vdc networks.
\b
    Examples
        vcd network isolated create isolated-net1 --gateway-ip 192.168.1.1 \\
                --netmask 255.255.255.0 --description 'Isolated VDC network' \\
                --primary-dns-ip 8.8.8.8 --dns-suffix example.com \\
                --ip-range-start 192.168.1.100 --ip-range-end 192.168.1.199 \\
                --dhcp-enabled --default-lease-time 3600 \\
                --max-lease-time 7200 --dhcp-ip-range-start 192.168.1.100 \\
                --dhcp-ip-range-end 192.168.1.199
            Create an isolated org vdc network with an inbuilt dhcp service.
\b
        vcd network isolated list
            List all isolated org vdc networks in the selected vdc
\b
        vcd network isolated delete isolated-net1
            Delete isolated network 'isoalted-net1' in the selected vdc
    """
    pass


@direct.command(
    'create',
    short_help='create a new directly connected org vdc '
    'network in vcd')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-p',
    '--parent',
    'parent_network_name',
    required=True,
    metavar='<external network name>',
    help='Name of the external network to be connected to')
@click.option(
    '-d',
    '--description',
    'description',
    metavar='<description>',
    default='',
    help='Description of the network to be created')
@click.option(
    '-s/-n',
    '--shared/--not-shared',
    'is_shared',
    is_flag=True,
    default=False,
    help='Share/Don\'t share the network with other VDC(s) in the '
    'organization')
def create_direct_network(ctx, name, parent_network_name, description,
                          is_shared):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        in_use_vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=in_use_vdc_href)

        result = vdc.create_directly_connected_vdc_network(
            network_name=name,
            parent_network_name=parent_network_name,
            description=description,
            is_shared=is_shared)

        stdout(result.Tasks.Task[0], ctx)
    except Exception as e:
        stderr(e, ctx)


@isolated.command(
    'create', short_help='create a new isolated org vdc '
    'network in vcd')
@click.pass_context
@click.argument('name', metavar='<name>')
@click.option(
    '-g',
    '--gateway',
    'gateway_ip',
    required=True,
    metavar='<ip>',
    help='IP address of the gateway of the new network')
@click.option(
    '-n',
    '--netmask',
    'netmask',
    required=True,
    metavar='<netmask>',
    help='network mask for the gateway')
@click.option(
    '-d',
    '--description',
    'description',
    metavar='<description>',
    default='',
    help='Description of the network to be created')
@click.option(
    '--dns1',
    'primary_dns_ip',
    metavar='<ip>',
    help='IP of the primary DNS server')
@click.option(
    '--dns2',
    'secondary_dns_ip',
    metavar='<ip>',
    help='IP of the secondary DNS server')
@click.option(
    '--dns-suffix', 'dns_suffix', metavar='<name>', help='DNS suffix')
@click.option(
    '--ip-range-start',
    'ip_range_start',
    metavar='<ip>',
    help='Start address of the IP ranges used for static pool allocation in '
    'the network')
@click.option(
    '--ip-range-end',
    'ip_range_end',
    metavar='<ip>',
    help='End address of the IP ranges used for static pool allocation in '
    'the network')
@click.option(
    '--dhcp-enabled/--dhcp-disabled',
    'is_dhcp_enabled',
    is_flag=True,
    help='Enable/Disable DHCP service on the new network')
@click.option(
    '--default-lease-time',
    'default_lease_time',
    metavar='<integer>',
    help='Default lease in seconds for DHCP addresses')
@click.option(
    '--max-lease-time',
    'max_lease_time',
    metavar='<integer>',
    help='Max lease in seconds for DHCP addresses')
@click.option(
    '--dhcp-ip-range-start',
    'dhcp_ip_range_start',
    metavar='<ip>',
    help='Start address of the IP range used for DHCP addresses')
@click.option(
    '--dhcp-ip-range-end',
    'dhcp_ip_range_end',
    metavar='<ip>',
    help='End address of the IP range used for DHCP addresses')
@click.option(
    '--shared/--not-shared',
    'is_shared',
    is_flag=True,
    default=False,
    help='Share/Don\'t share the network with other VDC(s) in the '
    'organization')
def create_isolated_network(ctx, name, gateway_ip, netmask, description,
                            primary_dns_ip, secondary_dns_ip, dns_suffix,
                            ip_range_start, ip_range_end, is_dhcp_enabled,
                            default_lease_time, max_lease_time,
                            dhcp_ip_range_start, dhcp_ip_range_end, is_shared):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        in_use_vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=in_use_vdc_href)

        result = vdc.create_isolated_vdc_network(
            network_name=name,
            gateway_ip=gateway_ip,
            netmask=netmask,
            description=description,
            primary_dns_ip=primary_dns_ip,
            secondary_dns_ip=secondary_dns_ip,
            dns_suffix=dns_suffix,
            ip_range_start=ip_range_start,
            ip_range_end=ip_range_end,
            is_dhcp_enabled=is_dhcp_enabled,
            default_lease_time=default_lease_time,
            max_lease_time=max_lease_time,
            dhcp_ip_range_start=dhcp_ip_range_start,
            dhcp_ip_range_end=dhcp_ip_range_end,
            is_shared=is_shared)

        stdout(result.Tasks.Task[0], ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command(
    'list', short_help='list all external networks in the system')
@click.pass_context
def list_external_networks(ctx):
    try:
        restore_session(ctx)
        client = ctx.obj['client']

        platform = Platform(client)
        ext_nets = platform.list_external_networks()

        result = []
        for ext_net in ext_nets:
            result.append({'name': ext_net.get('name')})
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@direct.command(
    'list',
    short_help='list all directly connected org vdc networks in the selected'
    ' vdc')
@click.pass_context
def list_direct_networks(ctx):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        in_use_vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=in_use_vdc_href)

        direct_nets = vdc.list_orgvdc_direct_networks()

        result = []
        for direct_net in direct_nets:
            result.append({'name': direct_net.get('name')})
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@isolated.command(
    'list',
    short_help='list all isolated org vdc networks in the selected vdc')
@click.pass_context
def list_isolated_networks(ctx):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        in_use_vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=in_use_vdc_href)

        isolated_nets = vdc.list_orgvdc_isolated_networks()

        result = []
        for isolated_net in isolated_nets:
            result.append({'name': isolated_net.get('name')})
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@direct.command(
    'delete',
    short_help='delete a directly connected org vdc network in the selected'
    ' vdc')
@click.pass_context
@click.argument('name', metavar='<name>')
@click.option(
    '-f',
    '--force',
    is_flag=True,
    default=False,
    help='pass this option to force delete an org vdc network')
@click.option(
    '-y',
    '--yes',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Are you sure you want to delete the OrgVdc Network?')
def delete_direct_networks(ctx, name, force):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        in_use_vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=in_use_vdc_href)

        delete_task = vdc.delete_direct_orgvdc_network(name=name, force=force)

        stdout(delete_task, ctx)
    except Exception as e:
        stderr(e, ctx)


@isolated.command(
    'delete',
    short_help='delete an isolated org vdc network in the selected vdc')
@click.pass_context
@click.argument('name', metavar='<name>')
@click.option(
    '-f',
    '--force',
    is_flag=True,
    default=False,
    help='pass this option to force delete an org vdc network')
@click.option(
    '-y',
    '--yes',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Are you sure you want to delete the OrgVdc Network?')
def delete_isolated_networks(ctx, name, force):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        in_use_vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=in_use_vdc_href)

        delete_task = vdc.delete_isolated_orgvdc_network(
            name=name, force=force)

        stdout(delete_task, ctx)
    except Exception as e:
        stderr(e, ctx)
