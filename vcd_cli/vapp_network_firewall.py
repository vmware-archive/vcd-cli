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


@services.group('firewall',
                short_help='manage firewall service of vapp network')
@click.pass_context
def firewall(ctx):
    """Manages firewall service of vapp network.

    \b
        Examples
            vcd vapp network services firewall enable-firewall vapp_name
                    network_name --enable
                Enable firewall service.

    \b
        vcd vapp network services firewall set-default-action vapp_name
                network_name --action allow --log-action False
            Set deault action in firewall service.

    \b
        vcd vapp network services firewall list vapp_name network_name
            List firewall rules in firewall service.

    \b
        vcd vapp network services firewall add vapp_name network_name rule_name
                --enable --policy drop --protocols Tcp,Udp --source-ip Any
                 --source-port-range Any --destination-port-range Any
                --destination-ip Any --enable-logging
            Add firewall rule in firewall service.

    \b
        vcd vapp network services firewall update vapp_name network_name
                rule_name --name rule_new_name --enable --policy
                drop --protocols Tcp,Udp --source-ip Any
                --source-port-range Any --destination-port-range Any
                --destination-ip Any --enable-logging
            Update firewall rule in firewall service.

    \b
        vcd vapp network services firewall delete vapp_name network_name
                --name firewall_rule_name
            Delete firewall rule in firewall service.
    """


def get_vapp_network_firewall(ctx, vapp_name, network_name):
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
@click.option('--enable/--disable',
              'is_enabled',
              default=True,
              metavar='<is_enable>',
              help='enable firewall service')
def enable_firewall_service(ctx, vapp_name, network_name, is_enabled):
    try:
        vapp_firewall = get_vapp_network_firewall(ctx, vapp_name, network_name)
        result = vapp_firewall.enable_firewall_service(is_enabled)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command('set-default-action',
                  short_help='set default action of firewall service')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.option('--action',
              'action',
              default='drop',
              metavar='<action>',
              help='deafult action on firewall service')
@click.option('--enable-log-action/--disable-log-action',
              'log_action',
              default=True,
              metavar='<log_action>',
              help='default action on firewall service log')
def set_default_action(ctx, vapp_name, network_name, action, log_action):
    try:
        vapp_firewall = get_vapp_network_firewall(ctx, vapp_name, network_name)
        result = vapp_firewall.set_default_action(action, log_action)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command('add', short_help='add firewall rule to firewall service')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.argument('firewall_rule_name',
                metavar='<firewall-rule-name>',
                required=True)
@click.option('--enable/--disable',
              'is_enable',
              default=True,
              metavar='<is_enable>',
              help='enable firewall rule')
@click.option('--policy',
              'policy',
              default='drop',
              metavar='<policy>',
              help='policy on firewall rule')
@click.option('--protocols',
              'protocols',
              default=None,
              metavar='<protocols>',
              help='all protocol names in comma separated format')
@click.option('--source-port-range',
              'source_port_range',
              default='Any',
              metavar='<source_port_range>',
              help='source port range on firewall rule')
@click.option('--source-ip',
              'source_ip',
              default='Any',
              metavar='<source_ip>',
              help='source ip on firewall rule')
@click.option('--destination-port-range',
              'destination_port_range',
              default='Any',
              metavar='<destination_port_range>',
              help='destination port range on firewall rule')
@click.option('--destination-ip',
              'destination_ip',
              default='Any',
              metavar='<destination_ip>',
              help='destination ip on firewall rule')
@click.option('--enable-logging/--disable-logging',
              'is_logging',
              default=True,
              metavar='<is_logging>',
              help='enable logging on firewall rule')
def add_firewall_rule(ctx, vapp_name, network_name, firewall_rule_name,
                      is_enable, policy, protocols, source_port_range,
                      source_ip, destination_port_range, destination_ip,
                      is_logging):
    try:
        protocol_list = ['Any']
        if protocols is not None:
            protocol_list = protocols.split(',')
        vapp_firewall = get_vapp_network_firewall(ctx, vapp_name, network_name)
        result = vapp_firewall.add_firewall_rule(
            name=firewall_rule_name,
            is_enabled=is_enable,
            policy=policy,
            protocols=protocol_list,
            source_port_range=source_port_range,
            source_ip=source_ip,
            destination_port_range=destination_port_range,
            destination_ip=destination_ip,
            enable_logging=is_logging)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command('list', short_help='list firewall rules in firewall service')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
def list_firewall_rule(ctx, vapp_name, network_name):
    try:
        vapp_firewall = get_vapp_network_firewall(ctx, vapp_name, network_name)
        result = vapp_firewall.list_firewall_rule()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command('update',
                  short_help='update firewall rule of firewall service')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.argument('firewall_rule_name',
                metavar='<firewall-rule-name>',
                required=True)
@click.option('--name',
              'new_name',
              default=None,
              metavar='<new_name>',
              help='new name of firewall rule')
@click.option('--enable/--disable',
              'is_enable',
              default=None,
              metavar='<is_enable>',
              help='enable firewall rule')
@click.option('--policy',
              'policy',
              default=None,
              metavar='<policy>',
              help='policy on firewall rule')
@click.option('--protocols',
              'protocols',
              default=None,
              metavar='<protocols>',
              help='all protocol names in comma separated format')
@click.option('--source-port-range',
              'source_port_range',
              default=None,
              metavar='<source_port_range>',
              help='source port range on firewall rule')
@click.option('--source-ip',
              'source_ip',
              default=None,
              metavar='<source_ip>',
              help='source ip on firewall rule')
@click.option('--destination-port-range',
              'destination_port_range',
              default=None,
              metavar='<destination_port_range>',
              help='destination port range on firewall rule')
@click.option('--destination-ip',
              'destination_ip',
              default=None,
              metavar='<destination_ip>',
              help='destination ip on firewall rule')
@click.option('--enable-logging/--disable-logging',
              'is_logging',
              default=None,
              metavar='<is_logging>',
              help='enable logging on firewall rule')
def update_firewall_rule(ctx, vapp_name, network_name, firewall_rule_name,
                         new_name, is_enable, policy, protocols,
                         source_port_range, source_ip, destination_port_range,
                         destination_ip, is_logging):
    try:
        protocol_list = None
        if protocols is not None:
            protocol_list = protocols.split(',')
        vapp_firewall = get_vapp_network_firewall(ctx, vapp_name, network_name)
        result = vapp_firewall.update_firewall_rule(
            name=firewall_rule_name,
            new_name=new_name,
            is_enabled=is_enable,
            policy=policy,
            protocols=protocol_list,
            source_port_range=source_port_range,
            source_ip=source_ip,
            destination_port_range=destination_port_range,
            destination_ip=destination_ip,
            enable_logging=is_logging)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@firewall.command('delete',
                  short_help='delete firewall rule in firewall service')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp-name>', required=True)
@click.argument('network_name', metavar='<network-name>', required=True)
@click.argument('firewall_rule_name',
                metavar='<firewall-rule-name>',
                required=True)
def delete_firewall_rule(ctx, vapp_name, network_name, firewall_rule_name):
    try:
        vapp_firewall = get_vapp_network_firewall(ctx, vapp_name, network_name)
        result = vapp_firewall.delete_firewall_rule(firewall_rule_name)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
