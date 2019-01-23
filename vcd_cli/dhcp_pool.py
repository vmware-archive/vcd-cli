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
from pyvcloud.vcd.client import GatewayBackingConfigType
from pyvcloud.vcd.vdc import VDC

from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import vcd
from vcd_cli.utils import tuple_to_dict
from vcd_cli.gateway import gateway  # NOQA
from vcd_cli.gateway import get_gateway
from vcd_cli.gateway import services

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
            --lease 8640 --subnet 255.255.255.0

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

