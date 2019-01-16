# VMware vCloud Director CLI
#
# Copyright (c) 2017-2019 VMware, Inc. All Rights Reserved.
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

from pyvcloud.vcd.client import MetadataDomain
from pyvcloud.vcd.client import MetadataValueType
from pyvcloud.vcd.client import MetadataVisibility
from pyvcloud.vcd.client import NSMAP
from pyvcloud.vcd.exceptions import InvalidParameterException
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.vdc_network import VdcNetwork

from vcd_cli.network import network
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout


@network.group(short_help='work with routed org vdc networks')
@click.pass_context
def routed(ctx):
    """Work with routed org vdc networks.

\b
    Examples
        vcd network routed create routed_network -g/--gateway-name gateway_name
            --subnet 5.5.6.1/20 --description description
            --primary-dns-ip 7.7.7.3 --secondary-dns-ip 7.7.7.4
            --dns-suffix test-suffix --ip-range 5.5.6.2-5.5.6.100
            --shared-enabled --guest-vlan-allowed-enabled
            --sub-interface-enabled --distributed-interface-enabled
            --retain-net-info-across-deployments-enabled
        Creates a routed org vdc network
\b
        vcd network routed edit name -n/--name name1
            --description new_description
            --shared-enabled/--shared-disabled
        Edit name, description and shared state of org vdc network

\b
        vcd network routed add-ip-ranges vdc_routed_nw
            --ip-range  2.2.3.1-2.2.3.2
            --ip-range 2.2.4.1-2.2.4.2

\b
        vcd network routed modify-ip-range vdc_routed_nw
                       --ip-range 192.168.1.2-192.168.1.20
                       --new-ip-range 192.168.1.25-192.168.1.50

\b
        vcd network routed list
            List all routed org vdc networks in the selected vdc

\b
        vcd network routed set-metadata vdc_routed_nw -k key1 -v value1
            Set a metadata entry in a routed org vdc network with default
            domain, visibility and metadata value type

\b
        vcd network routed remove-metadata vdc_routed_nw -k key1
            Remove a metadata entry from a routed org vdc network

\b
        vcd network routed list-metadata vdc_routed_nw
            List all metadata entries in a routed org vdc network
    """
    pass


@routed.command('create', short_help='Creates a routed org vdc network.')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-g',
    '--gateway-name',
    'gateway_name',
    required=True,
    metavar='<name>',
    help='name of gateway to which this network will connect')
@click.option(
    '--subnet',
    'subnet',
    required=True,
    metavar='<CIDR format. e.g.,x.x.x.x/20>',
    help='Network CIDR')
@click.option(
    '--description',
    'description',
    metavar='<description>',
    help='description')
@click.option(
    '--primary-dns-ip',
    'primary_dns_ip',
    metavar='<IP>',
    help='primary DNS IP')
@click.option(
    '--secondary-dns-ip',
    'secondary_dns_ip',
    metavar='<IP>',
    help='secondary DNS IP')
@click.option(
    '--dns-suffix', 'dns_suffix', metavar='<Name>', help='dns suffix')
@click.option(
    '--dns-suffix', 'dns_suffix', metavar='<Name>', help='dns suffix')
@click.option(
    '--ip-range',
    'ip_range',
    metavar='<ip_range_start-ip_range_end>',
    help='IP range')
@click.option(
    '--shared-enabled/--shared-disabled',
    'is_shared',
    default=False,
    metavar='<bool>',
    help='shared enabled')
@click.option(
    '--guest-vlan-allowed-enabled/--guest-vlan-allowed-disabled',
    'is_guest_vlan_allowed',
    default=False,
    metavar='<bool>',
    help='guest vlan allowed')
@click.option(
    '--sub-interface-enabled/--sub-interface-disabled',
    'is_sub_interface',
    default=False,
    metavar='<bool>',
    help='create as sub interface')
@click.option(
    '--distributed-interface-enabled/--distributed-interface-disabled',
    'is_distributed_interface',
    default=False,
    metavar='<bool>',
    help='create as distributed interface')
@click.option(
    '--retain-net-info-across-deployments-enabled/--retain-net-info-across'
    '-deployments-disabled',
    'is_retain_net_info_across_deployments',
    default=False,
    metavar='<bool>',
    help='retain net info across deployment')
def create_routed_vdc_network(ctx, name, gateway_name, subnet, description,
                              primary_dns_ip, secondary_dns_ip, dns_suffix,
                              ip_range, is_shared, is_guest_vlan_allowed,
                              is_sub_interface, is_distributed_interface,
                              is_retain_net_info_across_deployments):
    try:
        vdc = _get_vdc_ref(ctx)
        ip_range_start = None
        ip_range_end = None
        if ip_range is not None:
            ip_range_arr = ip_range.split('-')
            if len(ip_range_arr) != 2:
                raise InvalidParameterException(
                    'IP Range should in x.x.x.x-y.y.y.y format.')
            ip_range_start = ip_range_arr[0]
            ip_range_end = ip_range_arr[1]

        routed_network = vdc.create_routed_vdc_network(
            name, gateway_name, subnet, description, primary_dns_ip,
            secondary_dns_ip, dns_suffix, ip_range_start, ip_range_end,
            is_shared, is_guest_vlan_allowed, is_sub_interface,
            is_distributed_interface, is_retain_net_info_across_deployments)
        stdout(routed_network.Tasks.Task[0], ctx)
        stdout('Routed org vdc network created successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


def _get_vdc_ref(ctx):
    """Get the sdk's vdc resource.

    It will restore sessions if expired. It will read the client and vdc href
    from the context and create VDC object.
    """
    restore_session(ctx, vdc_required=True)
    client = ctx.obj['client']
    in_use_vdc_href = ctx.obj['profiles'].get('vdc_href')
    return VDC(client, href=in_use_vdc_href)


@routed.command('delete', short_help='delete org vdc routed network')
@click.pass_context
@click.argument('name', metavar='<vdc routed network name>', required=True)
def delete_vdc_routed_network(ctx, name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        task = vdc.delete_routed_orgvdc_network(name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@routed.command('edit', short_help='Edit a routed org vdc network.')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-n',
    '--name',
    'new_vdc_routed_nw_name',
    required=True,
    metavar='<name>',
    help='new name of org vdc network')
@click.option(
    '--description',
    'description',
    metavar='<description>',
    help='new description')
@click.option(
    '--shared-enabled/--shared-disabled',
    'is_shared',
    default=None,
    metavar='<bool>',
    help='share this network with other VDCs in the organization')
def edit_routed_vdc_network(ctx,
                            name,
                            new_vdc_routed_nw_name,
                            description=None,
                            is_shared=None):
    try:
        vdc = _get_vdc_ref(ctx)
        client = ctx.obj['client']
        routed_network = vdc.get_routed_orgvdc_network(name)
        is_shared if is_shared is not None else routed_network.IsShared
        vdcNetwork = VdcNetwork(client, resource=routed_network)
        task = vdcNetwork.edit_name_description_and_shared_state(
            new_vdc_routed_nw_name, description, is_shared)

        stdout(task, ctx)
        stdout('Routed org vdc network updated successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@routed.command(
    'add-ip-ranges', short_help='add IP range of '
    'routed org vdc network.')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-i',
    '--ip-range',
    'ip_ranges',
    required=True,
    multiple=True,
    metavar='<ip>',
    help='ip range in StartAddress-EndAddress format')
def add_ip_ranges_of_routed_vdc_network(ctx, name, ip_ranges):
    try:
        vdc = _get_vdc_ref(ctx)
        client = ctx.obj['client']
        routed_network = vdc.get_routed_orgvdc_network(name)
        vdcNetwork = VdcNetwork(client, resource=routed_network)
        task = vdcNetwork.add_static_ip_pool(ip_ranges)
        stdout(task, ctx)
        stdout('IP ranges are added to routed org vdc network successfully.',
               ctx)
    except Exception as e:
        stderr(e, ctx)


@routed.command(
    'list', short_help='list all routed org vdc networks in the selected vdc')
@click.pass_context
def list_routed_networks(ctx):
    try:
        vdc = _get_vdc_ref(ctx)
        routed_nets = vdc.list_orgvdc_routed_networks()
        result = []
        for routed_net in routed_nets:
            result.append({'name': routed_net.get('name')})
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@routed.command(
    'modify-ip-range',
    short_help='Modify IP range of '
    'routed org vdc network.')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
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
def modify_ip_range_of_routed_vdc_network(ctx, name, ip_range, new_ip_range):
    try:
        vdc = _get_vdc_ref(ctx)
        client = ctx.obj['client']
        routed_network = vdc.get_routed_orgvdc_network(name)
        vdcNetwork = VdcNetwork(client, resource=routed_network)
        task = vdcNetwork.modify_static_ip_pool(ip_range, new_ip_range)
        stdout(task, ctx)
        stdout('IP range of routed org vdc network is modified successfully.',
               ctx)
    except Exception as e:
        stderr(e, ctx)


@routed.command(
    'list-metadata', short_help='List metadata of a routed org vdc network.')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
def list_metadata(ctx, name):
    try:
        vdc = _get_vdc_ref(ctx)
        client = ctx.obj['client']
        routed_network = vdc.get_routed_orgvdc_network(name)
        vdcNetwork = VdcNetwork(client, resource=routed_network)
        metadata = vdcNetwork.get_all_metadata()
        result = []
        for metadata_entry in metadata.MetadataEntry:
            visibility = MetadataVisibility.READ_WRITE.value
            if hasattr(metadata_entry, 'Domain'):
                visibility = metadata_entry.Domain.get('visibility')
            type = metadata_entry.TypedValue.get('{' + NSMAP['xsi'] + '}type')
            result.append({
                'Name': metadata_entry.Key,
                'Value': metadata_entry.TypedValue.Value,
                'Type': type,
                'User access': visibility
            })
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@routed.command(
    'set-metadata', short_help='Set metadata to a routed org vdc network.')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-k',
    '--key',
    'key',
    required=True,
    metavar='<key>',
    help='metadata key name')
@click.option(
    '-v',
    '--value',
    'value',
    required=True,
    metavar='<value>',
    help='metadata value')
@click.option(
    '-d',
    '--domain',
    'domain',
    default=MetadataDomain.GENERAL,
    metavar='<domain>',
    help='metadata domain')
@click.option(
    '-i',
    '--visibility',
    'visibility',
    default=MetadataVisibility.READ_WRITE,
    metavar='<visibility>',
    help='visibility of metadata')
@click.option(
    '-t',
    '--value-type',
    'value_type',
    default=MetadataValueType.STRING,
    metavar='<value-type>',
    help='metadata value type')
def set_metadata(ctx, name, key, value, domain, visibility, value_type):
    try:
        vdc = _get_vdc_ref(ctx)
        client = ctx.obj['client']
        routed_network = vdc.get_routed_orgvdc_network(name)
        vdcNetwork = VdcNetwork(client, resource=routed_network)
        task = vdcNetwork.set_metadata(key, value, domain, visibility,
                                       value_type)
        stdout(task, ctx)
        stdout('Metadata is set to routed org vdc network successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@routed.command(
    'remove-metadata',
    short_help='Remove metadata from a routed org vdc network.')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '-k',
    '--key',
    'key',
    required=True,
    metavar='<key>',
    help='metadata key name')
@click.option(
    '-d',
    '--domain',
    'domain',
    default=MetadataDomain.GENERAL,
    metavar='<domain>',
    help='metadata domain')
def remove_metadata(ctx, name, key, domain):
    try:
        vdc = _get_vdc_ref(ctx)
        client = ctx.obj['client']
        routed_network = vdc.get_routed_orgvdc_network(name)
        vdcNetwork = VdcNetwork(client, resource=routed_network)
        task = vdcNetwork.remove_metadata(key, domain)
        stdout(task, ctx)
        stdout('Metadata is removed from vdc routed network successfully.',
               ctx)
    except Exception as e:
        stderr(e, ctx)
