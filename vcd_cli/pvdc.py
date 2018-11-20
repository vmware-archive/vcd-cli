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
from pyvcloud.vcd.client import NSMAP
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
        vcd pvdc create pvdc-name vc-name \\
                --storage-profile 'sp1' \\
                --storage-profile 'sp2' \\
                --resource-pool 'rp1' \\
                --resource-pool 'rp2' \\
                --vxlan-network-pool 'vnp1' \\
                --nsxt-manager-name 'nsx-t manager name' \\ (API version 31.0)
                --highest-supp-hw-vers 'vmx-11' \\
                --description 'description' \\
                --enable
            Create Provider Virtual Datacenter.
                Parameters --storage-profile and --resource-pool are both
                required parameters and each can have multiple entries.
\b
        vcd pvdc attach-rp pvdc-name rp1 rp2 ... (one or more rp names)
            Attach one or more resource pools to a Provider vDC.
\b
        vcd pvdc detach-rp pvdc-name rp1 rp2 ... (one or more rp names)
            Detach one or more resource pools from a Provider vDC.
\b
        Caveat: The current implementation of the attach-rp and detach-rp
        functions take a list of RP "basenames" as input. A basename is the
        last element of a full pathname. For example, given a pathname /a/b/c,
        the basename of that pathname is "c". Since RP names are only required
        to have unique pathnames but not unique basenames, this function may
        not work correctly if there are non-unique RP basenames. Therefore, in
        order to use these functions, all RP basenames must be unique. It is
        up to the user of these functions to be aware of this limitation and
        name their RPs appropriately. This limitation will be fixed in a future
        version of these functions.
\b
        vcd pvdc add-sp pvdc-name sp1 sp2 ... (one or more storage profiles)
            Add one or more storage profiles to a Provider vDC.
\b
        vcd pvdc del-sp pvdc-name sp1 sp2 ... (one or more storage profiles)
            Delete one or more storage profiles from a Provider vDC.
\b
        vcd pvdc migrate-vms pvdc-name rp1 vm1 vm2 ... --target-rp rp2
            Migrate one or more VMs from the source resource pool (rp1)
            to the target-rp (rp2 in this example, which is the target
            resource pool, an optional parameter). If the target-rp isn't
            specified, any available resource pool is chosen automatically.
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


def _pvdc_helper(ctx):
    client = ctx.obj['client']
    platform = Platform(client)
    return client, platform


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
    '-t',
    '--nsxt-manager-name',
    required=False,
    default=None,
    metavar='[nsxt-manager-name]',
    help='nsx-t manager name (valid for vCD API version 31.0 and above)')
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
           enable, description, highest_supp_hw_vers, vxlan_network_pool,
           nsxt_manager_name):
    try:
        restore_session(ctx)
        client, platform = _pvdc_helper(ctx)
        pvdc = \
            platform.create_provider_vdc(vim_server_name=vc_name,
                                         resource_pool_names=resource_pool,
                                         storage_profiles=storage_profile,
                                         pvdc_name=pvdc_name,
                                         is_enabled=enable,
                                         description=description,
                                         highest_hw_vers=highest_supp_hw_vers,
                                         vxlan_network_pool=vxlan_network_pool,
                                         nsxt_manager_name=nsxt_manager_name)
        stdout(pvdc.find('vcloud:Tasks', NSMAP).Task[0], ctx)
        stdout('PVDC created successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@pvdc.command('attach-rp', short_help='attach resource pools to a pvdc')
@click.pass_context
@click.argument('pvdc-name', metavar='<pvdc-name>', required=True)
@click.argument('respool', nargs=-1, metavar='<respool>', required=True)
def attach_rp(ctx, pvdc_name, respool):
    try:
        restore_session(ctx)
        client, platform = _pvdc_helper(ctx)
        task = platform.attach_resource_pools_to_provider_vdc(
            pvdc_name=pvdc_name,
            resource_pool_names=respool)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@pvdc.command('detach-rp', short_help='detach resource pools from a pvdc')
@click.pass_context
@click.argument('pvdc-name', metavar='<pvdc-name>', required=True)
@click.argument('respool', nargs=-1, metavar='<respool>', required=True)
def detach_rp(ctx, pvdc_name, respool):
    try:
        restore_session(ctx)
        client, platform = _pvdc_helper(ctx)
        task = platform.detach_resource_pools_from_provider_vdc(
            pvdc_name=pvdc_name,
            resource_pool_names=respool)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@pvdc.command('add-sp', short_help='add storage profiles to a pvdc')
@click.pass_context
@click.argument('pvdc-name', metavar='<pvdc-name>', required=True)
@click.argument('storage-profile', nargs=-1, metavar='<storage-profile>',
                required=True)
def add_sp(ctx, pvdc_name, storage_profile):
    try:
        restore_session(ctx)
        client, platform = _pvdc_helper(ctx)
        task = platform.pvdc_add_storage_profile(
            pvdc_name=pvdc_name,
            storage_profile_names=storage_profile)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@pvdc.command('del-sp', short_help='delete storage profiles from a pvdc')
@click.pass_context
@click.argument('pvdc-name', metavar='<pvdc-name>', required=True)
@click.argument('storage-profile', nargs=-1, metavar='<storage-profile>',
                required=True)
def del_sp(ctx, pvdc_name, storage_profile):
    try:
        restore_session(ctx)
        client, platform = _pvdc_helper(ctx)
        task = platform.pvdc_del_storage_profile(
            pvdc_name=pvdc_name,
            storage_profile_names=storage_profile)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@pvdc.command('migrate-vms', short_help='migrate vms to another resource pool')
@click.pass_context
@click.argument('pvdc-name', metavar='<pvdc-name>', required=True)
@click.argument('source-rp', metavar='<source-rp>', required=True)
@click.argument('vm-name', nargs=-1, metavar='<vm-name>', required=True)
@click.option(
    '-t',
    '--target-rp',
    required=False,
    default=None,
    metavar='[target-rp]',
    help='target resource pool name')
def migrate_vms(ctx, pvdc_name, source_rp, vm_name, target_rp):
    try:
        restore_session(ctx)
        client, platform = _pvdc_helper(ctx)
        task = platform.pvdc_migrate_vms(
            pvdc_name=pvdc_name,
            vms_to_migrate=vm_name,
            src_resource_pool=source_rp,
            target_resource_pool=target_rp)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)
