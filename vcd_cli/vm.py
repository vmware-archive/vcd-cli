# vCloud CLI 0.1
#
# Copyright (c) 2016 VMware, Inc. All Rights Reserved.
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
        vcd vm modify_cpu vapp1 vm1 --cpu 2 --core 2
            Modifies the VM 'vm1' in vApp 'vapp1' to be configured
            with 2 cpu and 2 cores .
\b
        vcd vm modify_memory vapp1 vm1 --memory 512
            Modifies the VM 'vm1' in vApp 'vapp1' to be configured
            with the specified memory .
    """

    if ctx.invoked_subcommand is not None:
        try:
            restore_session(ctx)
            if not ctx.obj['profiles'].get('vdc_in_use') or \
               not ctx.obj['profiles'].get('vdc_href'):
                raise Exception('select a virtual datacenter')
        except Exception as e:
            stderr(e, ctx)


@vm.command('list', short_help='list VMs')
@click.pass_context
def list_vms(ctx):
    try:
        raise Exception('not implemented')
    except Exception as e:
        stderr(e, ctx)


@vm.command(short_help='show VM details')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
def info(ctx, vapp_name, vm_name):
    try:
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        result = {}
        result['primary_ip'] = vapp.get_primary_ip(vm_name)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('modify-cpu',
            short_help='Modify the number of cpu/cores in the VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'cpu',
    '--cpu',
    required=True,
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
def modify_cpu(ctx, vapp_name, vm_name, cpu, cores):
    try:
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        vm_resource = vapp.get_vm(vm_name)
        vm = VM(client, resource=vm_resource)
        task = vm.modify_cpu(cpu, cores)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)


@vm.command('modify-memory', short_help='Modify the memory of the VM')
@click.pass_context
@click.argument('vapp-name', metavar='<vapp-name>', required=True)
@click.argument('vm-name', metavar='<vm-name>', required=True)
@click.option(
    'memory',
    '-m',
    '--memory',
    required=True,
    metavar='<memory>',
    type=click.INT,
    help='Memory to configure the VM.')
def modify_memory(ctx, vapp_name, vm_name, memory):
    try:
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        vapp_resource = vdc.get_vapp(vapp_name)
        vapp = VApp(client, resource=vapp_resource)
        vm_resource = vapp.get_vm(vm_name)
        vm = VM(client, resource=vm_resource)
        task = vm.modify_memory(memory)
        stdout(task, ctx)
    except Exception as e:
        stderr(e, ctx)
