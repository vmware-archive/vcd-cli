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
from pyvcloud.vcd.vapp_firewall import VappFirewall
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vapp_network import services


@services.group(
    'firewall', short_help='manage firewall service of vapp network')
@click.pass_context
def firewall(ctx):
    """Manages firewall service of vapp network.

    \b
        Examples
            vcd vapp network services firewall enable-firewall vapp_name
                    network_name --enable
                Enable firewall service.
    """


def get_vapp_network_dhcp(ctx, vapp_name, network_name):
    """Get the VappFirewall object.

    It will restore sessions if expired. It will reads the client and
    creates the VappFirewall object.
    """
    restore_session(ctx, vdc_required=True)
    client = ctx.obj['client']
    vapp_dhcp = VappFirewall(client, vapp_name, network_name)
    return vapp_dhcp


@firewall.command('enable-firewall', short_help='Enable firewall service')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.option(
    '--enable/--disable', 'is_enabled', default=True, metavar='<is_firewall>')
def enable_dhcp_service(ctx, vapp_name, network_name, is_enabled):
    try:
        vapp_firewall = get_vapp_network_dhcp(ctx, vapp_name, network_name)
        result = vapp_firewall.enable_firewall_service(is_enabled)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
