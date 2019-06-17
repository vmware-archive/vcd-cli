# VMware vCloud Director CLI
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
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout

from vcd_cli.vcd import vcd  # NOQA
from vcd_cli.vapp import vapp  # NOQA
from vcd_cli.vapp import get_vapp


@vapp.group(short_help='work with vapp network')
@click.pass_context
def network(ctx):
    """Work with vapp network.

\b
   Description
        Work with the vapp networks.

\b
        vdc vapp network create vapp1 vapp-network1
                --subnet 192.168.1.1/24
                --description 'vApp network'
                --dns1 8.8.8.8
                --dns2 8.8.8.9
                --dns-suffix example.com
                --ip-range 192.168.1.2-192.168.1.49
                --ip-range 192.168.1.100-192.168.1.149
                --guest-vlan-allowed-enabled
            Create a vApp network.

\b
        vdc vapp network reset vapp1 vapp-network1
            Reset a vApp network.

\b
        vdc vapp network delete vapp1 vapp-network1
            Delete a vApp network.

\b
        vdc vapp network update vapp1 vapp-network1 -n NewName -d Description
            Update a vApp network.

\b
        vdc vapp network add-ip-range vapp1 vapp-network1
                --ip-range 6.6.5.2-6.6.5.20
            Add IP range to the vApp network.

\b
        vdc vapp network delete-ip-range vapp1 vapp-network1
                --ip-range 6.6.5.2-6.6.5.20
            Delete IP range from vApp network.

\b
        vdc vapp network update-ip-range vapp1 vapp-network1
                --ip-range 6.6.5.2-6.6.5.20 --new-ip-range 6.6.5.10-6.6.5.18
            Update IP range of vApp network.

\b
        vdc vapp network add-dns vapp1 vapp-network1
                --dns1 6.6.5.2 --dns2 6.6.5.10-6.6.5.18
                --dns-suffix example.com
            Add DNS detail to vApp network.

\b
        vcd vapp network list-allocated-ip vapp1 vapp-network1
            List allocated ip

\b
        vcd vapp network list vapp1
            List vapp networks
    """
    pass


@network.command('create', short_help='create a vApp network')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('name', metavar='<name>', required=True)
@click.option(
    '--subnet', 'subnet', required=True, metavar='<CIDR>', help='Network CIDR')
@click.option(
    '--description',
    'description',
    metavar='<description>',
    help='description')
@click.option(
    '--dns1', 'primary_dns_ip', metavar='<IP>', help='primary DNS IP')
@click.option(
    '--dns2', 'secondary_dns_ip', metavar='<IP>', help='secondary DNS IP')
@click.option(
    '--dns-suffix', 'dns_suffix', metavar='<Name>', help='dns suffix')
@click.option(
    '--ip-range',
    'ip_ranges',
    multiple=True,
    metavar='<ip-range-start-ip-range-end>',
    help='IP range')
@click.option(
    '--guest-vlan-allowed-enabled/--guest-vlan-allowed-disabled',
    'is_guest_vlan_allowed',
    default=False,
    metavar='<bool>',
    help='guest vlan allowed')
def create_vapp_network(ctx, vapp_name, name, subnet, description,
                        primary_dns_ip, secondary_dns_ip, dns_suffix,
                        ip_ranges, is_guest_vlan_allowed):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        task = vapp.create_vapp_network(
            name, subnet, description, primary_dns_ip, secondary_dns_ip,
            dns_suffix, ip_ranges, is_guest_vlan_allowed)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@network.command('reset', short_help='reset a vApp network')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('network-name', metavar='<network-name>', required=True)
def reset_vapp_network(ctx, vapp_name, network_name):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        task = vapp.reset_vapp_network(network_name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@network.command('delete', short_help='delete a vApp network')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('network-name', metavar='<network-name>', required=True)
def delete_vapp_network(ctx, vapp_name, network_name):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        task = vapp.delete_vapp_network(network_name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@network.command(
    'update', short_help='update vapp network\'s name and description')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('network-name', metavar='<network-name>', required=True)
@click.option(
    '-n',
    '--name',
    'name',
    default=None,
    metavar='<name>',
    help='new name of the network')
@click.option(
    '-d',
    '--description',
    'description',
    default=None,
    metavar='<description>',
    help='new description of the network')
def update_vapp_network(ctx, vapp_name, network_name, name, description):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)

        task = vapp.update_vapp_network(network_name, name, description)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@network.command('add-ip-range', short_help='add IP range/s to the network')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.option(
    '-i',
    '--ip-range',
    'ip_range',
    required=True,
    multiple=True,
    metavar='<ip>',
    help='ip range in StartAddress-EndAddress format')
def add_ip_range(ctx, vapp_name, network_name, ip_range):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        for range in ip_range:
            ranges = range.split('-')
            task = vapp.add_ip_range(network_name, ranges[0], ranges[1])
            stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@network.command('delete-ip-range', short_help='delete an IP range in network')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.option(
    '-i',
    '--ip-range',
    'ip_range',
    required=True,
    metavar='<ip>',
    help='ip range in StartAddress-EndAddress format')
def delete_ip_range(ctx, vapp_name, network_name, ip_range):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        ranges = ip_range.split('-')
        task = vapp.delete_ip_range(network_name, ranges[0], ranges[1])
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@network.command(
    'update-ip-range', short_help='update IP range/s of the network')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.option(
    '-i',
    '--ip-range',
    'ip_range',
    required=True,
    metavar='<ip>',
    help='IP range in StartAddress-EndAddress format')
@click.option(
    '-n',
    '--new-ip-range',
    'new_ip_range',
    required=True,
    metavar='<ip>',
    help='new IP range in StartAddress-EndAddress format')
def update_ip_range(ctx, vapp_name, network_name, ip_range, new_ip_range):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        range = ip_range.split('-')
        new_range = new_ip_range.split('-')
        task = vapp.update_ip_range(network_name, range[0], range[1],
                                    new_range[0], new_range[1])
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@network.command('add-dns', short_help='add DNS to vapp network')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.option(
    '--dns1',
    'primary_dns_ip',
    default=None,
    metavar='<ip>',
    help='IP of the primary dns server')
@click.option(
    '--dns2',
    'secondary_dns_ip',
    default=None,
    metavar='<ip>',
    help='IP of the secondary dns server')
@click.option(
    '--dns-suffix',
    'dns_suffix',
    default=None,
    metavar='<name>',
    help='dns suffix')
def add_dns_to_vapp_network(ctx, vapp_name, network_name, primary_dns_ip,
                            secondary_dns_ip, dns_suffix):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        task = vapp.update_dns_vapp_network(network_name, primary_dns_ip,
                                            secondary_dns_ip, dns_suffix)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@network.command('list-allocated-ip', short_help='list allocated IP')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
def list_allocated_ip(ctx, vapp_name, network_name):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        task = vapp.list_ip_allocations(network_name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@network.command('list', short_help='list vapp networks')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
def list_vapp_networks(ctx, vapp_name):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        task = vapp.get_vapp_network_list()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@network.group('services', short_help='manage vapp network services')
@click.pass_context
def services(ctx):
    """Configure services of vapp network."""
    pass
