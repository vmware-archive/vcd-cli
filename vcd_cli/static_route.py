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
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
# Don't change the order of vcd  and gateway
from vcd_cli.vcd import vcd #NOQA
from vcd_cli.gateway import gateway # NOQA
from vcd_cli.gateway import get_gateway
from vcd_cli.gateway import services


@services.group('static-route', short_help='manage static routes of gateway')
@click.pass_context
def static_route(ctx):
    """Manages static routes of gateway.

\b
        Examples
            vcd gateway services static-route create test_gateway1 --type User
            --network 192.169.1.0/24 --next-hop 2.2.3.30 --mtu 1500
            --desc "Static Route Created" -v 0
                Create a new static route

\b
            vcd gateway services static-route list test_gateway1
                List all static routes
    """


@static_route.command("create", short_help="create a new static route")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.option(
    '--type',
    'type',
    default='User',
    metavar='<User>',
    help='type')
@click.option(
    '-n',
    '--network',
    'network',
    default=None,
    metavar='<ip>',
    help='IP address of network in CIDR format')
@click.option(
    '-h',
    '--next-hop',
    'next_hop',
    default=None,
    metavar='<ip>',
    help='IP address of the next hop')
@click.option(
    '--mtu',
    'mtu',
    default=1500,
    metavar='<mtu>',
    help='enable/disable the SNAT rule')
@click.option(
    '--desc',
    'description',
    default=None,
    metavar='<description>',
    help='description')
@click.option(
    '-v',
    'vnic',
    default=0,
    metavar='<vnic>',
    help='interface of gateway')
def create_static_route(ctx, gateway_name, type, network, next_hop,
                        mtu, description, vnic):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        gateway_resource.add_static_route(network, next_hop, mtu,
                                          description, type, vnic)
        stdout('Static route created successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@static_route.command('list', short_help='List all static routes on a gateway')
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
def list_static_routes(ctx, gateway_name):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        static_route_list = gateway_resource.list_static_routes()
        stdout(static_route_list, ctx)
    except Exception as e:
        stderr(e, ctx)
