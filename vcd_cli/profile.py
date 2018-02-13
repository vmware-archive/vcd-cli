# vCloud CLI 0.1
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

import click
import yaml

from vcd_cli.profiles import Profiles
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import abort_if_false
from vcd_cli.vcd import vcd


@vcd.group(short_help='manage profiles')
@click.pass_context
def profile(ctx):
    """Manage user profiles

    """
    pass


@profile.command('info', short_help='show details of current profile')
@click.pass_context
def info(ctx):
    try:
        profiles = Profiles.load()
        click.echo(yaml.dump(profiles.data, default_flow_style=False))
    except Exception as e:
        stderr(e, ctx)


@profile.group(short_help='work with vcd-cli extensions')
@click.pass_context
def extension(ctx):
    """Manage vcd-cli extensions.

\b
    Description
        Manages commands added to vcd-cli.
\b
        New commands can be added to vcd-cli as Python modules. The module
        containing the commands implementation needs to be present in the
        Python path.
\b
    Examples
        vcd profile extension list
            List the extension modules currently registered with vcd-cli.
\b
        vcd profile extension add container_service_extension.client.cse
            Add to vcd-cli the commands to work with CSE, located in the
            specified Python module.
\b
        vcd profile extension delete container_service_extension.client.cse
            Removes the CSE commands from vcd-cli.
\b
    Files
        ~/.vcd-cli/profiles.yaml (macOS and Linux)
        %userprofile%/.vcd-cli/profiles.yaml (Windows)
            The extension modules are registered in the profiles file.

    """
    pass


@extension.command('list', short_help='list vcd-cli extensions')
@click.pass_context
def list_extensions(ctx):
    try:
        profiles = Profiles.load()
        if 'extensions' in profiles.data and \
                profiles.data['extensions'] is not None:
            for extension in profiles.data['extensions']:
                click.echo(extension)
    except Exception as e:
        stderr(e, ctx)


@extension.command(short_help='add a vcd-cli extension')
@click.pass_context
@click.argument('module')
def add(ctx, module):
    try:
        profiles = Profiles.load()
        if 'extensions' not in profiles.data or \
                profiles.data['extensions'] is None:
            profiles.data['extensions'] = []
        if module not in profiles.data['extensions']:
            profiles.data['extensions'].append(module)
            profiles.save()
            click.secho('Extension added from module \'%s\'.' % module)
        else:
            raise Exception('module already in the profile')
    except Exception as e:
        stderr('Could not add extension from module \'%s\'' % module, ctx)


@extension.command(short_help='delete a vcd-cli extension')
@click.pass_context
@click.argument('module')
@click.option(
    '-y',
    '--yes',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Are you sure you want to delete the extension?')
def delete(ctx, module):
    try:
        profiles = Profiles.load()
        profiles.data['extensions'].remove(module)
        profiles.save()
        click.secho('Extension from module \'%s\' deleted.' % module)
    except Exception as e:
        stderr('Could not delete extension from module \'%s\'' % module, ctx)


@vcd.command(short_help='current resources in use')
@click.pass_context
def pwd(ctx):
    """Current resources in use

    """
    try:
        restore_session(ctx)
        host = ctx.obj['profiles'].get('host')
        user = ctx.obj['profiles'].get('user')
        in_use_org_name = ctx.obj['profiles'].get('org_in_use')
        in_use_vdc_name = ctx.obj['profiles'].get('vdc_in_use')
        in_use_vapp_name = ctx.obj['profiles'].get('vapp_in_use')
        message = ('connected to %s as \'%s\'\n' +
                   'using org: \'%s\', vdc: \'%s\', vApp: \'%s\'.') % \
                  (host, user, in_use_org_name, in_use_vdc_name,
                   in_use_vapp_name)
        stdout({
            'host': host,
            'user': user,
            'org': in_use_org_name,
            'vdc': in_use_vdc_name,
            'vapp': in_use_vapp_name
        }, ctx, message)
    except Exception as e:
        stderr(e, ctx)
