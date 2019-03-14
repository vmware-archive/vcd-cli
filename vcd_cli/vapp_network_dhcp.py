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
from pyvcloud.vcd.vapp_dhcp import VappDhcp
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vapp_network import services

DEFAULT_LEASE_TIME = '3600'
MAX_LEASE_TIME = '7200'


@services.group('dhcp', short_help='manage DHCP service of vapp network')
@click.pass_context
def dhcp(ctx):
    """Manages DHCP service of vapp network.

    \b
        Examples
            vcd vapp network services dhcp set vapp_name network_name --i
                    10.11.11.1-10.11.11.100 --default-lease-time 4500
                    --max-lease-time 7000
                Set dhcp service information

    \b
            vcd vapp network services dhcp enable-dhcp vapp_name network_name
                    --enable
                Enable DHCP service.
    """


def get_vapp_network_dhcp(ctx, vapp_name, network_name):
    """Get the VappDhcp object.

    It will restore sessions if expired. It will reads the client and
    creates the VappDhcp object.
    """
    restore_session(ctx, vdc_required=True)
    client = ctx.obj['client']
    vapp_dhcp = VappDhcp(client, vapp_name, network_name)
    return vapp_dhcp


@dhcp.command('set', short_help='Set DHCP service information')
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
    '-dlt',
    '--default-lease-time',
    'default_lease_time',
    default=DEFAULT_LEASE_TIME,
    metavar='<ip>',
    help='default lease time')
@click.option(
    '-mlt',
    '--max-lease-time',
    'max_lease_time',
    default=MAX_LEASE_TIME,
    metavar='<ip>',
    help='max lease time')
def set(ctx, vapp_name, network_name, ip_range, default_lease_time,
        max_lease_time):
    try:
        vapp_dhcp = get_vapp_network_dhcp(ctx, vapp_name, network_name)
        result = vapp_dhcp.set_dhcp_service(ip_range, default_lease_time,
                                            max_lease_time)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@dhcp.command('enable-dhcp', short_help='Enable DHCP Service')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.option(
    '--enable/--disable', 'is_enabled', default=True, metavar='<is_dhcp>')
def enable_dhcp_service(ctx, vapp_name, network_name, is_enabled):
    try:
        vapp_dhcp = get_vapp_network_dhcp(ctx, vapp_name, network_name)
        result = vapp_dhcp.enable_dhcp_service(is_enabled)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
