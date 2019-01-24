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
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
# Don't change the order of vcd  nd gateway
from vcd_cli.vcd import vcd #NOQA
from vcd_cli.gateway import gateway # NOQA
from vcd_cli.gateway import get_gateway
from vcd_cli.gateway import services

from pyvcloud.vcd.dhcp_pool import DhcpPool

LEASE_TIME = '8640'
@services.group('dhcp-pool', short_help='manage DHCP pool of the gateway')
@click.pass_context
def dhcp_pool(ctx):
    """Manages DHCP pool of gateway.

    \b
        Examples
            vcd gateway services dhcp-pool create gateway1 --range 30.20.10.11-
            30.20.10.15 --enable-auto-dns --gateway-ip 30.20.10.1 --domain
            abc.com --primary-server 30.20.10.20 --secondary-server 30.20.10.21
            --expire-lease --lease 8640 --subnet 255.255.255.0

            Create dhcp rule.
    \b
            vcd gateway services dhcp-pool delete test_gateway1 pool-1
                Deletes the DHCP pool
    \b
            vcd gateway services dhcp-pool list test_gateway1
                Lists the DHCP pool
    \b
            vcd gateway services dhcp-pool info test_gateway1 pool-1
                Info DHCP pool

    """


@dhcp_pool.command("create", short_help="create new DHCP pool")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.option(
   '-r',
   '--range',
   'ip_range',
   required=True,
   default=None,
   metavar='<IP range of the pool>',
   help='IP range of the DHCP pool')
@click.option(
   '--enable-auto-dns/--disable-auto-dns',
   'is_auto_dns',
   metavar='<bool>',
   default=False,
   help='Auto configure DNS')
@click.option(
   '-g'
   '--gateway-ip',
   'gateway_ip',
   metavar='<default-gateway-ip>',
   default=None,
   help='Default gateway ip')
@click.option(
   '-d'
   '--domain',
   'domain',
   metavar='<domain-name>',
   default=None,
   help='domain name')
@click.option(
   '-p'
   '--primary-server',
   'primary_server',
   metavar='<primary-name-server>',
   default=None,
   help='primary server ip')
@click.option(
   '-s'
   '--secondary-server',
   'secondary_server',
   metavar='<secondary-name-server>',
   default=None,
   help='secondary server ip')
@click.option(
   '-l'
   '--lease',
   'lease',
   metavar='<lease-time>',
   default=LEASE_TIME,
   help='lease time')
@click.option(
   '--never-expire-lease/--expire-lease',
   'lease_expire',
   metavar='<bool>',
   default=False,
   help='lease lease expire')
@click.option(
   '--subnet',
   'subnet',
   metavar='<subnet>',
   default=None,
   help='subnet mask')
def create_dhcp_pool(ctx, gateway_name, ip_range, is_auto_dns, gateway_ip,
                     domain, lease_expire, primary_server, secondary_server,
                     lease, subnet):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        gateway_resource.add_dhcp_pool(ip_range, is_auto_dns, gateway_ip
                                              , domain, lease_expire, lease,
                                              subnet, primary_server,
                                              secondary_server)
        stdout('DHCP Pool created successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@dhcp_pool.command("delete", short_help="deletes the DHCP pool")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.argument('pool_id', metavar='<dhcp pool id>', required=True)
def delete_dhcp_pool(ctx, gateway_name, pool_id):
    try:
        resource = get_dhcp_pool(ctx, gateway_name, pool_id)
        resource.delete_pool()
        stdout('DHCP Pool deleted successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


def get_dhcp_pool(ctx, gateway_name, pool_id):
    """Get the DHCP pool resource.

    It will restore sessions if expired. It will reads the client and
    creates the DHCP pool resource object.
    """
    restore_session(ctx, vdc_required=True)
    client = ctx.obj['client']
    resource = DhcpPool(client, gateway_name, pool_id)
    return resource


@dhcp_pool.command("list", short_help="lists the DHCP pool")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
def list_dhcp_pool(ctx, gateway_name):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        result = gateway_resource.list_dhcp_pools()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@dhcp_pool.command("info", short_help="info about DHCP pool")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.argument('pool_id', metavar='<dhcp pool id>', required=True)
def info_dhcp_pool(ctx, gateway_name, pool_id):
    try:
        resource = get_dhcp_pool(ctx, gateway_name, pool_id)
        result = resource.get_pool_info()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
