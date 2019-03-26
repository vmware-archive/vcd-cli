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
from pyvcloud.vcd.external_network import ExternalNetwork
from pyvcloud.vcd.platform import Platform
from pyvcloud.vcd.utils import netmask_to_cidr_prefix_len
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.client import NSMAP

from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import abort_if_false
from vcd_cli.vcd import vcd


@vcd.group(short_help='work with vcd networks')
@click.pass_context
def network(ctx):
    """Work with networks in vCloud Director.

\b
    Examples
        vcd network list
            List all org vdc networks available in a org.
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

\b
        vcd network external create external-net1
                --vc vc1
                --port-group pg1
                --gateway 192.168.1.1
                --netmask 255.255.255.0
                --ip-range 192.168.1.2-192.168.1.49
                --ip-range 192.168.1.100-192.168.1.149
                --description 'External network'
                --dns1 8.8.8.8
                --dns2 8.8.8.9
                --dns-suffix example.com
            Create an external network.
                Parameter --ip-range can have multiple entries.

\b
        vcd network external delete external-net1
            Delete an external network.

\b
        vcd network external update external-net1
                --name 'new-external-net1'
                --description 'New external network'
            Update name and description of an external network.

\b
        vcd network external add-subnet external-net1
                --gateway 192.168.1.1
                --netmask 255.255.255.0
                --ip-range 192.168.1.2-192.168.1.49
                --dns1 8.8.8.8
                --dns2 8.8.8.9
                --dns-suffix example.com
            Add subnet to external network.
                Parameter ip-range can have multiple entries.

\b
        vcd network external enable-subnet external-net1
                --gateway 192.168.1.1
                --enable/--disable
            Enable/Disable subnet of an external network.

\b
        vcd network external add-ip-range external-net1
                --gateway 192.168.1.1
                --ip-range 192.168.1.2-192.168.1.20
            Add an IP range to an external network.

\b
        vcd network external update-ip-range external-net1
                --gateway 192.168.1.1
                --ip-range 192.168.1.2-192.168.1.20
                --new-ip-range 192.168.1.25-192.168.1.50
            Update an IP range in an external network.

\b
        vcd network external delete-ip-range external-net1
                --gateway 192.168.1.1
                --ip-range 192.168.1.2-192.168.1.20
            Delete an IP range from an external network.

\b
        vcd network external attach-port-group external-net1
                --vc vc1
                --port-group pg1
            Attach a port group to an external network.

\b
        vcd network external detach-port-group external-net1
                --vc vc1
                --port-group pg1
            Detach a port group from an external network.

\b
        vcd network external list-pvdc external-net1
                --filter name==pvdc*
            List available provider vdcs

\b
        vcd network external list-gateway external-net1
                --filter name==gateway*
            List associated gateways

\b
        vcd network external list-allocated-ip external-net1
                --filter name==gateway*
            List allocated ip

\b
        vcd network external list-sub-allocated-ip external-net1
                --filter name==gateway*
            List sub allocated ip

\b
        vcd network external list-direct-org-vdc-network external-net1
                --filter name==org-vdc-net*
            List associated direct org vDC networks

\b
        vcd network external list-vsphere-network external-net1
                --filter name==portgroup*
            List associated vSphere Networks

\b
        vcd network external info external-net1
            Show external network details.
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
        vcd network direct create direct-net1
                --description 'Directly connected VDC network'
                --parent ext-net1
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
        vcd network isolated create isolated-net1 --gateway 192.168.1.1
                --netmask 255.255.255.0 --description 'Isolated VDC network'
                --dns1 8.8.8.8 --dns2 8.8.8.9 --dns-suffix example.com
                --ip-range-start 192.168.1.100 --ip-range-end 192.168.1.199
                --dhcp-enabled --default-lease-time 3600
                --max-lease-time 7200 --dhcp-ip-range-start 192.168.1.100
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
        prefix_len = netmask_to_cidr_prefix_len(gateway_ip, netmask)
        network_cidr = gateway_ip + '/' + str(prefix_len)

        result = vdc.create_isolated_vdc_network(
            network_name=name,
            network_cidr=network_cidr,
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


@external.command('create', short_help='create a new external network')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-v',
    '--vc',
    'vc_name',
    required=True,
    metavar='<vc-name>',
    help='name of the vCenter')
@click.option(
    '-p',
    '--port-group',
    'port_group',
    required=True,
    multiple=True,
    metavar='<name>',
    help='portgroup to create external network')
@click.option(
    '-g',
    '--gateway',
    'gateway_ip',
    required=True,
    metavar='<ip>',
    help='gateway of the subnet')
@click.option(
    '-n',
    '--netmask',
    'netmask',
    required=True,
    metavar='<netmask>',
    help='network mask of the subnet')
@click.option(
    '-i',
    '--ip-range',
    'ip_range',
    required=True,
    multiple=True,
    metavar='<ip>',
    help='IP range in StartAddress-EndAddress format')
@click.option(
    '-d',
    '--description',
    'description',
    metavar='<description>',
    default='',
    help='Description of the external network to be created')
@click.option(
    '--dns1',
    'primary_dns_ip',
    metavar='<ip>',
    help='IP of the primary DNS server of the subnet')
@click.option(
    '--dns2',
    'secondary_dns_ip',
    metavar='<ip>',
    help='IP of the secondary DNS server of the subnet')
@click.option(
    '--dns-suffix', 'dns_suffix', metavar='<name>', help='DNS suffix')
def create_external_network(ctx, name, vc_name, port_group, gateway_ip,
                            netmask, ip_range, description, primary_dns_ip,
                            secondary_dns_ip, dns_suffix):
    try:
        platform = _get_platform(ctx)
        ext_net = platform.create_external_network(
            name=name,
            vim_server_name=vc_name,
            port_group_names=port_group,
            gateway_ip=gateway_ip,
            netmask=netmask,
            ip_ranges=ip_range,
            description=description,
            primary_dns_ip=primary_dns_ip,
            secondary_dns_ip=secondary_dns_ip,
            dns_suffix=dns_suffix)

        stdout(ext_net['{' + NSMAP['vcloud'] + '}Tasks'].Task[0], ctx)
        stdout('External network created successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command(
    'list', short_help='list all external networks in the system')
@click.pass_context
def list_external_networks(ctx):
    try:
        platform = _get_platform(ctx)
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
        if type(e).__name__ == 'AccessForbiddenException':
            message = "Access denied.\nPlease try following command"
            message += '\nvcd network list'
            stdout(message, ctx)
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
        if type(e).__name__ == 'AccessForbiddenException':
            message = "Access denied.\nPlease try following command"
            message += '\nvcd network list'
            stdout(message, ctx)
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


@external.command('delete', short_help='delete an external network')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
def delete_external_network(ctx, name):
    try:
        platform = _get_platform(ctx)
        task = platform.delete_external_network(name=name)

        stdout(task, ctx)
        stdout('External network deleted successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command(
    'update', short_help='update name and description of an external network')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-n',
    '--name',
    'new_name',
    metavar='<name>',
    required=False,
    help='New name of the external network')
@click.option(
    '-d',
    '--description',
    'new_description',
    metavar='<description>',
    required=False,
    help='New description of the external network')
def update_external_network(ctx, name, new_name, new_description):
    try:
        platform = _get_platform(ctx)
        ext_net = platform.update_external_network(
            name=name, new_name=new_name, new_description=new_description)

        stdout(ext_net['{' + NSMAP['vcloud'] + '}Tasks'].Task[0], ctx)
        stdout('External network updated successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command('add-subnet', short_help='add subnet to an external network')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-g',
    '--gateway',
    'gateway_ip',
    required=True,
    metavar='<ip>',
    help='gateway ip of the subnet')
@click.option(
    '-n',
    '--netmask',
    'netmask',
    required=True,
    metavar='<netmask>',
    help='network mask of the subnet')
@click.option(
    '-i',
    '--ip-range',
    'ip_range',
    required=True,
    multiple=True,
    metavar='<ip>',
    help='ip range in StartAddress-EndAddress format')
@click.option(
    '--dns1',
    'primary_dns_ip',
    metavar='<ip>',
    help='ip of the primary dns server of the subnet')
@click.option(
    '--dns2',
    'secondary_dns_ip',
    metavar='<ip>',
    help='ip of the secondary dns server of the subnet')
@click.option(
    '--dns-suffix', 'dns_suffix', metavar='<name>', help='dns suffix')
def add_subnet_external_network(ctx, name, gateway_ip, netmask, ip_range,
                                primary_dns_ip, secondary_dns_ip, dns_suffix):
    try:
        extnet_obj = _get_ext_net_obj(ctx, name)

        ext_net = extnet_obj.add_subnet(
            name=name,
            gateway_ip=gateway_ip,
            netmask=netmask,
            ip_ranges=ip_range,
            primary_dns_ip=primary_dns_ip,
            secondary_dns_ip=secondary_dns_ip,
            dns_suffix=dns_suffix)

        stdout(ext_net['{' + NSMAP['vcloud'] + '}Tasks'].Task[0], ctx)
        stdout('subnet is added successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command(
    'enable-subnet', short_help='enable subnet of an external network')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-g',
    '--gateway',
    'gateway_ip',
    required=True,
    metavar='<ip>',
    help='gateway ip of the subnet')
@click.option(
    '--enable/--disable',
    'is_enabled',
    default=None,
    help='enable/disable the subnet')
def enable_subnet_external_network(ctx, name, gateway_ip, is_enabled):
    try:
        extnet_obj = _get_ext_net_obj(ctx, name)

        ext_net = extnet_obj.enable_subnet(
            gateway_ip=gateway_ip, is_enabled=is_enabled)

        stdout(ext_net['{' + NSMAP['vcloud'] + '}Tasks'].Task[0], ctx)
        if is_enabled:
            stdout('Subnet is enabled successfully.', ctx)
        else:
            stdout('Subnet is disabled successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


def _get_ext_net_obj(ctx, name):
    """Returns ExternalNetwork object."""
    platform = _get_platform(ctx)
    client = ctx.obj['client']
    return ExternalNetwork(
        client, resource=platform.get_external_network(name))


def _get_platform(ctx):
    """Returns Platform object"""
    restore_session(ctx)
    client = ctx.obj['client']
    return Platform(client)


@external.command(
    'add-ip-range',
    short_help='add an IP range to a subnet in an external network')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-g',
    '--gateway',
    'gateway_ip',
    required=True,
    metavar='<ip>',
    help='gateway ip of the subnet')
@click.option(
    '-i',
    '--ip-range',
    'ip_range',
    required=True,
    multiple=True,
    metavar='<ip>',
    help='ip range in StartAddress-EndAddress format')
def add_ip_range_external_network(ctx, name, gateway_ip, ip_range):
    try:
        extnet_obj = _get_ext_net_obj(ctx, name)

        ext_net = extnet_obj.add_ip_range(
            gateway_ip=gateway_ip, ip_ranges=ip_range)
        stdout(ext_net['{' + NSMAP['vcloud'] + '}Tasks'].Task[0], ctx)
        stdout('Ip Range added to a subnet successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command(
    'update-ip-range',
    short_help='update an IP range of a subnet in an external network')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-g',
    '--gateway',
    'gateway_ip',
    required=True,
    metavar='<ip>',
    help='gateway ip of the subnet')
@click.option(
    '-i',
    '--ip-range',
    'ip_range',
    required=True,
    metavar='<ip>',
    help='ip range in StartAddress-EndAddress format')
@click.option(
    '-n',
    '--new-ip-range',
    'new_ip_range',
    required=True,
    metavar='<ip>',
    help='ip range in StartAddress-EndAddress format')
def modify_ip_range_external_network(ctx, name, gateway_ip, ip_range,
                                     new_ip_range):
    try:
        extnet_obj = _get_ext_net_obj(ctx, name)

        ext_net = extnet_obj.modify_ip_range(
            gateway_ip=gateway_ip,
            old_ip_range=ip_range,
            new_ip_range=new_ip_range)
        stdout(ext_net['{' + NSMAP['vcloud'] + '}Tasks'].Task[0], ctx)
        stdout('IP Range of a subnet modified successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command(
    'delete-ip-range',
    short_help='delete an IP range of a subnet in an external network')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-g',
    '--gateway',
    'gateway_ip',
    required=True,
    metavar='<ip>',
    help='gateway ip of the subnet')
@click.option(
    '-i',
    '--ip-range',
    'ip_range',
    required=True,
    multiple=True,
    metavar='<ip>',
    help='ip range in StartAddress-EndAddress format')
def delete_ip_range_external_network(ctx, name, gateway_ip, ip_range):
    try:
        extnet_obj = _get_ext_net_obj(ctx, name)

        ext_net = extnet_obj.delete_ip_range(
            gateway_ip=gateway_ip, ip_ranges=ip_range)
        stdout(ext_net['{' + NSMAP['vcloud'] + '}Tasks'].Task[0], ctx)
        stdout('IP Range of a subnet removed successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command(
    'detach-port-group',
    short_help='detach port group from an external network')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-v', '--vc', 'vc_name', required=True, help='name of the vCenter')
@click.option(
    '-p', '--port-group', 'pg_name', required=True, help='Port group name')
def detach_port_group_external_network(ctx, name, vc_name, pg_name):
    try:
        extnet_obj = _get_ext_net_obj(ctx, name)

        ext_net = extnet_obj.detach_port_group(
            vim_server_name=vc_name, port_group_name=pg_name)
        stdout(ext_net['{' + NSMAP['vcloud'] + '}Tasks'].Task[0], ctx)
        stdout('Port group detached successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command(
    'attach-port-group',
    short_help='attach a port group to an external network')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-v', '--vc', 'vc_name', required=True, help='name of the vCenter')
@click.option(
    '-p',
    '--port-group',
    'pg_name',
    required=True,
    help='name of the port group present in vCenter')
def attach_port_group_external_network(ctx, name, vc_name, pg_name):
    try:
        extnet_obj = _get_ext_net_obj(ctx, name)

        ext_net = extnet_obj.attach_port_group(
            vim_server_name=vc_name, port_group_name=pg_name)
        stdout(ext_net['{' + NSMAP['vcloud'] + '}Tasks'].Task[0], ctx)
        stdout('Port group attached successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command('list-pvdc', short_help='list associated pvdcs')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '--filter',
    'filter',
    default=None,
    metavar='<name==pvdc*>',
    help='filter for provider vdc')
def list_available_pvdcs(ctx, name, filter):
    try:
        platform = _get_platform(ctx)
        client = ctx.obj['client']
        ext_net = platform.get_external_network(name)
        ext_net_obj = ExternalNetwork(client, resource=ext_net)
        assoc_prov_vdc_name = ext_net_obj.list_provider_vdc(filter)
        result = []
        result.append({'Provider Vdcs': assoc_prov_vdc_name})
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command('list-gateway', short_help='list associated gateways')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '--filter',
    'filter',
    default=None,
    metavar='<name==gateway*>',
    help='filter for gateway')
def list_available_gateways(ctx, name, filter):
    try:
        platform = _get_platform(ctx)
        client = ctx.obj['client']
        ext_net = platform.get_external_network(name)
        ext_net_obj = ExternalNetwork(client, resource=ext_net)
        gateway_names = ext_net_obj.list_extnw_gateways(filter)
        result = []
        for gatway_name in gateway_names:
            result.append({'Edge Gateway': gatway_name})
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command('list-allocated-ip', short_help='list allocated IP')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '--filter',
    'filter',
    default=None,
    metavar='<name==gateway*>',
    help='filter for gateway')
def list_allocated_ip(ctx, name, filter):
    try:
        platform = _get_platform(ctx)
        client = ctx.obj['client']
        ext_net = platform.get_external_network(name)
        ext_net_obj = ExternalNetwork(client, resource=ext_net)
        allocated_ip = ext_net_obj.list_allocated_ip_address(filter)
        stdout(allocated_ip, ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command('list-sub-allocated-ip', short_help='list sub allocated IP')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '--filter',
    'filter',
    default=None,
    metavar='<name==gateway*>',
    help='filter for gateway')
def list_sub_allocated_ip(ctx, name, filter):
    try:
        platform = _get_platform(ctx)
        client = ctx.obj['client']
        ext_net = platform.get_external_network(name)
        ext_net_obj = ExternalNetwork(client, resource=ext_net)
        sub_allocated_ip = ext_net_obj.list_gateway_ip_suballocation(filter)
        stdout(sub_allocated_ip, ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command(
    'list-direct-org-vdc-network',
    short_help='list associated direct org vDC networks.')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '--filter',
    'filter',
    default=None,
    metavar='<name==org-vdc-net*>',
    help='filter for org vDC network')
def list_direct_org_vdc_networks(ctx, name, filter):
    try:
        platform = _get_platform(ctx)
        client = ctx.obj['client']
        ext_net = platform.get_external_network(name)
        ext_net_obj = ExternalNetwork(client, resource=ext_net)
        direct_ovdc_networks = \
            ext_net_obj.list_associated_direct_org_vdc_networks(filter)
        result = []
        for direct_ovdc_network in direct_ovdc_networks:
            result.append({'Direct Org VDC Networks': direct_ovdc_network})
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command(
    'list-vsphere-network', short_help='list associated vSphere networks')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '--filter',
    'filter',
    default=None,
    metavar='<name==portgroup*>',
    help='filter for vSphere Network')
def list_vsphere_network(ctx, name, filter):
    try:
        platform = _get_platform(ctx)
        client = ctx.obj['client']
        ext_net = platform.get_external_network(name)
        ext_net_obj = ExternalNetwork(client, resource=ext_net)
        vSphere_network_list = ext_net_obj.list_vsphere_network(filter)
        stdout(vSphere_network_list, ctx)
    except Exception as e:
        stderr(e, ctx)


@external.command('info', short_help='show external network details')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
def external_network_info(ctx, name):
    try:
        platform = _get_platform(ctx)
        client = ctx.obj['client']
        ext_net = platform.get_external_network(name)

        config = ext_net['{' + NSMAP['vcloud'] + '}Configuration']
        output = {}
        count = 0
        for ipscope in config.IpScopes.IpScope:
            ipscope_dict = {}
            ipscope_dict['is_inherited'] = ipscope.IsInherited
            ipscope_dict['gateway'] = ipscope.Gateway
            ipscope_dict['netmask'] = ipscope.Netmask
            if hasattr(ipscope, 'Dns1'):
                ipscope_dict['dns1'] = ipscope.Dns1
            if hasattr(ipscope, 'Dns2'):
                ipscope_dict['dns2'] = ipscope.Dns2
            if hasattr(ipscope, 'DnsSuffix'):
                ipscope_dict['dns_suffix'] = ipscope.DnsSuffix
                ipscope_dict['Is_Enabled'] = ipscope.IsEnabled
            if hasattr(ipscope, 'IpRanges'):
                count_ip_range = 0
                for ip_range in ipscope.IpRanges.IpRange:
                    count_ip_range = count_ip_range + 1
                    ip_range_dict = {}
                    ip_range_dict['start_address'] = ip_range.StartAddress
                    ip_range_dict['end_address'] = ip_range.EndAddress
                    ipscope_dict['ip_range ' + str(count_ip_range)] = \
                        ip_range_dict
            count = count + 1
            output['ipscope ' + str(count)] = ipscope_dict
        if hasattr(config, 'FenceMode'):
            output['fence_mode'] = config.FenceMode
        if hasattr(config, 'RetainNetInfoAcrossDeployments'):
            output['retain_net_info_across_deployment'] = \
                config.RetainNetInfoAcrossDeployments
        if hasattr(ext_net, 'VimPortGroupRef'):
            output['vim_server_href'] = \
                ext_net.VimPortGroupRef.VimServerRef.get('href')
            output['vim_server_id'] = \
                ext_net.VimPortGroupRef.VimServerRef.get('id')
            output['vim_portgroup_moref'] = ext_net.VimPortGroupRef.MoRef
            output['vim_object_type'] = \
                ext_net.VimPortGroupRef.VimObjectType
        stdout(output, ctx)
    except Exception as e:
        stderr(e, ctx)


@network.command('list', short_help='list all org VDC networks in a org')
@click.pass_context
def list_orgvdc_networks(ctx):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        in_use_vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=in_use_vdc_href)

        result = vdc.list_orgvdc_network_records()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
