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
        vcd vm suspend vapp1 vm1
            Suspend the VM.

\b
        vcd vm discard-suspend vapp1 vm1
            Discard suspended state of the VM.

\b
        vcd vm reset vapp1 vm1
            Reset the VM.
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
