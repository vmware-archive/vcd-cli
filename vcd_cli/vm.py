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

import click
from pyvcloud.vcd.client import IpAddressMode
from pyvcloud.vcd.client import NetworkAdapterType
from pyvcloud.vcd.utils import vm_to_dict
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
        vcd vm add-nic vapp1 vm1
                --adapter-type VMXNET3
                --primary
                --connect
                --network network_name
                --ip-address-mode MANUAL
                --ip-address 192.168.1.10
            Adds a nic to the VM.

\b
        vcd vm list-nics vapp1 vm1
            Lists the nics of the VM.

\b
        vcd vm delete-nic vapp1 vm1
                --index 1
            Deletes the nic at given index.

\b
        vcd vm power-on vapp1 vm1
            Power on the VM.

\b
        vcd vm power-off vapp1 vm1
            Power off the VM.

\b
        vcd vm reboot vapp1 vm1
            Reboot the VM.

\b
        vcd vm shutdown vapp1 vm1
            Shutdown the VM.

\b
        vcd vm suspend vapp1 vm1
            Suspend the VM.

\b
        vcd vm discard-suspend vapp1 vm1
            Discard suspended state of the VM.

\b
        vcd vm reset vapp1 vm1
            Reset the VM.

\b
        vcd vm install-vmware-tools vapp1 vm1
            Install vmware tools in the VM.

\b
        vcd vm insert-cd vapp1 vm1
                --media-href https://10.11.200.00/api/media/76e53c34-1845-43ca-bd5a-759c0d537433
            Insert CD from catalog to the VM.

\b
        vcd vm eject-cd vapp1 vm1
                --media-href https://10.11.200.00/api/media/76e53c34-1845-43ca-bd5a-759c0d537433
            Eject CD from the VM.

\b
        vcd vm consolidate vapp1 vm1
            Consolidate the VM.

\b
        vcd vm create-snapshot vapp1 vm1
            Create snapshot of the VM.

\b
        vcd vm revert-to-snapshot vapp1 vm1
            Revert VM to current snapshot.

\b
        vcd vm copy vapp1 vm1 vapp2 vm2
            Copy VM from one vapp to another vapp.

\b
        vcd vm move vapp1 vm1 vapp2 vm2
            Move VM from one vapp to another vapp.

\b
        vcd vm delete vapp1 vm1
            Delete VM.

\b
        vcd vm attach-disk vapp1 vm1
               --idisk-href https://10.11.200.00/api/disk/76e53c34-1845-43ca-bd5a-759c0d537433
            Attach independent disk to VM.

\b
        vcd vm deploy vapp1 vm1
            Deploy a VM.

\b
        vcd vm undeploy vapp1 vm1
            Undeploy a VM.

\b
        vcd vm upgrade-virtual-hardware vapp1 vm1
            Upgrade virtual hardware of VM.

\b
        vcd vm general-setting vapp1 vm1
            Show general setting details of VM.


\b
        vcd vm list-storage-profile vapp1 vm1
            List all storage profiles of VM.

    """
    pass


@vm.command('list', short_help='list VMs')
@click.pass_context
def list_vms(ctx):
    try:
        raise Exception('not implemented')
    except Exception as e:
        stderr(e, ctx)


def _get_vapp(ctx, vapp_name):
    client = ctx.obj['client']
    vdc_href = ctx.obj['profiles'].get('vdc_href')
    vdc = VDC(client, href=vdc_href)
    vapp_resource = vdc.get_vapp(vapp_name)
    return VApp(client, resource=vapp_resource)


def _get_vm(ctx, vapp_name, vm_name):
    client = ctx.obj['client']
    vapp = _get_vapp(ctx, vapp_name)
    vm_resource = vapp.get_vm(vm_name)
    return VM(client, href=vm_resource.get('href'))


@vm.command(short_help='show VM details')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def info(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name).get_resource()
        result = vm_to_dict(vm)
        result['vapp'] = vapp_name
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
        vm = _get_vm(ctx, vapp_name, vm_name)
        if cpu is not None:
            task_cpu_update = vm.modify_cpu(cpu, cores)
            stdout("Updating cpu (and core(s) if specified) for the VM")
            stdout(task_cpu_update, ctx)
        if memory is not None:
            task_memory_update = vm.modify_memory(memory)
            stdout("Updating memory for the VM")
            stdout(task_memory_update, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('add-nic', short_help='Add a nic to the VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'adapter_type',
    '--adapter-type',
    required=False,
    metavar='<adapter-type>',
    type=click.Choice([
        NetworkAdapterType.VLANCE.value, NetworkAdapterType.VMXNET.value,
        NetworkAdapterType.VMXNET2.value, NetworkAdapterType.VMXNET3.value,
        NetworkAdapterType.E1000.value
    ]),
    help='adapter type of nic - one of VLANCE|VMXNET|VMXNET2|VMXNET3|E1000')
@click.option(
    'primary',
    '--primary',
    required=False,
    is_flag=True,
    metavar='<primary>',
    help='whether nic has to be a primary')
@click.option(
    'connect',
    '--connect',
    required=False,
    is_flag=True,
    metavar='<connect>',
    help='whether nic has to be connected')
@click.option(
    'network',
    '--network',
    required=False,
    default='none',
    metavar='<network>',
    help='network to connect to')
@click.option(
    'ip_address_mode',
    '--ip-address-mode',
    required=False,
    default=IpAddressMode.DHCP.value,
    metavar='<ip-address-mode>',
    type=click.Choice([
        IpAddressMode.DHCP.value, IpAddressMode.POOL.value,
        IpAddressMode.MANUAL.value
    ]),
    help='IP address allocation mode - one of DHCP|POOL|MANUAL|NONE')
@click.option(
    'ip_address',
    '--ip-address',
    required=False,
    metavar='<ip-address>',
    help='nanual IP address that needs to be allocated to the nic')
def add_nic(ctx, vapp_name, vm_name, adapter_type, primary, connect, network,
            ip_address_mode, ip_address):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.add_nic(adapter_type, primary, connect, network,
                          ip_address_mode, ip_address)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('list-nics', short_help='List all the nics of the VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def list_nics(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        nics = vm.list_nics()
        stdout(nics, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('delete-nic', short_help='Delete the nic with the index')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'index',
    '--index',
    required=True,
    metavar='<index>',
    type=click.INT,
    help='index of the nic to be deleted')
def delete_nic(ctx, vapp_name, vm_name, index):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.delete_nic(index)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('power-off', short_help='power off a VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def power_off(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.power_off()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('power-on', short_help='power on a VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def power_on(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.power_on()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('reboot', short_help='reboot a VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def reboot(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.reboot()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('shutdown', short_help='shutdown a VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def shutdown(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.shutdown()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('suspend', short_help='suspend a VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def suspend(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.suspend()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('discard-suspend', short_help='discard suspend state of a VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def discard_suspend(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.discard_suspended_state()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('reset', short_help='reset a VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def reset(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.power_reset()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('install-vmware-tools', short_help='instal vmware tools')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def install_vmware_tools(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.install_vmware_tools()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('insert-cd', short_help='insert CD from catalog')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'media_href',
    '--media-href',
    required=True,
    metavar='<media-href>',
    help='media href to be inserted')
def insert_cd(ctx, vapp_name, vm_name, media_href):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.insert_cd_from_catalog(media_href)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('eject-cd', short_help='eject CD from VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'media_href',
    '--media-href',
    required=True,
    metavar='<media-href>',
    help='media href to be ejected')
def eject_cd(ctx, vapp_name, vm_name, media_href):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.eject_cd(media_href)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('consolidate', short_help='consolidate VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def consolidate(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.consolidate()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('create-snapshot', short_help='create snapshot of a VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'is_memory',
    '--is-include-memory',
    required=False,
    metavar='<is_memory>',
    type=click.BOOL,
    help='Include the virtual machine memory')
@click.option(
    'quiesce',
    '--quiesce',
    required=False,
    metavar='<quiesce>',
    type=click.BOOL,
    help='file system of the vm should be quiesced')
@click.option(
    'name',
    '--name',
    required=False,
    metavar='<name>',
    type=click.STRING,
    help='snapshot name')
def create_snapshot(ctx, vapp_name, vm_name, is_memory, quiesce, name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.snapshot_create(memory = is_memory,
                                  quiesce = quiesce,
                                  name = name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('revert-to-snapshot', short_help='revert VM to current snapshot')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def revert_to_snapshot(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.snapshot_revert_to_current()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('copy', short_help='copy vm from one vapp to another vapp')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'target_vapp_name',
    '--target-vapp-name',
    required=True,
    metavar='<target-vapp>',
    help='target vapp name')
@click.option(
    'target_vm_name',
    '--target-vm-name',
    required=True,
    metavar='<target-vm>',
    help='target vm name')
def copy_to(ctx, vapp_name, vm_name, target_vapp_name, target_vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.copy_to(source_vapp_name=vapp_name,
                          target_vapp_name=target_vapp_name,
                          target_vm_name=target_vm_name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('move', short_help='move VM from one vapp to another vapp')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'target_vapp_name',
    '--target-vapp-name',
    required=True,
    metavar='<target-vapp>',
    help='target vapp name')
@click.option(
    'target_vm_name',
    '--target-vm-name',
    required=True,
    metavar='<target-vm>',
    help='target vm name')
def move_to(ctx, vapp_name, vm_name, target_vapp_name, target_vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.move_to(source_vapp_name=vapp_name,
                          target_vapp_name=target_vapp_name,
                          target_vm_name=target_vm_name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('delete', short_help='delete VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def delete(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.delete()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('attach-disk', short_help='attach independent disk to VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'idisk_href',
    '--idisk-href',
    required=True,
    metavar='<idisk-href>',
    help='idisk href')
def attach_disk(ctx, vapp_name, vm_name, idisk_href):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = _get_vapp(ctx, vapp_name)
        task = vapp.attach_disk_to_vm(disk_href=idisk_href, vm_name=vm_name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('deploy', short_help='deploy a VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def deploy(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.deploy()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('undeploy', short_help='undeploy a VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def undeploy(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.undeploy()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command(
    'upgrade-virtual-hardware', short_help='upgrade virtual hardware of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def upgrade_virtual_hardware(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.upgrade_virtual_hardware()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('general-setting', short_help='general setting detail of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def general_setting_detail(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.general_setting_detail()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command(
    'list-storage-profile', short_help='list all storage profiles of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def list_storage_profile(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.list_storage_profile()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)
