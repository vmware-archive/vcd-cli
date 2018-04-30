# VMware vCloud Director CLI
#
# Copyright (c) 2018 VMware, Inc. All Rights Reserved.
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
from pyvcloud.vcd.client import NSMAP
from pyvcloud.vcd.platform import Platform

from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import vcd


@vcd.group(short_help='manage vCenter Servers')
@click.pass_context
def vc(ctx):
    """Manage vCenter Servers in vCloud Director.

\b
    Examples
        vcd vc list
            Get list of vCenter Servers attached to the vCD system.
\b
        vcd vc info vc1
            Get details of the vCenter Server 'vc1' attached to the vCD system.
\b
        vcd vc attach vc-name
            --vc-host 'vc.server.example.com' (or something similar)
            --vc-user 'vc-admin-user-name'
            --vc-pwd 'vc-admin-user-password'
            --vc-root-folder 'vc-root-folder' (for VCD API version 31.0)
            --nsx-server-name 'nsx-server-namespace'
            --nsx-host 'nsx.server.example.com' (or something similar)
            --nsx-user 'nsx-admin-user-name'
            --nsx-pwd 'nsx-admin-password'
            --enable
                Attaches Virtual Center (VC) server with the given
                credentials to vCD.
    """
    pass


@vc.command('list', short_help='list vCenter Servers')
@click.pass_context
def list_vcenters(ctx):
    try:
        restore_session(ctx)
        platform = Platform(ctx.obj['client'])
        stdout(platform.list_vcenters(), ctx)
    except Exception as e:
        stderr(e, ctx)


@vc.command(short_help='show vCenter details')
@click.pass_context
@click.argument('name')
def info(ctx, name):
    try:
        restore_session(ctx)
        platform = Platform(ctx.obj['client'])
        stdout(platform.get_vcenter(name), ctx)
    except Exception as e:
        stderr(e, ctx)


@vc.command('attach', short_help='attach vCenter Server')
@click.pass_context
@click.argument('vc-name', metavar='<vc-name>', required=True)
@click.option(
    '--vc-host',
    required=True,
    default=None,
    metavar='[vc-host]',
    help='vc host name (vc.server.example.com, or something similar)')
@click.option(
    '--vc-user',
    required=True,
    default=None,
    metavar='[vc-user]',
    help='VC admin user name')
@click.option(
    '--vc-pwd',
    required=True,
    default=None,
    metavar='[vc-pwd]',
    help='VC admin password')
@click.option(
    '--vc-root-folder',
    required=False,
    default=None,
    metavar='[vc-root-folder]',
    help='VC root folder (for a future release - VCD API version 31.0)')
@click.option(
    '--nsx-server-name',
    required=False,
    default=None,
    metavar='[nsx-server-name]',
    help='NSX server name')
@click.option(
    '--nsx-host',
    required=False,
    default=None,
    metavar='[nsx-host]',
    help='NSX host name (nsx.server.example.com, or something similar)')
@click.option(
    '--nsx-user',
    required=False,
    default=None,
    metavar='[nsx-user]',
    help='NSX admin user name')
@click.option(
    '--nsx-pwd',
    required=False,
    default=None,
    metavar='[nsx-pwd]',
    help='NSX admin password')
@click.option(
    '-e',
    '--enable',
    is_flag=True,
    default=None,
    metavar='[enable]',
    help='enable flag (enables VC when it is attached to vCD)')
def attach(ctx, vc_name, vc_host, vc_user, vc_pwd, vc_root_folder,
           nsx_server_name, nsx_host, nsx_user, nsx_pwd, enable):
    try:
        restore_session(ctx)
        client = ctx.obj['client']
        platform = Platform(client)
        result = platform.attach_vcenter(vc_server_name=vc_name,
                                         vc_server_host=vc_host,
                                         vc_admin_user=vc_user,
                                         vc_admin_pwd=vc_pwd,
                                         vc_root_folder=vc_root_folder,
                                         nsx_server_name=nsx_server_name,
                                         nsx_host=nsx_host,
                                         nsx_admin_user=nsx_user,
                                         nsx_admin_pwd=nsx_pwd,
                                         is_enabled=enable)
        vc = result.find('vmext:VimServer', NSMAP)
        Tasks = vc.find('vcloud:Tasks', NSMAP)
        stdout(Tasks.Task[0], ctx)
        stdout('VirtualCenter server attached successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)
