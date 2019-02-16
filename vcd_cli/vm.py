# vCloud CLI 0.1
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
import json

import click
from pyvcloud.vcd.vapp import VApp
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.vm import VM

from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import vcd


@vcd.group(short_help='manage VMs')
@click.pass_context
def vm(ctx):
    """Manage VMs in vCloud Director.

\b
    Examples
        vcd vm list
            Get list of VMs in current virtual datacenter.
\b
        vcd vm info vapp1 vm1
            Get details of the VM 'vm1' in vApp 'vapp1'.
\b
        vcd vm update vapp1 vm1 --cpu 2 --core 2
            Modifies the VM 'vm1' in vApp 'vapp1' to be configured
            with 2 cpu and 2 cores .
\b
        vcd vm update vapp1 vm1 --memory 512
            Modifies the VM 'vm1' in vApp 'vapp1' to be configured
            with the specified memory .
\b
        vcd vm update vapp1 vm1 --cpu 2 --memory 512
            Modifies the VM 'vm1' in vApp 'vapp1' to be configured
            with 2 cpu and the specified memory .
\b
        vcd vm power-on vapp1 vm1
            Power On the VM 'vm1' in vApp 'vapp1'.
\b
        vcd vm power-off vapp1 vm1
            Power Off the VM 'vm1' in vApp 'vapp1'.
\b
        vcd vm power-reset vapp1 vm1
            Power reset the VM 'vm1' in vApp 'vapp1'.
\b
        vcd vm reboot vapp1 vm1
            Reboot the VM 'vm1' in vApp 'vapp1'.
\b
        vcd vm shutdown vapp1 vm1
            Shutdown the VM 'vm1' in vApp 'vapp1'.
\b
        vcd vm show-snapshot vapp1 vm1
            Show snapshot for the VM 'vm1' in vApp 'vapp1'.
\b
        vcd vm create-snapshot vapp1 vm1
            Create snapshot for the VM 'vm1' in vApp 'vapp1'.
\b
        vcd vm revert-snapshot vapp1 vm1
            Revert to the current snapshot for the VM 'vm1' in vApp 'vapp1'.
\b
        vcd vm remove-snapshot vapp1 vm1
            Remove all snapshots for the VM 'vm1' in vApp 'vapp1'.
    """
    pass


@vm.command('list', short_help='list VMs in a vApp')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
def list_vms(ctx, vapp_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        vm_list = vapp.get_all_vms()
        stdout_vm_list = []
        for vm_obj in vm_list:
            vm_attributes = dict(vm_obj.attrib)
            if "type" in vm_attributes:
                del vm_attributes["type"]
            if hasattr(vm_obj, "Description"):
                vm_attributes["description"] = vm_obj.Description.text
            if hasattr(vm_obj, "DateCreated"):
                vm_attributes["date_created"] = vm_obj.DateCreated.text
            stdout_vm_list.append(vm_attributes)
        result = {'vm_list': json.dumps(stdout_vm_list, indent=4)}
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command(short_help='show VM details')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def info(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        result = {'primary_ip': vapp.get_primary_ip(vm_name)}
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('update', short_help='Update the VM properties and configurations')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'cpu',
    '--cpu',
    required=False,
    metavar='<cpu>',
    type=click.INT,
    help='Number of virtual CPUs to configure the VM.')
@click.option(
    'cores',
    '--cores',
    required=False,
    default=None,
    metavar='<cores>',
    type=click.INT,
    help='Number of cores per socket.')
@click.option(
    'memory',
    '--memory',
    required=False,
    metavar='<memory>',
    type=click.INT,
    help='Memory to configure the VM.')
def update(ctx, vapp_name, vm_name, cpu, cores, memory):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        vm_resource = vapp.get_vm(vm_name)
        vm_obj = VM(client, resource=vm_resource)
        if cpu is not None:
            task_cpu_update = vm_obj.modify_cpu(cpu, cores)
            stdout("Updating cpu (and core(s) if specified) for the VM")
            stdout(task_cpu_update, ctx)
        if memory is not None:
            task_memory_update = vm_obj.modify_memory(memory)
            stdout("Updating memory for the VM")
            stdout(task_memory_update, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('power-on', short_help='Powers on the vm.')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def power_on(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        vm_resource = vapp.get_vm(vm_name)
        vm_obj = VM(client, resource=vm_resource)

        if not vm_obj.is_powered_on(vm_resource):
            stdout("Powering on the virtual machine")
            power_on_command = vm_obj.power_on()
            exec_results = dict(power_on_command.attrib)
            result = {'vm_power_on': json.dumps(exec_results, indent=4)}
        else:
            result = {'vm_power_on': "Already powered on."}
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('power-off', short_help='Powers off the vm.')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def power_off(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        vm_resource = vapp.get_vm(vm_name)
        vm_obj = VM(client, resource=vm_resource)
        if not vm_obj.is_powered_off(vm_resource):
            stdout("Powering off the virtual machine")
            power_off_command = vm_obj.power_off()
            exec_results = dict(power_off_command.attrib)
            result = {'vm_power_off': json.dumps(exec_results, indent=4)}
        else:
            result = {'vm_power_off': "Already powered off."}
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('power-reset', short_help='Powers reset the vm.')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def power_reset(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        vm_resource = vapp.get_vm(vm_name)
        vm_obj = VM(client, resource=vm_resource)
        if vm_obj.is_powered_on(vm_resource):
            stdout("Resetting the virtual machine")
            power_reset_command = vm_obj.power_reset()
            exec_results = dict(power_reset_command.attrib)
            result = {'vm_power_reset': json.dumps(exec_results, indent=4)}
        else:
            result = {
                'vm_power_reset':
                    "VM is powered off, please power on VM to reset power."
            }

        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('reboot', short_help='Reboots the vm.')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def reboot(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        vm_resource = vapp.get_vm(vm_name)
        vm_obj = VM(client, resource=vm_resource)
        if vm_obj.is_powered_on(vm_resource):
            stdout("Rebooting on the virtual machine")
            reboot_command = vm_obj.reboot()
            exec_results = dict(reboot_command.attrib)
            result = {'vm_reboot': json.dumps(exec_results, indent=4)}
        else:
            result = {
                'vm_reboot': "VM is powered off, please power on VM to reboot."
            }
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('shutdown', short_help='Shutdown the vm.')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def shutdown(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        vm_resource = vapp.get_vm(vm_name)
        vm_obj = VM(client, resource=vm_resource)
        if vm_obj.is_powered_on(vm_resource):
            stdout("Shutting down on the virtual machine")
            shutdown_command = vm_obj.shutdown()
            exec_results = dict(shutdown_command.attrib)
            result = {'vm_shutdown': json.dumps(exec_results, indent=4)}
        else:
            result = {
                'vm_shutdown':
                    "VM is powered off, please power on VM to shutdown."
            }
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('show-snapshot', short_help='Show VM snapshot.')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def show_snapshot(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        vm_resource = vapp.get_vm(vm_name)
        vm_obj = VM(client, resource=vm_resource)
        vm_resource = vm_obj.get_resource()
        snapshot_list = []
        for snapshot in vm_resource.SnapshotSection:
            if not hasattr(snapshot, "Snapshot"):
                continue
            snapshot_list.append(dict(snapshot.Snapshot.attrib))
        result = {'vm_snapshot': json.dumps(snapshot_list, indent=4)}
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('create-snapshot', short_help='Create a snapshot of the vm.')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.argument('snapshot-name', metavar='<snapshot-name>', required=False)
@click.option(
    'quiesce',
    '--quiesce',
    required=False,
    default=True,
    metavar='<quiesce>',
    type=click.BOOL,
    help='Should snapshot include the virtual machine’s memory.')
@click.option(
    'memory',
    '--memory',
    required=False,
    default=True,
    metavar='<memory>',
    type=click.BOOL,
    help='Set this flag if you need file system of the virtual '
         'machine be quiesced before the snapshot is created. '
         'Requires VMware tools to be installed on the vm.')
def create_snapshot(ctx, vapp_name, vm_name, snapshot_name, quiesce, memory):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        vm_resource = vapp.get_vm(vm_name)
        vm_obj = VM(client, resource=vm_resource)
        stdout("Creating snapshot for the virtual machine")
        create_command = vm_obj.snapshot_create(memory, quiesce, snapshot_name)
        exec_results = dict(create_command.attrib)
        result = {'vm_create_snapshot': json.dumps(exec_results, indent=4)}
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command(
    'revert-snapshot',
    short_help='Reverts a virtual machine to the current snapshot, if any.')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def revert_snapshot(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        vm_resource = vapp.get_vm(vm_name)
        vm_obj = VM(client, resource=vm_resource)
        stdout("Reverting to the latest snapshot of the virtual machine")
        revert_command = vm_obj.snapshot_revert_to_current()
        exec_results = dict(revert_command.attrib)
        result = {'vm_snapshot_revert': json.dumps(exec_results, indent=4)}
        stdout(result, ctx)
    except Exception as e:
        note = "please check if VM snapshots exist. You can run show-snapshot command to list VM snapshots."
        stderr(str(e) + "\n{}".format(note), ctx)


@vm.command(
    'remove-snapshot',
    short_help='Removes all user created snapshots of a virtual machine.')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def remove_snapshot(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        vm_resource = vapp.get_vm(vm_name)
        vm_obj = VM(client, resource=vm_resource)
        stdout("Removing all snapshots of the virtual machine")
        remove_command = vm_obj.snapshot_remove_all()
        exec_results = dict(remove_command.attrib)
        result = {'vm_snapshot_remove': json.dumps(exec_results, indent=4)}
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
