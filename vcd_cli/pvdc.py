# VMware vCloud Director CLI
#
# Copyright (c) 2017-2018 VMware, Inc. All Rights Reserved.
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
from pyvcloud.vcd.platform import Platform
from pyvcloud.vcd.pvdc import PVDC
from pyvcloud.vcd.system import System
from pyvcloud.vcd.utils import pvdc_to_dict

from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import vcd


@vcd.group(short_help='work with provider virtual datacenters')
@click.pass_context
def pvdc(ctx):
    """Work with provider virtual datacenters in vCloud Director.

\b
    Examples
        vcd pvdc list
            Get list of provider virtual datacenters.
\b
        vcd pvdc info name
            Display provider virtual data center details.
\b
        vcd pvdc create pvdc-name vc-name
            --storage-profile 'sp1'
            --storage-profile 'sp2'
            --resource-pool 'rp1'
            --resource-pool 'rp2'
            --vxlan-network-pool 'vnp1'
            --highest-supported-hw-version 'vmx-11'
            --description 'description'
            --enable
                Create Provider Virtual Datacenter.
                   Parameters --storage-profile and --resource-pool are both
                   required parameters and each can have multiple entries.
    """
    pass


@pvdc.command('list', short_help='list of provider virtual datacenters')
@click.pass_context
def list_pvdc(ctx):
    try:
        restore_session(ctx)
        client = ctx.obj['client']
        sys_admin_resource = client.get_admin()
        system = System(client, admin_resource=sys_admin_resource)
        result = []
        for pvdc in system.list_provider_vdcs():
            result.append({'name': pvdc.get('name')})
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@pvdc.command('info', short_help='show pvdc details')
@click.pass_context
@click.argument('name', metavar='<name>')
def info_pvdc(ctx, name):
    try:
        restore_session(ctx)
        client = ctx.obj['client']
        sys_admin_resource = client.get_admin()
        system = System(client, admin_resource=sys_admin_resource)
        pvdc_reference = system.get_provider_vdc(name)
        pvdc = PVDC(client, href=pvdc_reference.get('href'))
        refs = pvdc.get_vdc_references()
        md = pvdc.get_metadata()
        result = pvdc_to_dict(pvdc.get_resource(), refs, md)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@pvdc.command('create', short_help='create pvdc')
@click.pass_context
@click.argument('pvdc-name', metavar='<pvdc-name>', required=True)
@click.argument('vc-name', metavar='<vc-name>', required=True)
@click.option(
    '-s',
    '--storage-profile',
    required=True,
    default=None,
    multiple=True,
    help='storage profile name (required parameter, can have multiple)')
@click.option(
    '-r',
    '--resource-pool',
    required=True,
    default=None,
    multiple=True,
    help='resource pool name (required parameter, can have multiple)')
@click.option(
    '-n',
    '--vxlan-network-pool',
    required=False,
    default=None,
    metavar='[vxlan-network-pool]',
    help='vxlan network pool name')
@click.option(
    '-d',
    '--description',
    required=False,
    default=None,
    metavar='[description]',
    help='description of PVDC')
@click.option(
    '-e',
    '--enable',
    is_flag=True,
    default=None,
    metavar='[enable]',
    help='enable flag (enables PVDC when it is created)')
@click.option(
    '-v',
    '--highest-supp-hw-vers',
    required=False,
    default=None,
    metavar='[highest-supp-hw-vers]',
    help='highest supported hw version, e.g. vmx-11, vmx-10, vmx-09, etc.')
def create(ctx, vc_name, resource_pool, storage_profile, pvdc_name,
           enable, description, highest_supp_hw_vers,
           vxlan_network_pool):
    try:
        restore_session(ctx)
        client = ctx.obj['client']
        platform = Platform(client)
        platform.create_provider_vdc(vim_server_name=vc_name,
                                     resource_pool_names=resource_pool,
                                     storage_profiles=storage_profile,
                                     pvdc_name=pvdc_name,
                                     is_enabled=enable,
                                     description=description,
                                     highest_supp_hw_vers=highest_supp_hw_vers,
                                     vxlan_network_pool=vxlan_network_pool)
        stdout('PVDC created successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)
