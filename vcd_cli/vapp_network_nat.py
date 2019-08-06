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

    \b
        vcd vapp network services nat get-nat-type vapp_name network_name
            Get  NAT type and policy in NAT service.

    \b
        vcd vapp network services nat add vapp_name network_name
                --type ipTranslation --vm_id testvm1 --nic_id 1
            Add  NAT rule to NAT service.

    \b
        vcd vapp network services nat add vapp_name network_name
                --type ipTranslation --vm_id testvm1 --nic_id 1 --mapping_mode
                 manual --ext_ip 10.1.1.1
            Add  NAT rule to NAT service.

    \b
        vcd vapp network services nat add vapp_name network_name
                --type portForwarding  --vm_id testvm1 --nic_id 1 --ext_port -1
                --int_port -1 --protocol TCP_UDP
            Add  NAT rule to NAT service.

    \b
        vcd vapp network services nat list vapp_name network_name
            List NAT rules in NAT service.

    \b
        vcd vapp network services nat delete vapp_name network_name id
            Delete NAT rule from NAT service.

    \b
        vcd vapp network services nat update vapp_name network_name rule_id
            --vm_id testvm1 --nic_id 1
            Update  NAT rule to NAT service.

    \b
        vcd vapp network services nat update vapp_name network_name rule_id
                --vm_id testvm1 --nic_id 1 --mapping_mode manual
                --ext_ip 10.1.1.1
            Update  NAT rule to NAT service.

    \b
        vcd vapp network services nat update vapp_name network_name rule_id
                --vm_id testvm1 --nic_id 1 --ext_port -1 --int_port -1
                --protocol TCP_UDP
            Update  NAT rule to NAT service.
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


@nat.command('enable-nat', short_help='enable NAT service')
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


@nat.command('get-nat-type', short_help='get NAT type')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
def get_nat_type(ctx, vapp_name, network_name):
    try:
        vapp_nat = get_vapp_network_nat(ctx, vapp_name, network_name)
        result = vapp_nat.get_nat_type()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@nat.command('add', short_help='add NAT rule')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.option('--type',
              'type',
              required=True,
              metavar='<type>',
              help='type of NAT service')
@click.option('--vm_id',
              'vm_id',
              required=True,
              metavar='<vm_id>',
              help='VM local id')
@click.option('--nic_id',
              'nic_id',
              required=True,
              metavar='<nic_id>',
              help='NIC id of vapp network in vm ')
@click.option('--mapping_mode',
              'mapping_mode',
              default='automatic',
              metavar='<mapping_mode>',
              help='mapping mode of NAT rule')
@click.option('--ext_ip',
              'ext_ip',
              default=None,
              metavar='<ext_ip>',
              help='external IP address')
@click.option('--ext_port',
              'ext_port',
              default=-1,
              metavar='<ext_port>',
              help='external port')
@click.option('--int_port',
              'int_port',
              default=-1,
              metavar='<int_port>',
              help='internal port')
@click.option('--protocol',
              'protocol',
              default='TCP',
              metavar='<protocol>',
              help='protocol')
def add_nat_rule(ctx, vapp_name, network_name, type, vm_id, nic_id,
                 mapping_mode, ext_ip, ext_port, int_port, protocol):
    try:
        vapp_nat = get_vapp_network_nat(ctx, vapp_name, network_name)
        result = vapp_nat.add_nat_rule(nat_type=type,
                                       vapp_scoped_vm_id=vm_id,
                                       vm_nic_id=nic_id,
                                       mapping_mode=mapping_mode,
                                       external_ip_address=ext_ip,
                                       external_port=ext_port,
                                       internal_port=int_port,
                                       protocol=protocol)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@nat.command('list', short_help='list NAT rules')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
def get_list_of_nat_rule(ctx, vapp_name, network_name):
    try:
        vapp_nat = get_vapp_network_nat(ctx, vapp_name, network_name)
        result = vapp_nat.get_list_of_nat_rule()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@nat.command('delete', short_help='delete NAT rules')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.argument('rule_id', metavar='<rule_id>', required=True)
def delete_nat_rule(ctx, vapp_name, network_name, rule_id):
    try:
        vapp_nat = get_vapp_network_nat(ctx, vapp_name, network_name)
        result = vapp_nat.delete_nat_rule(rule_id)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@nat.command('update', short_help='update NAT rule')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.argument('rule_id', metavar='<rule-id>', required=True)
@click.option('--vm_id',
              'vm_id',
              default=None,
              metavar='<vm_id>',
              help='VM local id')
@click.option('--nic_id',
              'nic_id',
              default=None,
              metavar='<nic_id>',
              help='NIC id of vapp network in vm ')
@click.option('--mapping_mode',
              'mapping_mode',
              default=None,
              metavar='<mapping_mode>',
              help='mapping mode of NAT rule')
@click.option('--ext_ip',
              'ext_ip',
              default=None,
              metavar='<ext_ip>',
              help='external IP address')
@click.option('--ext_port',
              'ext_port',
              default=None,
              metavar='<ext_port>',
              help='external port')
@click.option('--int_port',
              'int_port',
              default=None,
              metavar='<int_port>',
              help='internal port')
@click.option('--protocol',
              'protocol',
              default=None,
              metavar='<protocol>',
              help='protocol')
def update_nat_rule(ctx, vapp_name, network_name, rule_id, vm_id, nic_id,
                    mapping_mode, ext_ip, ext_port, int_port, protocol):
    try:
        vapp_nat = get_vapp_network_nat(ctx, vapp_name, network_name)
        result = vapp_nat.update_nat_rule(rule_id=rule_id,
                                          vapp_scoped_vm_id=vm_id,
                                          vm_nic_id=nic_id,
                                          mapping_mode=mapping_mode,
                                          external_ip_address=ext_ip,
                                          external_port=ext_port,
                                          internal_port=int_port,
                                          protocol=protocol)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
