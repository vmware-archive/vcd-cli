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
from pyvcloud.vcd.ipsec_vpn import IpsecVpn
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
# Don't change the order of vcd  and gateway
from vcd_cli.vcd import vcd  # NOQA
from vcd_cli.gateway import gateway  # NOQA
from vcd_cli.gateway import get_gateway
from vcd_cli.gateway import services


@services.group('ipsec-vpn', short_help='Manage ipsec vpn of gateway')
@click.pass_context
def ipsec_vpn(ctx):
    """Manages IPsec VPN of gateway.

    \b
        Examples
            vcd gateway services ipsec-vpn create test_gateway1
                    --name name
                    --local-id lid1
                    --local-ip 2.2.3.2
                    --peer-id pid1
                    --peer-ip 2.2.3.4
                    --local-subnet 30.20.10.0/24
                    --peer-subnet 10.20.10.0/24
                    --desc "IPsec VPN"
                    --psk abcd1234
                    --enable
                Creates new IPsec VPN.

    \b
            vcd gateway services ipsec-vpn update test_gateway1 2.2.3.2-2.2.3.3
                    --new-name new_name
                    --enable
                Updates IPsec VPN with new values.

    \b
            vcd gateway services ipsec-vpn enable-activation-status test_gateway1
                    --enable
                Enable/disable activation status.

    \b
            vcd gateway services ipsec-vpn info-activation-status test_gateway1
                Info activation status.

    \b
            vcd gateway services ipsec-vpn enable-logging test_gateway1
                    --enable
                Enable/disable logging.

    \b
            vcd gateway services ipsec-vpn info-logging-settings test_gateway1
                Info logging settings.

    \b
            vcd gateway services ipsec-vpn set-log-level test_gateway1 warning
                Set global log level for IPsec VPN.

    \b
            vcd gateway services ipsec-vpn list test_gateway1
                List IPsec VPN of a gateway.

    \b
            vcd gateway services ipsec-vpn change-shared-key test_gateway1
                    new_shared_key
                Change shared key of IPsec VPN.

    \b
            vcd gateway services ipsec-vpn info test_gateway1
                    2.2.3.2-2.2.3.3
                Get details of IPsec VPN.

    \b
            vcd gateway services ipsec-vpn delete test_gateway1 2.2.3.2-2.2.3.3
                Deletes IPsec VPN.

    """
    __DEFAULT_ENCRYPTION_PROTOCOL = 'aes'
    __DEFAULT_AUTHENTICATION_MODE = 'psk'
    __DEFAULT_DH_GROUP = 'dh5'
    __DEFAULT_MTU = '1500'
    __DEFAULT_IP_SEC_ENABLE = True
    __DEFAULT_ENABLE_PFS = False


@ipsec_vpn.command("create", short_help="create new IPsec VPN")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.option(
    '--name',
    'name',
    required=True,
    metavar='<IPsec VPN name>',
    help='IPsec VPN name')
@click.option(
    '-lid',
    '--local-id',
    'local_id',
    required=True,
    metavar='<local-id>',
    help='Local id of IPsec VPN.')
@click.option(
    '-pid',
    '--peer-id',
    'peer_id',
    required=True,
    metavar='<peer-id>',
    help='Peer id of IPsec VPN.')
@click.option(
    '-lip',
    '--local-ip',
    'local_ip',
    required=True,
    metavar='<local-ip>',
    help='Local IP/Local end point of IPsec VPN.')
@click.option(
    '-pip',
    '--peer-ip',
    'peer_ip',
    required=True,
    metavar='<peer-ip>',
    help='Peer IP/Peer end point of IPsec VPN.')
@click.option(
    '-lsubnet',
    '--local-subnet',
    'local_subnet',
    required=True,
    metavar='<local-subnet>',
    help='Local subnets of IPsec VPN.These should be given comma separated.')
@click.option(
    '-psubnet',
    '--peer-subnet',
    'peer_subnet',
    required=True,
    metavar='<peer-subnet>',
    help='Peer subnets of IPsec VPN.These should be given comma separated.')
@click.option(
    '-psk',
    '--pre-shared-key',
    'pre_shared_key',
    required=True,
    metavar='<pre-shared-key>',
    help='Pre shared key of IPsec VPN.')
@click.option(
    '--description',
    'description',
    default=None,
    metavar='<description>',
    help='Description of IPsec VPN.')
@click.option(
    '--encryption-protocol',
    'encryption_protocol',
    default='aes',
    metavar='<encryption protocol>',
    help='encryption protocol of IPsec VPN.')
@click.option(
    '--authentication-mode',
    'authentication_mode',
    default='psk',
    metavar='<authentication_mode>',
    help='authentication_mode of IPsec VPN.')
@click.option(
    '--dh-group',
    'dh_group',
    default='dh5',
    metavar='<dh group>',
    help='dh group for IPsec VPN.')
@click.option(
    '--mtu',
    'mtu',
    default='1500',
    metavar='<mtu>',
    help='mtu for IPsec VPN.')
@click.option(
    '--enable/--disable',
    'enabled',
    default=False,
    metavar='<bool>',
    is_flag=True,
    help='enable/disable IPsec VPN')
@click.option(
    '--enable_pfs/--disable_pfs',
    'enable_pfs',
    default=False,
    metavar='<bool>',
    is_flag=True,
    help='enable/disable PFS of IPsec VPN')
def create_ipsec_vpn(ctx, gateway_name, name, local_id, peer_id, local_ip,
                     peer_ip, local_subnet, peer_subnet, pre_shared_key,
                     description, encryption_protocol, authentication_mode,
                     dh_group, mtu, enabled, enable_pfs):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        gateway_resource.add_ipsec_vpn(name=name,
                                       peer_id=peer_id,
                                       peer_ip_address=peer_ip,
                                       local_id=local_id,
                                       local_ip_address=local_ip,
                                       local_subnet=local_subnet,
                                       peer_subnet=peer_subnet,
                                       shared_secret_encrypted=pre_shared_key,
                                       encryption_protocol=encryption_protocol,
                                       authentication_mode=authentication_mode,
                                       dh_group=dh_group,
                                       mtu=mtu,
                                       description=description,
                                       is_enabled=enabled,
                                       enable_pfs=enable_pfs)
        stdout('IPsec VPN created successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@ipsec_vpn.command("update", short_help="update IPsec VPN")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.argument('id', metavar='<local end point-peer end point>', required=True)
@click.option(
    '--new-name',
    'name',
    metavar='<IPsec VPN name>',
    help='IPsec VPN name')
@click.option(
    '-lid',
    '--local-id',
    'local_id',
    metavar='<local-id>',
    help='Local id of IPsec VPN.')
@click.option(
    '-pid',
    '--peer-id',
    'peer_id',
    metavar='<peer-id>',
    help='Peer id of IPsec VPN.')
@click.option(
    '-lip',
    '--local-ip',
    'local_ip',
    metavar='<local-ip>',
    help='Local IP/Local end point of IPsec VPN.')
@click.option(
    '-pip',
    '--peer-ip',
    'peer_ip',
    metavar='<peer-ip>',
    help='Peer IP/Peer end point of IPsec VPN.')
@click.option(
    '-lsubnet',
    '--local-subnet',
    'local_subnet',
    metavar='<local-subnet>',
    help='Local subnets of IPsec VPN.These should be given comma separated.')
@click.option(
    '-psubnet',
    '--peer-subnet',
    'peer_subnet',
    metavar='<peer-subnet>',
    help='Peer subnets of IPsec VPN.These should be given comma separated.')
@click.option(
    '-psk',
    '--pre-shared-key',
    'pre_shared_key',
    metavar='<pre-shared-key>',
    help='Pre shared key of IPsec VPN.')
@click.option(
    '--description',
    'description',
    metavar='<description>',
    help='Description of IPsec VPN.')
@click.option(
    '--encryption-protocol',
    'encryption_protocol',
    metavar='<encryption protocol>',
    help='encryption protocol of IPsec VPN.')
@click.option(
    '--authentication-mode',
    'authentication_mode',
    metavar='<authentication_mode>',
    help='authentication_mode of IPsec VPN.')
@click.option(
    '--dh-group',
    'dh_group',
    metavar='<dh group>',
    help='dh group for IPsec VPN.')
@click.option(
    '--mtu',
    'mtu',
    metavar='<mtu>',
    help='mtu for IPsec VPN.')
@click.option(
    '--enable/--disable',
    'enabled',
    metavar='<bool>',
    is_flag=True,
    help='enable/disable IPsec VPN')
@click.option(
    '--enable_pfs/--disable_pfs',
    'enable_pfs',
    metavar='<bool>',
    is_flag=True,
    help='enable/disable PFS of IPsec VPN')
def update_ipsec_vpn(ctx, gateway_name, id, name, local_id, peer_id, local_ip,
                     peer_ip, local_subnet, peer_subnet, pre_shared_key,
                     description, encryption_protocol, authentication_mode,
                     dh_group, mtu, enabled, enable_pfs):
    try:
        ipsec_vpn_obj = get_ipsec_vpn(ctx, gateway_name, id)
        ipsec_vpn_obj.update_ipsec_vpn(name=name,
                                       peer_id=peer_id,
                                       peer_ip_address=peer_ip,
                                       local_id=local_id,
                                       local_ip_address=local_ip,
                                       local_subnet=local_subnet,
                                       peer_subnet=peer_subnet,
                                       shared_secret_encrypted=pre_shared_key,
                                       encryption_protocol=encryption_protocol,
                                       authentication_mode=authentication_mode,
                                       dh_group=dh_group,
                                       mtu=mtu,
                                       description=description,
                                       is_enabled=enabled,
                                       enable_pfs=enable_pfs)
        stdout('IPsec VPN updated successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@ipsec_vpn.command("delete", short_help="Deletes the IPsec VPN")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.argument('id', metavar='<local end point-peer end point>', required=True)
def delete_ipsec_vpn(ctx, gateway_name, id):
    try:
        ipsec_vpn_obj = get_ipsec_vpn(ctx, gateway_name, id)
        ipsec_vpn_obj.delete_ipsec_vpn()
        stdout('IPsec VPN deleted successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@ipsec_vpn.command("enable-activation-status",
                   short_help="enable activation status")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.option(
    '--enable/--disable',
    'enabled',
    default=False,
    metavar='<bool>',
    is_flag=True,
    help='enable/disable IPsec VPN')
def enable_activation_status(ctx, gateway_name, enabled):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        gateway_resource.enable_activation_status_ipsec_vpn(enabled)
        stdout('IPsec VPN activation status changed.', ctx)
    except Exception as e:
        stderr(e, ctx)


@ipsec_vpn.command("info-activation-status",
                   short_help="info activation status")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
def info_activation_status(ctx, gateway_name):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        result = gateway_resource.info_activation_status_ipsec_vpn()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@ipsec_vpn.command("enable-logging",
                   short_help="enable logging of IPsec VPN.")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.option(
    '--enable/--disable',
    'enabled',
    default=False,
    metavar='<bool>',
    is_flag=True,
    help='enable/disable global logging of IPsec VPN')
def enable_logging(ctx, gateway_name, enabled):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        gateway_resource.enable_logging_ipsec_vpn(enabled)
        stdout('IPsec VPN logging enable status changed.', ctx)
    except Exception as e:
        stderr(e, ctx)


@ipsec_vpn.command("info-logging-settings",
                   short_help="info logging settings")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
def info_logging_settings(ctx, gateway_name):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        result = gateway_resource.info_logging_settings_ipsec_vpn()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@ipsec_vpn.command("set-log-level",
                   short_help="set log level of IPsec VPN. It's value should be"
                              " from the domain:{emergency, alert, critical, "
                              "error, warning, notice, info, debug)")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.argument('log_level', metavar='<log level>', required=True)
def set_log_level(ctx, gateway_name, log_level):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        gateway_resource.set_log_level_ipsec_vpn(log_level)
        stdout('IPsec VPN log level changed.', ctx)
    except Exception as e:
        stderr(e, ctx)


@ipsec_vpn.command("list",
                   short_help="list ipsec vpn")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
def list_ipsec_vpn(ctx, gateway_name):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        result = gateway_resource.list_ipsec_vpn()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@ipsec_vpn.command("change-shared-key", short_help="change shared key")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.argument('new_shared_key', metavar='<new shared key>', required=True)
def change_shared_key(ctx, gateway_name, new_shared_key):
    try:
        gateway_resource = get_gateway(ctx, gateway_name)
        gateway_resource.change_shared_key_ipsec_vpn(new_shared_key)
        stdout('IPsec VPN shared key changed.', ctx)
    except Exception as e:
        stderr(e, ctx)


@ipsec_vpn.command("info", short_help="get details of ipsec vpn")
@click.pass_context
@click.argument('gateway_name', metavar='<gateway name>', required=True)
@click.argument('id', metavar='<local end point-peer end point>', required=True)
def info_ipsec_vpn(ctx, gateway_name, id):
    try:
        ipsec_vpn_obj = get_ipsec_vpn(ctx, gateway_name, id)
        result = ipsec_vpn_obj.get_vpn_site_info()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


def get_ipsec_vpn(ctx, gateway_name, id):
    """Get the sdk's ipsec vpn object.

    It will restore sessions if expired. It will read the client.
    """
    restore_session(ctx, vdc_required=True)
    client = ctx.obj['client']
    ipsec_vpn = IpsecVpn(client=client,
                         gateway_name=gateway_name,
                         ipsec_end_point=id)
    return ipsec_vpn
