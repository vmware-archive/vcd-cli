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
from pyvcloud.vcd.vapp_nat import VappNat
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vapp_network import services


@services.group('nat', short_help='manage NAT service of vapp network')
@click.pass_context
def nat(ctx):
    """Manages NAT service of vapp network.

    \b
        Examples
            vcd vapp network services nat enable-nat vapp_name network_name
                    --enable
                Enable NAT service.

    \b
        vcd vapp network services nat set-nat-type vapp_name network_name
                --type ipTranslation --policy allowTrafficIn
            Set NAT type in NAT service.
    """


def get_vapp_network_nat(ctx, vapp_name, network_name):
    """Get the VappNat object.

    It will restore sessions if expired. It will reads the client and
    creates the VappNat object.
    """
    restore_session(ctx, vdc_required=True)
    client = ctx.obj['client']
    vapp_nat = VappNat(client, vapp_name, network_name)
    return vapp_nat


@nat.command('enable-nat', short_help='Enable NAT service')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.option('--enable/--disable',
              'is_enabled',
              default=True,
              metavar='<is_enable>',
              help='enable NAT service')
def enable_nat_service(ctx, vapp_name, network_name, is_enabled):
    try:
        vapp_nat = get_vapp_network_nat(ctx, vapp_name, network_name)
        result = vapp_nat.enable_nat_service(is_enabled)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@nat.command('set-nat-type', short_help='set NAT type')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.option('--type',
              'type',
              default='ipTranslation',
              metavar='<type>',
              help='type of NAT service')
@click.option('--policy',
              'policy',
              default='allowTrafficIn',
              metavar='<policy>',
              help='policy of NAT service')
def update_nat_type(ctx, vapp_name, network_name, type, policy):
    try:
        vapp_nat = get_vapp_network_nat(ctx, vapp_name, network_name)
        result = vapp_nat.update_nat_type(type, policy)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
