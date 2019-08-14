# VMware vCloud Director Python SDK
# Copyright (c) 2014-2019 VMware, Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import click
from pyvcloud.vcd.vapp_static_route import VappStaticRoute
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vapp_network import services


@services.group('static-route',
                short_help='manage static route service of vapp network')
@click.pass_context
def static_route(ctx):
    """Manage static route service of vapp network.

    \b
        vcd vapp network services static-route enable-service vapp_name
                network_name --enable
            Enable static route service.

    \b
        vcd vapp network services static-route enable-service vapp_name
                network_name --disable
            Disable static route service.

    \b
        vcd vapp network services static-route add vapp_name network_name
                --name route_name
                --nhip next_hop_ip
                --network network_cidr
            Add static route in static route service.

    \b
        vcd vapp network services static-route list vapp_name network_name
            List static route in static route service.

    \b
        vcd vapp network services static-route update vapp_name network_name
                route_name
                --name new_route_name
                --network network_cidr
                --nhip next_hop_ip
            Update static route in static route service.

    \b
        vcd vapp network services static-route delete vapp_name network_name
                route_name
            Delete static route in static route service.
    """


def get_vapp_network_static_route(ctx, vapp_name, network_name):
    """Get the VappStaticRoute object.

    It will restore sessions if expired. It will reads the client and
    creates the VappStaticRoute object.
    """
    restore_session(ctx, vdc_required=True)
    client = ctx.obj['client']
    vapp_static_route = VappStaticRoute(client, vapp_name, network_name)
    return vapp_static_route


@static_route.command('enable-service',
                      short_help='enable static route service')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.option('--enable/--disable',
              'is_enabled',
              default=True,
              metavar='<is_enable>',
              help='enable static route service')
def enable_service(ctx, vapp_name, network_name, is_enabled):
    try:
        static_route = get_vapp_network_static_route(ctx, vapp_name,
                                                     network_name)
        result = static_route.enable_service(is_enabled)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@static_route.command('add',
                      short_help='add static route in static route service')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.option('--name',
              'route_name',
              required=True,
              metavar='<route-name>',
              help='route name')
@click.option('--network',
              'network_cidr',
              required=True,
              metavar='<network-cidr>',
              help='network CIDR')
@click.option('--nhip',
              'next_hop_ip',
              required=True,
              metavar='<next-hop-ip>',
              help='next hop IP')
def add(ctx, vapp_name, network_name, route_name, network_cidr, next_hop_ip):
    try:
        static_route = get_vapp_network_static_route(ctx, vapp_name,
                                                     network_name)
        result = static_route.add(route_name, network_cidr, next_hop_ip)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@static_route.command('list',
                      short_help='list static route in static route service')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
def list(ctx, vapp_name, network_name):
    try:
        static_route = get_vapp_network_static_route(ctx, vapp_name,
                                                     network_name)
        result = static_route.list()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@static_route.command('update',
                      short_help='update static route in static route service')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.argument('route_name', metavar='<route-name>', required=True)
@click.option('--name',
              'route_new_name',
              default=None,
              metavar='<route-new-name>',
              help='route new name')
@click.option('--network',
              'network_cidr',
              default=None,
              metavar='<network-cidr>',
              help='network CIDR')
@click.option('--nhip',
              'next_hop_ip',
              default=None,
              metavar='<next-hop-ip>',
              help='next hop IP')
def update(ctx, vapp_name, network_name, route_name, route_new_name,
           network_cidr, next_hop_ip):
    try:
        static_route = get_vapp_network_static_route(ctx, vapp_name,
                                                     network_name)
        result = static_route.update(name=route_name,
                                     new_name=route_new_name,
                                     network_cidr=network_cidr,
                                     next_hop_ip=next_hop_ip)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@static_route.command('delete',
                      short_help='delete static route in static route service')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.argument('route_name', metavar='<route-name>', required=True)
def list(ctx, vapp_name, network_name, route_name):
    try:
        static_route = get_vapp_network_static_route(ctx, vapp_name,
                                                     network_name)
        result = static_route.delete(route_name)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
