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
    """

    if ctx.invoked_subcommand is not None:
        try:
            restore_session(ctx)
        except Exception as e:
            stderr(e, ctx)


@pvdc.command('list', short_help='list of provider virtual datacenters')
@click.pass_context
def list_pvdc(ctx):
    try:
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
        client = ctx.obj['client']
        sys_admin_resource = client.get_admin()
        system = System(client, admin_resource=sys_admin_resource)
        pvdc_reference = system.get_provider_vdc(name)
        pvdc = PVDC(
            client,
            href=pvdc_reference.get('href'))
        refs = pvdc.get_vdc_references()
        md = pvdc.get_metadata()
        result = pvdc_to_dict(pvdc.get_resource(), refs, md)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
