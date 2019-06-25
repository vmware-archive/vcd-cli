# VMware vCloud Director CLI
#
# Copyright (c) 2014-2018 VMware, Inc. All Rights Reserved.
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

import os
import click
from pyvcloud.vcd.client import ApiVersion
from pyvcloud.vcd.client import EntityType
from pyvcloud.vcd.client import get_links
from pyvcloud.vcd.client import ResourceType
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.utils import access_settings_to_dict
from pyvcloud.vcd.utils import to_dict
from pyvcloud.vcd.utils import vapp_to_dict
from pyvcloud.vcd.vapp import VApp
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.vm import VM

from vcd_cli.utils import access_settings_to_list
from vcd_cli.utils import acl_str_to_list_of_dict
from vcd_cli.utils import extract_name_and_id
from vcd_cli.utils import is_sysadmin
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import abort_if_false
from vcd_cli.vcd import vcd


@vcd.group(short_help='manage vApps')
@click.pass_context
def vapp(ctx):
    """Manage vApps in vCloud Director.

\b
    Description
        The vapp command manages vApps.

\b
        'vapp create' creates a new vApp in the current vDC. When '--catalog'
        and '--template' are not provided, it creates an empty vApp and VMs can
        be added later. When specifying a template in a catalog, it creates an
        instance of the catalog template.

\b
        'vapp add-vm' adds a VM to the vApp. When '--catalog' is used, the
        <source-vapp> parameter refers to a template in the specified catalog
        and the command will instantiate the <source-vm> found in the template.
        If '--catalog' is not used, <source-vapp> refers to another vApp in the
        vDC and the command will copy the <source-vm> found in the vApp. The
        name of the VM and other options can be customized when the VM is added
        to the vApp.

\b
    Examples
        vcd vapp list
            Get list of vApps in current virtual datacenter.

\b
        vcd vapp list vapp1
            Get list of VMs in vApp 'vapp1'.

\b
        vcd vapp list --filter name==vapp1
            Get list of vApp with name vapp1.

\b
        vcd vapp list --filter ownerName==user1
            Get list of vApp with ownername 'user1'.

\b
        vcd vapp list --filter numberOfVMs==7
            Get list of vApp with numberOfVMs 7.

\b
        vcd vapp list --filter vdcName==ovdc1
            Get list of vApp with vdcName 'ovdc1'.

\b
        vcd vapp info vapp1
            Get details of the vApp 'vapp1'.

\b
        vcd vapp create vapp1
            Create an empty vApp with name 'vapp1'.

\b
        vcd vapp create vapp1 --network net1
            Create an empty vApp connected to a network.

\b
        vcd vapp create vapp1 -c catalog1 -t template1
            Instantiate a vApp from a catalog template.

\b
        vcd vapp create vapp1 -c catalog1 -t template1
                 --cpu 4 --memory 4096 --disk-size 20000
                 --network net1 --ip-allocation-mode pool
                 --hostname myhost --vm-name vm1 --accept-all-eulas
                 --storage-profile '*'
            Instantiate a vApp with customized settings.

\b
        vcd vapp update vapp1 -n vapp-new-name -d "new description"
            Updates vApp name and description.

\b
        vcd vapp delete vapp1 --yes --force
            Delete a vApp.

\b
        vcd --no-wait vapp delete vapp1 --yes --force
            Delete a vApp without waiting for completion.

\b
        vcd vapp update-lease vapp1 7776000
            Set vApp lease to 90 days.

\b
        vcd vapp update-lease vapp1 0
            Set vApp lease to no expiration.

\b
        vcd vapp shutdown vapp1 --yes
            Gracefully shutdown a vApp.

\b
        vcd vapp reboot vapp1 --yes
            Reboot a vApp.

\b
        vcd vapp power-off vapp1
            Power off a vApp.

\b
        vcd vapp power-off vapp1 vm1 vm2
            Power off vm1 and vm2 of vapp1.

\b
        vcd vapp reset vapp1 vm1 vm2
            Power reset vm1 and vm2 of vapp1.

\b
        vcd vapp deploy vapp1 vm1 vm2
            Deploy vm1 and vm2 of vapp1.

\b
        vcd vapp undeploy vapp1 vm1 vm2
            Undeploy vm1 and vm2 of vapp1.

\b
        vcd vapp stop vapp1
            stop a vApp.

\b
        vcd vapp delete vapp1 vm1 vm2
            Delete vm1 and vm2 from vapp1.

\b
        vcd vapp reboot vapp1 vm1 vm2 --yes
            Reboot vm1 and vm2 in vApp.

\b
        vcd vapp shutdown vapp1 vm1 vm2 --yes
            Shutdown vm1 and vm2 in vApp.

\b
        vcd vapp power-on vapp1
            Power on a vApp.

\b
        vcd vapp reset vapp1
            Power reset vapp1.

\b
        vcd vapp deploy vapp1
            Deploy vapp1.

\b
        vcd vapp power-on vapp1 vm1 vm2
            Power on vm1 and vm2 of vapp1.

\b
        vcd vapp capture vapp1 catalog1
            Capture a vApp as a template in a catalog.

\b
        vcd vapp download vapp1 file.ova
            Download a vapp.

\b
        vcd vapp attach vapp1 vm1 disk1
            Attach a disk to a VM in the given vApp.

\b
        vcd vapp detach vapp1 vm1 disk1
            Detach a disk from a VM in the given vApp.

\b
        vcd vapp add-disk vapp1 vm1 10000
            Add a disk of 10000 MB to a VM.

\b
        vcd vapp add-vm vapp1 template1.ova vm1 -c catalog1
            Add a VM to a vApp. Instantiate the source VM \'vm1\' that is in
            the \'template1.ova\' template in the \'catalog1\' catalog and
            place the new VM inside \'vapp1\' vApp.

\b
        vdc vapp connect vapp1 org-vdc-network1
            Connects the network org-vdc-network1 to vapp1.

\b
        vdc vapp disconnect vapp1 org-vdc-network1
            Disconnects the network org-vdc-network1 from vapp1.

\b
        vcd vapp suspend vapp1
            Suspend a vapp.

\b
        vcd vapp discard-suspended-state vapp1
            Discard suspended state of vapp.

\b
        vcd vapp enter-maintenance-mode vapp1
            Place a vApp in Maintenance Mode.

\b
        vcd vapp exit-maintenance-mode vapp1
            Exit maintenance mode a vapp.

\b
        vcd vapp upgrade-virtual-hardware vapp1
            Upgrade virtual hardware of vapp.

\b
        vcd vapp copy vapp1 -n new_vapp_name -v target_vdc -d description
            Copy a vapp to target vdc.

\b
        vcd vapp move vapp1 -v target_vdc
            Move a vapp to target vdc.

\b
        vcd vapp create-snapshot vapp1
            Create snapshot of the vapp.

\b
        vcd vapp revert-to-snapshot vapp1
            Revert to to current snapshot of the vapp.

\b
        vcd vapp remove-snapshot vapp1
            Remove snapshot of the vapp.
    """
    pass


@vapp.command(short_help='show vApp details')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
def info(ctx, name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(name)
        vapp = VApp(client, resource=vapp_resource)
        md = vapp.get_metadata()
        access_control_settings = vapp.get_access_settings()
        result = vapp_to_dict(vapp_resource, md,
                              access_settings_to_dict(access_control_settings))
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command(short_help='attach disk to VM in vApp')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.argument('disk-name', metavar='<disk-name>', required=True)
def attach(ctx, vapp_name, vm_name, disk_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)

        disk_name, disk_id = extract_name_and_id(disk_name)
        disk = vdc.get_disk(name=disk_name, disk_id=disk_id)

        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)

        task = vapp.attach_disk_to_vm(
            disk_href=disk.get('href'), vm_name=vm_name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command(short_help='detach disk from VM in vApp')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.argument('disk-name', metavar='<disk-name>', required=True)
def detach(ctx, vapp_name, vm_name, disk_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)

        disk_name, disk_id = extract_name_and_id(disk_name)
        disk = vdc.get_disk(name=disk_name, disk_id=disk_id)

        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)

        task = vapp.detach_disk_from_vm(
            disk_href=disk.get('href'), vm_name=vm_name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('list', short_help='list vApps')
@click.pass_context
@click.argument('name', metavar='<vapp-name>', default=None, required=False)
@click.option('--filter', 'filter', metavar='<filter>', help='filter for vapp')
def list_vapps(ctx, name, filter):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        result = []
        records = []
        if name is None:
            if is_sysadmin(ctx):
                resource_type = ResourceType.ADMIN_VAPP.value
            else:
                resource_type = ResourceType.VAPP.value
            name = None
            attributes = None
        else:
            if name is not None:
                if is_sysadmin(ctx):
                    resource_type = ResourceType.ADMIN_VM.value
                else:
                    resource_type = ResourceType.VM.value
            if filter is None:
                filter = 'containerName==' + name
                attributes = [
                    'name', 'containerName', 'ipAddress', 'status', 'memoryMB',
                    'numberOfCpus'
                ]
            else:
                filter = 'name==' + name + ';' + filter
                resource_type = ResourceType.ADMIN_VAPP.value
                attributes = [
                    'isDeployed', 'isEnabled', 'memoryAllocationMB', 'name',
                    'numberOfCpus', 'numberOfVMs', 'ownerName', 'status',
                    'storageKB', 'vdcName'
                ]

        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        records = vdc.list_vapp_details(resource_type, filter)

        if len(records) == 0:
            if name is None:
                result = 'No vApps were found.'
            else:
                result = 'No vms were found.'

        else:
            for r in records:
                result.append(
                    to_dict(
                        r, resource_type=resource_type, attributes=attributes))

            stdout(result, ctx, show_id=False)
    except Exception as e:
        stderr(e, ctx)


@vapp.command(short_help='create a vApp')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.option('-d', '--description', metavar='text', help='vApp description')
@click.option(
    '-c', '--catalog', metavar='name', help='Catalog where the template is')
@click.option('-t', '--template', metavar='name', help='Name of the template')
@click.option(
    '-n',
    '--network',
    'network',
    required=False,
    default=None,
    metavar='name',
    help='Network')
@click.option(
    'ip_allocation_mode',
    '-i',
    '--ip-allocation-mode',
    type=click.Choice(['dhcp', 'pool']),
    required=False,
    default='dhcp',
    metavar='mode',
    help='IP allocation mode')
@click.option(
    '-m',
    '--memory',
    'memory',
    required=False,
    default=None,
    metavar='<MB>',
    type=click.INT,
    help='Amount of memory in MB')
@click.option(
    '-u',
    '--cpu',
    'cpu',
    required=False,
    default=None,
    metavar='<virtual-cpus>',
    type=click.INT,
    help='Number of CPUs')
@click.option(
    '-k',
    '--disk-size',
    'disk_size',
    required=False,
    default=None,
    metavar='<MB>',
    type=click.INT,
    help='Size of the vm home disk in MB')
@click.option(
    '-v',
    '--vm-name',
    required=False,
    default=None,
    metavar='name',
    help='VM name')
@click.option('-o', '--hostname', metavar='hostname', help='Hostname')
@click.option(
    'storage_profile',
    '-s',
    '--storage-profile',
    required=False,
    default=None,
    metavar='name',
    help='Name of the storage profile for the vApp')
@click.option(
    '-a',
    '--accept-all-eulas',
    is_flag=True,
    default=False,
    help='Accept all EULAs')
def create(ctx, name, description, catalog, template, network, memory, cpu,
           disk_size, ip_allocation_mode, vm_name, hostname, storage_profile,
           accept_all_eulas):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        if catalog is None and template is None:
            vapp_resource = vdc.create_vapp(
                name,
                description=description,
                network=network,
                accept_all_eulas=accept_all_eulas)
        else:
            vapp_resource = vdc.instantiate_vapp(
                name,
                catalog,
                template,
                description=description,
                network=network,
                memory=memory,
                cpu=cpu,
                disk_size=disk_size,
                deploy=True,
                power_on=True,
                accept_all_eulas=accept_all_eulas,
                cust_script=None,
                ip_allocation_mode=ip_allocation_mode,
                vm_name=vm_name,
                hostname=hostname,
                storage_profile=storage_profile)
        stdout(vapp_resource.Tasks.Task[0], ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command(short_help='delete a vApp or VM(s)')
@click.pass_context
@click.argument('name', required=True)
@click.argument('vm-names', nargs=-1)
@click.option(
    '-y',
    '--yes',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Are you sure you want to delete the vApp or the VM(s)?')
@click.option(
    '-f',
    '--force',
    is_flag=True,
    help='Force delete running VM(s). Only applies to vApp delete.')
def delete(ctx, name, vm_names, force):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        if len(vm_names) == 0:
            task = vdc.delete_vapp(name, force)
        else:
            vapp_resource = vdc.get_vapp(name)
            vapp = VApp(client, resource=vapp_resource)
            task = vapp.delete_vms(vm_names)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('update-lease', short_help='update vApp lease')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('runtime-seconds', metavar='<runtime-seconds>', required=True)
@click.argument('storage-seconds', metavar='[storage-seconds]', required=False)
def update_lease(ctx, name, runtime_seconds, storage_seconds):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(name)
        vapp = VApp(client, resource=vapp_resource)
        if storage_seconds is None:
            storage_seconds = runtime_seconds
        task = vapp.set_lease(runtime_seconds, storage_seconds)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('change-owner', short_help='change vApp owner')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('user-name', metavar='<user-name>', required=True)
def change_owner(ctx, vapp_name, user_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        in_use_org_href = ctx.obj['profiles'].get('org_href')
        org = Org(client, in_use_org_href)
        user_resource = org.get_user(user_name)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        vapp.change_owner(user_resource.get('href'))
        stdout('vapp owner changed', ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('reboot', short_help='Reboot a vApp or VM(s)')
@click.pass_context
@click.argument('name', required=True)
@click.argument('vm-names', nargs=-1)
@click.option(
    '-y',
    '--yes',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Are you sure you want to reboot the vApp or VM(s)?')
def reboot(ctx, name, vm_names):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(name)
        vapp = VApp(client, resource=vapp_resource)
        if len(vm_names) == 0:
            task = vapp.reboot()
            stdout(task, ctx)
        else:
            for vm_name in vm_names:
                vm = VM(client, href=vapp.get_vm(vm_name).get('href'))
                vm.reload()
                task = vm.reboot()
                stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('power-off', short_help='power off a vApp')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('vm-names', nargs=-1)
@click.option(
    '-y',
    '--yes',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Are you sure you want to power off the vApp?')
def power_off(ctx, name, vm_names):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(name)
        vapp = VApp(client, resource=vapp_resource)
        if len(vm_names) == 0:
            task = vapp.power_off()
            stdout(task, ctx)
        else:
            for vm_name in vm_names:
                vm = VM(client, resource=vapp.get_vm(vm_name))
                task = vm.power_off()
                stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('reset', short_help='Reset a vApp or VM(s)')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('vm-names', nargs=-1)
@click.option(
    '-y',
    '--yes',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Are you sure you want to reset the vApp or VM(s)?')
def reset(ctx, name, vm_names):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(name)
        vapp = VApp(client, resource=vapp_resource)
        if len(vm_names) == 0:
            task = vapp.power_reset()
            stdout(task, ctx)
        else:
            for vm_name in vm_names:
                vm = VM(client, resource=vapp.get_vm(vm_name))
                task = vm.power_reset()
                stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('deploy', short_help='Deploy a vApp or VM(s)')
@click.pass_context
@click.argument('name', required=True)
@click.argument('vm-names', nargs=-1)
@click.option(
    '--power-on/--power-off',
    is_flag=True,
    help='Specifies whether to power on/off vApp/VM on deployment,'
    'if not specified, default is power on')
@click.option(
    '--force-customization',
    is_flag=True,
    help='Specifies whether to force customization on deployment,'
    'if not specified, default is False')
def deploy(ctx, name, vm_names, power_on, force_customization):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(name)
        vapp = VApp(client, resource=vapp_resource)
        if power_on is not None:
            power_on = False
        if force_customization is not None:
            force_customization = True
        if len(vm_names) == 0:
            task = vapp.deploy(power_on=power_on)
            stdout(task, ctx)
        else:
            for vm_name in vm_names:
                vm = VM(client, href=vapp.get_vm(vm_name).get('href'))
                vm.reload()
                task = vm.deploy(
                    power_on=power_on, force_customization=force_customization)
                stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('undeploy', short_help='undeploy a vApp or VM(s)')
@click.pass_context
@click.argument('name', required=True)
@click.argument('vm-names', nargs=-1)
@click.option(
    '-y',
    '--yes',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Are you sure you want to undeploy the vApp or VM(s)?')
@click.option(
    '--action',
    type=click.Choice(['default', 'powerOff', 'suspend', 'shutdown', 'force']),
    required=False,
    default='default',
    help='Undeploy power action')
def undeploy(ctx, name, vm_names, action):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(name)
        vapp = VApp(client, resource=vapp_resource)
        if len(vm_names) == 0:
            task = vapp.undeploy(action)
            stdout(task, ctx)
        else:
            for vm_name in vm_names:
                vm = VM(client, href=vapp.get_vm(vm_name).get('href'))
                vm.reload()
                task = vm.undeploy(action)
                stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('stop', short_help='stop a vApp')
@click.pass_context
@click.argument('vapp_name', required=True, metavar='<vapp_name>')
def stop_vapp(ctx, vapp_name):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        task = vapp.undeploy()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('power-on', short_help='power on a vApp or VM(s)')
@click.pass_context
@click.argument('name', required=True)
@click.argument('vm-names', nargs=-1)
def power_on(ctx, name, vm_names):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(name)
        vapp = VApp(client, resource=vapp_resource)
        if len(vm_names) == 0:
            task = vapp.power_on()
            stdout(task, ctx)
        else:
            for vm_name in vm_names:
                vm = VM(client, resource=vapp.get_vm(vm_name))
                task = vm.power_on()
                stdout(task, ctx)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('shutdown', short_help='shutdown a vApp')
@click.pass_context
@click.argument('name', required=True)
@click.argument('vm-names', nargs=-1)
@click.option(
    '-y',
    '--yes',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Are you sure you want to shutdown the vApp or VM(s)?')
def shutdown(ctx, name, vm_names):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(name)
        vapp = VApp(client, resource=vapp_resource)
        if len(vm_names) == 0:
            task = vapp.shutdown()
            stdout(task, ctx)
        else:
            for vm_name in vm_names:
                vm = VM(client, href=vapp.get_vm(vm_name).get('href'))
                vm.reload()
                task = vm.shutdown()
                stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('suspend', short_help='suspend a vApp')
@click.pass_context
@click.argument('vapp_name', required=True, metavar='<vapp_name>')
def suspend_vapp(ctx, vapp_name):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        task = vapp.suspend_vapp()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command(
    'discard-suspended-state', short_help='discard suspended state of vApp')
@click.pass_context
@click.argument('vapp_name', required=True, metavar='<vapp_name>')
def discard_suspended_state_vapp(ctx, vapp_name):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        task = vapp.discard_suspended_state_vapp()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command(
    'enter-maintenance-mode', short_help='Place a vApp in Maintenance Mode')
@click.pass_context
@click.argument('vapp_name', required=True, metavar='<vapp_name>')
def enter_maintenance_mode(ctx, vapp_name):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        vapp.enter_maintenance_mode()
        stdout('Entered maintenance mode successfully', ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command(
    'exit-maintenance-mode', short_help='exit maintenance mode a vApp')
@click.pass_context
@click.argument('vapp_name', required=True, metavar='<vapp_name>')
def exit_maintenance_mode(ctx, vapp_name):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        vapp.exit_maintenance_mode()
        stdout('exited maintenance mode successfully', ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command(
    'upgrade-virtual-hardware',
    short_help='upgrade virtual hardware of a vApp')
@click.pass_context
@click.argument('vapp_name', required=True, metavar='<vapp_name>')
def upgrade_virtual_hardware(ctx, vapp_name):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        no_of_vm_upgraded = vapp.upgrade_virtual_hardware()
        result = {'No of vm upgraded': no_of_vm_upgraded}
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('download', short_help='Download a vApp')
@click.pass_context
@click.argument('vapp_name', required=True, metavar='<vapp_name>')
@click.argument(
    'file_name',
    type=click.Path(exists=False),
    metavar='[file-name]',
    required=True)
@click.option(
    '-o',
    '--overwrite',
    is_flag=True,
    required=False,
    default=False,
    help='overwrite')
def download_ova(ctx, vapp_name, file_name, overwrite):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        if file_name is not None:
            save_as_name = file_name
        if not overwrite and os.path.isfile(save_as_name):
            raise Exception('File exists.')
        bytes_written = vapp.download_ova(save_as_name)
        result = {'file': save_as_name, 'size': bytes_written}
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('connect', short_help='connect an ovdc network to a vapp')
@click.pass_context
@click.argument('name', required=True, metavar='<vapp-name>')
@click.argument('network', required=True, metavar='<orgvdc-network-name>')
@click.option(
    '--retain-ip',
    is_flag=True,
    default=None,
    help="True if the network resources such as IP/MAC of router will be "
    "retained across deployments. False by default")
@click.option(
    '--is-deployed',
    is_flag=True,
    default=None,
    help="True if this orgvdc network has been deployed. False by default")
def connect(ctx, name, network, retain_ip, is_deployed):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(name)
        vapp = VApp(client, resource=vapp_resource)
        task = vapp.connect_org_vdc_network(
            network, retain_ip=retain_ip, is_deployed=is_deployed)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command(
    'disconnect', short_help='disconnect an ovdc network from a '
    'vapp')
@click.pass_context
@click.argument('name', required=True, metavar='<vapp-name>')
@click.argument('network', required=True, metavar='<orgvdc-network-name>')
@click.option(
    '-y',
    '--yes',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Are you sure you want to disconnect the network?')
def disconnect(ctx, name, network):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(name)
        vapp = VApp(client, resource=vapp_resource)
        task = vapp.disconnect_org_vdc_network(network)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('capture', short_help='Capture a vApp as template')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('catalog', metavar='<catalog>', required=True)
@click.argument('template', metavar='[template]', required=False)
@click.option(
    '-i',
    '--identical',
    'customizable',
    flag_value='identical',
    help='Make identical copy')
@click.option(
    '-c',
    '--customizable',
    'customizable',
    flag_value='customizable',
    default=True,
    help='Make copy customizable during instantiation')
@click.option('-d', '--description', default='', help='Description')
def capture(ctx, name, catalog, template, customizable, description):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        in_use_org_href = ctx.obj['profiles'].get('org_href')
        org = Org(client, in_use_org_href)
        catalog_resource = org.get_catalog(catalog)
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(name)
        overwrite = False
        if template is None:
            template = vapp_resource.get('name')
        else:
            overwrite = True
        task = org.capture_vapp(
            catalog_resource,
            vapp_href=vapp_resource.get('href'),
            catalog_item_name=template,
            description=description,
            customize_on_instantiate=customizable == 'customizable',
            overwrite=overwrite)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('add-disk', short_help='add disk to vm')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
@click.argument('vm-name', required=True, metavar='<vm-name>')
@click.argument('size', metavar='<size>', required=True, type=click.INT)
@click.option(
    'storage_profile',
    '-s',
    '--storage-profile',
    required=False,
    default=None,
    metavar='<storage-profile>',
    help='Name of the storage profile for the new disk')
def add_disk(ctx, name, vm_name, size, storage_profile):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(name)
        vapp = VApp(client, resource=vapp_resource)
        task = vapp.add_disk_to_vm(vm_name, size)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command(short_help='set active vApp')
@click.pass_context
@click.argument('name', metavar='<name>', required=True)
def use(ctx, name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        in_use_org_name = ctx.obj['profiles'].get('org_in_use')
        in_use_vdc_name = ctx.obj['profiles'].get('vdc_in_use')
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(name)
        vapp = VApp(client, resource=vapp_resource)
        ctx.obj['profiles'].set('vapp_in_use', str(name))
        ctx.obj['profiles'].set('vapp_href', str(vapp.href))
        message = 'now using org: \'%s\', vdc: \'%s\', vApp: \'%s\'.' % \
                  (in_use_org_name, in_use_vdc_name, name)
        stdout({
            'org': in_use_org_name,
            'vdc': in_use_vdc_name,
            'vapp': name
        }, ctx, message)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('add-vm', short_help='add VM to vApp')
@click.pass_context
@click.argument('name', metavar='<target-vapp>', required=True)
@click.argument('source-vapp', metavar='<source-vapp>', required=True)
@click.argument('source-vm', metavar='<source-vm>', required=True)
@click.option(
    '-c',
    '--catalog',
    metavar='name',
    help='Name of the catalog if the source vApp is a template')
@click.option(
    '-t',
    '--target-vm',
    metavar='name',
    help='Rename the target VM with this name')
@click.option(
    '-o',
    '--hostname',
    metavar='hostname',
    help='Customize VM and set hostname in the guest OS')
@click.option(
    '-n', '--network', metavar='name', help='vApp network to connect to')
@click.option(
    'ip_allocation_mode',
    '-i',
    '--ip-allocation-mode',
    type=click.Choice(['dhcp', 'pool']),
    required=False,
    default='dhcp',
    metavar='mode',
    help='IP allocation mode')
@click.option(
    'storage_profile',
    '-s',
    '--storage-profile',
    metavar='name',
    help='Name of the storage profile for the VM')
@click.option(
    '--password-auto',
    is_flag=True,
    help='Autogenerate administrator password')
@click.option('--accept-all-eulas', is_flag=True, help='Accept all EULAs')
def add_vm(ctx, name, source_vapp, source_vm, catalog, target_vm, hostname,
           network, ip_allocation_mode, storage_profile, password_auto,
           accept_all_eulas):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        in_use_org_href = ctx.obj['profiles'].get('org_href')
        org = Org(client, in_use_org_href)
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        source_vapp_resource = None
        if catalog is None:
            source_vapp_resource = vdc.get_vapp(source_vapp)
        else:
            catalog_item = org.get_catalog_item(catalog, source_vapp)
            source_vapp_resource = client.get_resource(
                catalog_item.Entity.get('href'))
        assert source_vapp_resource is not None
        vapp_resource = vdc.get_vapp(name)
        vapp = VApp(client, resource=vapp_resource)
        spec = {'source_vm_name': source_vm, 'vapp': source_vapp_resource}
        if target_vm is not None:
            spec['target_vm_name'] = target_vm
        if hostname is not None:
            spec['hostname'] = hostname
        if network is not None:
            spec['network'] = network
            spec['ip_allocation_mode'] = ip_allocation_mode
        if storage_profile is not None:
            spec['storage_profile'] = vdc.get_storage_profile(storage_profile)
        if password_auto is not None:
            spec['password_auto'] = password_auto
        task = vapp.add_vms([spec], all_eulas_accepted=accept_all_eulas)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.group(short_help='work with vapp acl')
@click.pass_context
def acl(ctx):
    """Work with vapp access control list.

\b
   Description
        Work with vapp access control list in the current Organization.
\b
        vcd vapp acl add my-vapp 'user:TestUser1:Change'
            'user:TestUser2:FullControl' 'user:TestUser3'
            Add one or more access setting to the specified vapp.
            access-list is specified in the format
            'user:<username>:<access-level>'
            access-level is one of 'ReadOnly', 'Change', 'FullControl'
            'ReadOnly' by default. eg. 'user:TestUser3'
\b
        vcd vapp acl remove my-vapp 'user:TestUser1' 'user:TestUser2'
            Remove one or more acl from the specified vapp. access-list is
            specified in the format 'user:username'
\b
        vcd vapp acl share my-vapp --access-level ReadOnly
            Share vapp access to all members of the current organization.
            access-level is one of 'ReadOnly', 'Change', 'FullControl'.
            'ReadOnly' by default.
\b
        vcd vapp acl unshare my-vapp
            Unshare  vapp access from  all members of the current
            organization.
\b
        vcd vapp acl list my-vapp
            List acl of a vapp.
    """
    pass


@acl.command(short_help='add access settings to a particular vapp')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>')
@click.argument('access-list', nargs=-1, required=True)
def add(ctx, vapp_name, access_list):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp = VApp(client, resource=vdc.get_vapp(vapp_name))

        vapp.add_access_settings(
            access_settings_list=acl_str_to_list_of_dict(access_list))
        stdout('Access settings added to vapp \'%s\'.' % vapp_name, ctx)
    except Exception as e:
        stderr(e, ctx)


@acl.command(short_help='remove access settings from a particular vapp')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>')
@click.argument('access-list', nargs=-1, required=False)
@click.option(
    '--all',
    is_flag=True,
    required=False,
    default=False,
    metavar='[all]',
    help='remove all the access settings from the vapp')
@click.option(
    '-y',
    '--yes',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Are you sure you want to remove access settings?')
def remove(ctx, vapp_name, access_list, all):
    try:
        if all:
            click.confirm(
                'Do you want to remove all access settings from the vapp '
                '\'%s\'' % vapp_name,
                abort=True)
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp = VApp(client, resource=vdc.get_vapp(vapp_name))

        vapp.remove_access_settings(
            access_settings_list=acl_str_to_list_of_dict(access_list),
            remove_all=all)
        stdout('Access settings removed from vapp \'%s\'.' % vapp_name, ctx)
    except Exception as e:
        stderr(e, ctx)


@acl.command(short_help='share vapp access to all members of the current v'
             'organization')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>')
@click.option(
    'access_level',
    '--access-level',
    type=click.Choice(['ReadOnly', 'Change', 'FullControl']),
    required=False,
    default='ReadOnly',
    metavar='<access-level>',
    help='access level at which the vapp is shared. ReadOnly by'
    ' default')
def share(ctx, vapp_name, access_level):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp = VApp(client, resource=vdc.get_vapp(vapp_name))

        vapp.share_with_org_members(everyone_access_level=access_level)
        stdout(
            'Vapp \'%s\' shared to all members of the org \'%s\'.' %
            (vapp_name, ctx.obj['profiles'].get('org_in_use')), ctx)
    except Exception as e:
        stderr(e, ctx)


@acl.command(short_help='unshare vapp access from members of the '
             'current organization')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>')
def unshare(ctx, vapp_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp = VApp(client, resource=vdc.get_vapp(vapp_name))

        vapp.unshare_from_org_members()
        stdout(
            'Vapp \'%s\' unshared from all members of the org \'%s\'.' %
            (vapp_name, ctx.obj['profiles'].get('org_in_use')), ctx)
    except Exception as e:
        stderr(e, ctx)


@acl.command('list', short_help='list vapp access control list')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>')
def list_acl(ctx, vapp_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp = VApp(client, resource=vdc.get_vapp(vapp_name))

        acl = vapp.get_access_settings()
        stdout(
            access_settings_to_list(
                acl, ctx.obj['profiles'].get('org_in_use')), ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('update', short_help='update vapp\'s name and description')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>')
@click.option(
    '-n',
    '--name',
    'name',
    required=True,
    metavar='<name>',
    help='new name of the vapp')
@click.option(
    '-d',
    '--description',
    'description',
    metavar='<description>',
    help='new description of the vapp')
def update_vapp(ctx, vapp_name, name, description):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)

        task = vapp.edit_name_and_description(name, description)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('copy', short_help='copy a vapp')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp_name>')
@click.option(
    '-n',
    '--name',
    'vapp_new_name',
    required=True,
    metavar='<vapp_new_name>',
    help='name of copy vapp')
@click.option(
    '-v',
    '--vdc',
    'vdc',
    default=None,
    metavar='<vdc>',
    help='virtual datacenter name where need to copy vapp')
@click.option(
    '-d',
    '--description',
    'description',
    metavar='<description>',
    help='description of copy vapp')
def copy_to(ctx, vapp_name, vapp_new_name, vdc, description):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        logged_in_org = client.get_org()
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        if vdc is not None:
            if client.get_api_version() < ApiVersion.VERSION_33.value:
                links = get_links(
                    logged_in_org, media_type=EntityType.VDC.value)
            else:
                links = client.get_resource_link_from_query_object(
                    logged_in_org,
                    media_type=EntityType.RECORDS.value,
                    type='vdc')
            for v in links:
                if vdc == v.name:
                    vdc_href = v.href
                    break
        vapp = get_vapp(ctx, vapp_name)
        task = vapp.copy_to(vdc_href, vapp_new_name, description)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('move', short_help='move a vapp')
@click.pass_context
@click.argument('vapp_name', metavar='<vapp_name>')
@click.option(
    '-v',
    '--vdc',
    'vdc',
    default=None,
    required=True,
    metavar='<vdc>',
    help='virtual datacenter name where need to move vapp')
def move_to(ctx, vapp_name, vdc):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        org_in_use = ctx.obj['profiles'].get('org_in_use')
        org_resource = client.get_org_by_name(org_in_use)
        vdc_href = None
        if vdc is not None:
            if client.get_api_version() < ApiVersion.VERSION_33.value:
                links = get_links(
                    org_resource, media_type=EntityType.VDC.value)
            else:
                links = client.get_resource_link_from_query_object(
                    org_resource,
                    media_type=EntityType.RECORDS.value,
                    type='vdc')
            for v in links:
                if vdc == v.name:
                    vdc_href = v.href
                    break
        if vdc_href is not None:
            vapp = get_vapp(ctx, vapp_name)
            task = vapp.move_to(vdc_href)
            stdout(task, ctx)
        else:
            stdout('Org vdc not found', ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('create-snapshot', short_help='create snapshot of a vapp')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.option(
    'is_memory',
    '--is-include-memory',
    default=False,
    required=False,
    metavar='<is_memory>',
    type=click.BOOL,
    help='Include the virtual machine memory')
@click.option(
    'quiesce',
    '--quiesce',
    default=False,
    required=False,
    metavar='<quiesce>',
    type=click.BOOL,
    help='file system of the vm should be quiesced')
def create_snapshot(ctx, vapp_name, is_memory, quiesce):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        task = vapp.create_snapshot(memory=is_memory, quiesce=quiesce)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command(
    'revert-to-snapshot', short_help='revert vapp to current snapshot')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
def revert_to_snapshot(ctx, vapp_name):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        task = vapp.snapshot_revert_to_current()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vapp.command('remove-snapshot', short_help='rmove snapshot of vapp')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
def snapshot_remove(ctx, vapp_name):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = get_vapp(ctx, vapp_name)
        task = vapp.snapshot_remove()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


def get_vapp(ctx, vapp_name):
    client = ctx.obj['client']
    vdc_href = ctx.obj['profiles'].get('vdc_href')
    vdc = VDC(client, href=vdc_href)
    return VApp(client, resource=vdc.get_vapp(vapp_name))
