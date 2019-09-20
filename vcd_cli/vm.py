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
from pyvcloud.vcd.client import MetadataDomain
from pyvcloud.vcd.client import NetworkAdapterType
from pyvcloud.vcd.utils import metadata_to_dict
from pyvcloud.vcd.platform import Platform
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
        vcd vm update-nic vapp1 vm1
                --adapter-type VMXNET3
                --primary
                --connect
                --network network_name
                --ip-address-mode MANUAL
                --ip-address 192.168.1.10
            Update a nic of the VM.


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
                --media-id 76e53c34-1845-43ca-bd5a-759c0d537433
            Insert CD from catalog to the VM.

\b
        vcd vm eject-cd vapp1 vm1
                --media-id 76e53c34-1845-43ca-bd5a-759c0d537433
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
        vcd vm remove-snapshot vapp1 vm1
            Remove VM snapshot.

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
               --idisk-id 76e53c34-1845-43ca-bd5a-759c0d537433
            Attach independent disk to VM.

\b
        vcd vm detach-disk vapp1 vm1
               --idisk-id 76e53c34-1845-43ca-bd5a-759c0d537433
            Detach independent disk from VM.

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

\b
        vcd vm reload-from-vc vapp1 vm1
            Reload VM from VC.

\b
        vcd vm check-compliance vapp1 vm1
            Check compliance of VM.

\b
        vcd vm gc-enable vapp1 vm1
                --enable
            Enable guest customization of VM.

\b
        vcd vm gc-status vapp1 vm1
            Returns guest customization status of VM.

\b
        vcd vm customize-on-next-poweron vapp1 vm1
            Customize on next power on of VM.

\b
        vcd vm poweron-force-recustomize vapp1 vm1
            Power on and force re-customize VM.

\b
        vcd vm list-virtual-hardware-section vapp1 vm1
            List virtual hadware section of VM.

\b
        vcd vm get-compliance-result vapp1 vm1
            Get compliance result of VM.

\b
        vcd vm list-current-metrics vapp1 vm1
            List current metrics of VM.

\b
        vcd vm list-subset-current-metrics vapp1 vm1
                --metric-pattern *.average
            List subset of current metrics of VM based on metric pattern.

\b
        vcd vm list-historic-metrics vapp1 vm1
            List historic metrics of VM.

\b
        vcd vm list-sample-historic-data vapp1 vm1
                --metric-name disk.read.average
            List historic sample data of given metric of VM.

\b
        vcd vm update-general-setting vapp1 vm1 --name vm_new_name
            --d vm_new_description --cn new_computer_name --bd 60
            --ebs True
            Update general setting details of VM.

\b
        vcd vm relocate vapp1 vm1
                --datastore-id 0d8c7358-3e8d-4862-9364-68155069d252
            Relocate VM to given datastore.

\b
        vcd vm list-os-section vapp1 vm1
            List OS section properties of VM.

\b
        vcd vm update-os-section vapp1 vm1
                --ovf-info newInfo
                --description newDescription
            Update OS section properties of VM.

\b
        vcd vm list-gc-section vapp1 vm1
            List guest customization section properties of VM.

\b
        vcd vm update-gc-section
                --disable
            Update guest customization section properties of VM.

\b
        vcd vm check-post-gc-script vapp1 vm1
            Check post guest customization script status of VM.

\b
        vcd vm list-vm-capabilities vapp1 vm1
            List VM capabilities section properties of VM.

\b
        vcd vm update-vm-capabilities
                --enable-memory-hot-add
            Update VM capabilities section properties of VM.

\b
        vcd vm list-runtime-info vapp1 vm1
            List runtime info properties of VM.

\b
        vcd vm list-boot-options vapp1 vm1
            List boot options properties of VM.

\b
        vcd vm update-boot-options vapp1 vm1
                --enable-enter-bios-setup
            Update boot options properties of VM.

\b
        vcd vm set-metadata vapp1 vm1
                --domain GENERAL
                --visibility READWRITE
                --key key1
                --value value1
                --value-type MetadataStringValue
            Set metadata of VM.

\b
        vcd vm update-metadata vapp1 vm1
                --domain GENERAL
                --visibility READWRITE
                --key key1
                --value value2
                --value-type MetadataStringValue
            Update metadata of VM.

\b
        vcd vm list-metadata vapp1 vm1
            List metadata of VM.

\b
        vcd vm remove-metadata vapp1 vm1
                --domain GENERAL
                --key key1
            Remove metadata of VM.

\b
        vcd vm list-screen-ticket vapp1 vm1
            List screen ticket of VM.

\b
        vcd vm list-mks-ticket vapp1 vm1
            List mks ticket of VM.

\b
        vcd vm list-product-sections vapp1 vm1
            List product sections of VM.

\b
        vcd vm update-vhs-disk vapp1 vm1
                --e-name 'Hard Disk 1'
                --v-quantity 694487
            Update virtual hardware section disk of VM.

\b
        vcd vm update-vhs-media  vapp1 vm1
                --e-name 'CD DVD DRive'
                --host-resource pb1.iso
            Update virtual hardware section media of VM.

\b
        vcd vm enable-nested-hypervisor vapp1 vm1
            Enable nested hypervisor of VM.
    """
    pass


@vm.command('list', short_help='list VMs')
@click.pass_context
def list_vms(ctx):
    try:
        raise Exception('not implemented')
    except Exception as e:
        stderr(e, ctx)

def _get_vdc(ctx):
    client = ctx.obj['client']
    vdc_href = ctx.obj['profiles'].get('vdc_href')
    vdc = VDC(client, href=vdc_href)
    return vdc

def _get_vapp(ctx, vapp_name):
    client = ctx.obj['client']
    vdc = _get_vdc(ctx)
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

@vm.command('update-nic', short_help='Update a nic to the VM')
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
    required=True,
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
def update_nic(ctx, vapp_name, vm_name, adapter_type, primary, connect, network,
               ip_address_mode, ip_address):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.update_nic(network_name=network, is_connected=connect,
                             is_primary=primary,
                             ip_address_mode=ip_address_mode,
                             ip_address=ip_address, adapter_type=adapter_type)
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
    'media_id',
    '--media-id',
    required=True,
    metavar='<media-id>',
    help='media id to be inserted')
def insert_cd(ctx, vapp_name, vm_name, media_id):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.insert_cd_from_catalog(media_id=media_id)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('eject-cd', short_help='eject CD from VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'media_id',
    '--media-id',
    required=True,
    metavar='<media-id>',
    help='media id to be ejected')
def eject_cd(ctx, vapp_name, vm_name, media_id):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.eject_cd(media_id=media_id)
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

@vm.command('remove-snapshot', short_help='remove VM snaphot')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def remove_snapshot(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.snapshot_remove_all()
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
    'idisk_id',
    '--idisk-id',
    required=True,
    metavar='<idisk-id>',
    help='idisk id')
def attach_disk(ctx, vapp_name, vm_name, idisk_id):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = _get_vapp(ctx, vapp_name)
        vdc = _get_vdc(ctx)
        disk = vdc.get_disk(disk_id=idisk_id)
        idisk_href = disk.get('href')
        task = vapp.attach_disk_to_vm(disk_href=idisk_href, vm_name=vm_name)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('detach-disk', short_help='detach independent disk from VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'idisk_id',
    '--idisk-id',
    required=True,
    metavar='<idisk-id>',
    help='idisk id')
def detach_disk(ctx, vapp_name, vm_name, idisk_id):
    try:
        restore_session(ctx, vdc_required=True)
        vapp = _get_vapp(ctx, vapp_name)
        vdc = _get_vdc(ctx)
        disk = vdc.get_disk(disk_id=idisk_id)
        idisk_href = disk.get('href')
        task = vapp.detach_disk_from_vm(disk_href=idisk_href, vm_name=vm_name)
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

@vm.command('reload-from-vc', short_help='reload VM from VC')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def reload_from_vc(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.reload_from_vc()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('check-compliance', short_help='check compliance of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def check_compliance(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.check_compliance()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('customize-on-next-poweron', short_help='customize on '
                                                    'next power on of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def customize_on_next_poweron(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.customize_at_next_power_on()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('gc-enable', short_help='enable/disable the guest customization')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    '--enable/--disable',
    'is_enabled',
    default=None,
    help='enable/disable the guest customization')
def gc_enable(ctx, vapp_name, vm_name, is_enabled):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.enable_guest_customization(is_enabled = is_enabled)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('gc-status', short_help='get guest customization status')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def get_gc_status(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.get_guest_customization_status()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('poweron-force-recustomize', short_help='power on and '
                                                        'force recustomize VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def power_on_and_force_recustomize(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.power_on_and_force_recustomization()
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('list-virtual-hardware-section', short_help='list virtual hardware '
                                                        'section of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'is_cpu',
    '--is-include-cpu',
    required=False,
    metavar='<is_cpu>',
    type=click.BOOL,
    help='list the virtual machine CPU')
@click.option(
    'is_memory',
    '--is-include-memory',
    required=False,
    metavar='<is_memory>',
    type=click.BOOL,
    help='list the virtual machine memory')
@click.option(
    'is_disk',
    '--is-include-disk',
    required=False,
    metavar='<is_disk>',
    type=click.BOOL,
    help='list the virtual machine disk')
@click.option(
    'is_media',
    '--is-include-media',
    required=False,
    metavar='<is_media>',
    type=click.BOOL,
    help='list the virtual machine media')
@click.option(
    'is_network',
    '--is-include-network',
    required=False,
    metavar='<is_network>',
    type=click.BOOL,
    help='list the virtual machine network')
def list_virtual_hardware_section(ctx, vapp_name, vm_name, is_cpu, is_memory,
                                  is_disk, is_media, is_network):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.list_virtual_hardware_section(is_cpu=is_cpu,
                                                is_memory=is_memory,
                                                is_disk=is_disk,
                                                is_media=is_media,
                                                is_networkCards=is_network)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('get-compliance-result', short_help='get compliance result of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def get_compliance_result(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.get_compliance_result()
        compliance_result = result.ComplianceStatus
        stdout(compliance_result, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('list-current-metrics', short_help='list current metrics of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def list_all_currennt_metrics(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.list_all_current_metrics()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('list-subset-current-metrics', short_help='list subset of '
                                                      'current metrics of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'metric_pattern',
    '--metric-pattern',
    required=True,
    metavar='<metric_pattern>',
    help='list subset of current metrics based on metric pattern')
def list_subset_currennt_metrics(ctx, vapp_name, vm_name, metric_pattern):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.list_current_metrics_subset(metric_pattern=metric_pattern)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('list-historic-metrics', short_help='list historic metrics of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def list_all_historic_metrics(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.list_all_historic_metrics()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('list-sample-historic-data', short_help='list sample historic '
                                                'data of given metric of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'metric_name',
    '--metric-name',
    required=True,
    metavar='<metric_name>',
    help='list sample historic data based on metric name')
def list_sample_historic_metrics(ctx, vapp_name, vm_name, metric_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.list_sample_historic_metric_data(metric_name=metric_name)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command(
    'update-general-setting', short_help='update general setting of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'name',
    '--name',
    required=False,
    default=None,
    metavar='<vm_name>',
    help='vm name')
@click.option(
    'description',
    '--d',
    required=False,
    default=None,
    metavar='<description>',
    help='vm description')
@click.option(
    'computer_name',
    '--cn',
    required=False,
    default=None,
    metavar='<computer_name>',
    help='vm computer name')
@click.option(
    'boot_delay',
    '--bd',
    required=False,
    default=None,
    metavar='<boot_delay>',
    type=click.INT,
    help='boot delay of VM.')
@click.option(
    'enter_bios_setup',
    '--ebs',
    required=False,
    default=None,
    metavar='<enter_bios_setup>',
    type=click.BOOL,
    help='enter bios setup of VM.')
@click.option(
    'storage_policy',
    '--sp',
    required=False,
    default=None,
    metavar='<storage_policy>',
    help='vm storage policy')
def update_general_setting(ctx, vapp_name, vm_name, name, description,
                           computer_name, boot_delay, enter_bios_setup,
                           storage_policy):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vm = _get_vm(ctx, vapp_name, vm_name)
        vdc = _get_vdc(ctx)
        storage_policy_href = None
        if storage_policy is not None:
            storage_policy_href = vdc.get_storage_profile(storage_policy).get(
                'href')
        task = vm.update_general_setting(
            name=name,
            description=description,
            computer_name=computer_name,
            boot_delay=boot_delay,
            enter_bios_setup=enter_bios_setup,
            storage_policy_href=storage_policy_href)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('relocate', short_help='relocate VM to given datastore')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'datastore_id',
    '--datastore-id',
    required=True,
    metavar='<datastore-id>',
    help='datastore id')
def relocate(ctx, vapp_name, vm_name, datastore_id):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.relocate(datastore_id=datastore_id)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('list-os-section', short_help='list operating system section '
                                          'properties of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def list_os_section(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.list_os_section()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command(
    'update-os-section', short_help='update os section properties of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'ovf_info',
    '--ovf-info',
    required=False,
    default=None,
    metavar='<ovf_info>',
    help='ovf info')
@click.option(
    'description',
    '--d',
    required=False,
    default=None,
    metavar='<description>',
    help='description')
def update_os_section(ctx, vapp_name, vm_name, ovf_info, description):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.update_operating_system_section(ovf_info=ovf_info,
                                                  description=description)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('list-gc-section', short_help='list guest customization section '
                                          'properties of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def list_gc_section(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.list_gc_section()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command(
    'update-gc-section', short_help='update guest customization section'
                                    ' properties of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    '--enable/--disable',
    'is_enabled',
    required=False,
    default=None,
    metavar='<bool>',
    help='enable guest customization')
@click.option(
    '--enable-change-sid/--disable-change-sid',
    'is_change_sid',
    required=False,
    default=None,
    metavar='<bool>',
    help='change sid')
@click.option(
    '--enable-join-domain/--disable-join-domain',
    'is_join_domain',
    required=False,
    default=None,
    metavar='<bool>',
    help='enable join domain')
@click.option(
    '--enable-use-org-settings/--disable-use-org-settings',
    'is_use_org_settings',
    required=False,
    default=None,
    metavar='<bool>',
    help='enable use org settings')
@click.option(
    '--domain-name',
    'domain_name',
    required=False,
    default=None,
    metavar='<str>',
    help='domain name')
@click.option(
    '--domain-user-name',
    'domain_user_name',
    required=False,
    default=None,
    metavar='<str>',
    help='domain user name')
@click.option(
    '--domain-user-password',
    'domain_user_password',
    required=False,
    default=None,
    metavar='<str>',
    help='domain user password')
@click.option(
    '--enable-admin-password/--disable-admin-password',
    'is_admin_password',
    required=False,
    default=None,
    metavar='<bool>',
    help='enable admin password')
@click.option(
    '--enable-admin-password-auto/--disable-admin-password-auto',
    'is_admin_password_auto',
    required=False,
    default=None,
    metavar='<bool>',
    help='enable admin password auto')
@click.option(
    '--admin-password',
    'admin_password',
    required=False,
    default=None,
    metavar='<str>',
    help='admin password')
@click.option(
    '--enable-admin-auto-logon/--disable-admin-auto-logon',
    'is_admin_auto_logon',
    required=False,
    default=None,
    metavar='<bool>',
    help='enable admin auto logon')
@click.option(
    '--admin-auto-logon-count',
    'admin_auto_logon_count',
    required=False,
    default=0,
    metavar='<int>',
    help='admin auto logon count')
@click.option(
    '--enable-reset-password/--disable-reset-password',
    'is_reset_password',
    required=False,
    default=None,
    metavar='<bool>',
    help='enable reset password')
@click.option(
    '--customization-script',
    'customization_script',
    required=False,
    default=None,
    metavar='<str>',
    help='customization scipt')
def update_gc_section(ctx, vapp_name, vm_name, is_enabled, is_change_sid,
                      is_join_domain, is_use_org_settings, domain_name,
                      domain_user_name, domain_user_password, is_admin_password,
                      is_admin_password_auto, admin_password,
                      is_admin_auto_logon, admin_auto_logon_count,
                      is_reset_password, customization_script):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm. \
            update_guest_customization_section(
            enabled=is_enabled,
            change_sid=is_change_sid,
            join_domain_enabled=is_join_domain,
            use_org_settings=is_use_org_settings,
            domain_name=domain_name,
            domain_user_name=domain_user_name,
            domain_user_password=domain_user_password,
            admin_password_enabled=is_admin_password,
            admin_password_auto=is_admin_password_auto,
            admin_password=admin_password,
            admin_auto_logon_enabled=is_admin_auto_logon,
            admin_auto_logon_count=admin_auto_logon_count,
            reset_password_required=is_reset_password,
            customization_script=customization_script)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('check-post-gc-script', short_help='check post guest customization'
                                          'script of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def check_post_gc_script(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.list_check_post_gc_status()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('list-vm-capabilities', short_help='list VM capabilities section '
                                               'properties')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def list_vm_capabilities(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.list_vm_capabilities()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command(
    'update-vm-capabilities', short_help='update VM capabilities properties')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'enable_memory_hot_add',
    '--enable-memory-hot-add/--disable-memory-hot-add',
    required=False,
    default=None,
    metavar='<bool>',
    help='enable memory hot add')
@click.option(
    'enable_cpu_hot_add',
    '--enable-cpu-hot-add/--disable-cpu-hot-add',
    required=False,
    default=None,
    metavar='<bool>',
    help='enable CPU hot add')
def update_vm_capabilities_section(ctx, vapp_name, vm_name,
                                   enable_memory_hot_add, enable_cpu_hot_add):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm. \
            update_vm_capabilities_section(
            memory_hot_add_enabled=enable_memory_hot_add,
            cpu_hot_add_enabled=enable_cpu_hot_add)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('list-runtime-info', short_help='list runtime info properties'
                                            ' of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def list_runtime_info(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.list_run_time_info()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('list-boot-options', short_help='list boot options properties'
                                            ' of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def list_boot_options(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.list_boot_options()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command(
    'update-boot-options', short_help='update boot options properties')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'boot_delay',
    '--bool-delay',
    required=False,
    default=None,
    metavar='<int>',
    help='boot delay option')
@click.option(
    'enter_bios_setup',
    '--enable-enter-bios-setup/--disable-enter-bios-setup',
    required=False,
    default=None,
    metavar='<bool>',
    help='enable enter bios set-up')
def update_boot_options(ctx, vapp_name, vm_name,
                                   boot_delay, enter_bios_setup):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        task = vm.update_boot_options(boot_delay=boot_delay,
                                      enter_bios_setup=enter_bios_setup)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('list-metadata', short_help='list metadata of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def show_metadata(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = metadata_to_dict(vm.get_metadata())
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('set-metadata', short_help='set an entity as metadata of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'domain',
    '--domain',
    type=click.Choice(['GENERAL', 'SYSTEM']),
    required=True,
    metavar='<domain>',
    help='domain')
@click.option(
    'visibility',
    '--visibility',
    type=click.Choice(['PRIVATE', 'READONLY', 'READWRITE']),
    required=True,
    metavar='<visibility>',
    help='visibility')
@click.option(
    'value_type',
    '--value-type',
    type=click.Choice(
        ['MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue',
         'MetadataDateTimeValue']),
    required=True,
    metavar='<value_type>',
    help='value_type')
@click.option(
    'key',
    '--key',
    required=True,
    metavar='<key>',
    help='key')
@click.option(
    'value',
    '--value',
    required=True,
    metavar='<value>',
    help='value')
def set_metadata(ctx, vapp_name, vm_name, domain, visibility, value_type, key,
                 value):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.set_metadata(domain=domain,
                                 visibility=visibility,
                                 key=key,
                                 value=value,
                                 metadata_type=value_type)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('update-metadata', short_help='update metadata of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'domain',
    '--domain',
    type=click.Choice(['GENERAL', 'SYSTEM']),
    required=True,
    metavar='<domain>',
    help='domain')
@click.option(
    'visibility',
    '--visibility',
    type=click.Choice(['PRIVATE', 'READONLY', 'READWRITE']),
    required=True,
    metavar='<visibility>',
    help='visibility')
@click.option(
    'value_type',
    '--value-type',
    type=click.Choice(
        ['MetadataStringValue', 'MetadataNumberValue', 'MetadataBooleanValue',
         'MetadataDateTimeValue']),
    required=True,
    metavar='<value_type>',
    help='value_type')
@click.option(
    'key',
    '--key',
    required=True,
    metavar='<key>',
    help='key')
@click.option(
    'value',
    '--value',
    required=True,
    metavar='<value>',
    help='value')
def update_metadata(ctx, vapp_name, vm_name, domain, visibility, value_type,
                    key,
                    value):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.set_metadata(domain=domain,
                                 visibility=visibility,
                                 key=key,
                                 value=value,
                                 metadata_type=value_type)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('remove-metadata', short_help='remove metadata of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'domain',
    '--domain',
    type=click.Choice(['GENERAL', 'SYSTEM']),
    required=True,
    metavar='<domain>',
    help='domain')
@click.option(
    'key',
    '--key',
    required=True,
    metavar='<key>',
    help='key')
def remove_metadata(ctx, vapp_name, vm_name, domain, key):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.remove_metadata(domain=MetadataDomain(domain),
                                    key=key)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('list-screen-ticket', short_help='list screen ticket of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def list_screen_ticket(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.list_screen_ticket()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('list-mks-ticket', short_help='list mks ticket of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def list_mks_ticket(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.list_mks_ticket()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('list-product-sections', short_help='list product sections of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def list_product_sections(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.list_product_sections()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('update-vhs-disk', short_help='update virtual hardware section '
                                          'disk of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'element_name',
    '--e-name',
    required=True,
    metavar='<element-name>',
    help='element name')
@click.option(
    'virtual_quantity',
    '--v-quantity',
    required=True,
    metavar='<virtual_quantity>',
    help='virtual quantity in bytes')
def update_vhs_disk(ctx, vapp_name, vm_name, element_name, virtual_quantity):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.\
            update_vhs_disks(element_name=element_name,
                             virtual_quatntity_in_bytes=virtual_quantity)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)

@vm.command('update-vhs-media', short_help='update virtual hardware section '
                                          'media of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'element_name',
    '--e-name',
    required=True,
    metavar='<element-name>',
    help='element name')
@click.option(
    'host_resource',
    '--host-resource',
    required=True,
    metavar='<host resource>',
    help='host resource')
def update_vhs_media(ctx, vapp_name, vm_name, element_name, host_resource):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.update_vhs_media(element_name=element_name,
                                     host_resource=host_resource)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('enable-nested-hypervisor', short_help='enable nested hypervisor '
                                                   'of VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def enable_nested_hypervisor(ctx, vapp_name, vm_name):
    try:
        restore_session(ctx, vdc_required=True)
        vm = _get_vm(ctx, vapp_name, vm_name)
        result = vm.enable_nested_hypervisor()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
