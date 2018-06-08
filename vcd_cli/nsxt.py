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
from pyvcloud.vcd.platform import Platform
from pyvcloud.vcd.utils import to_dict

from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import vcd


@vcd.group(short_help='manage NSX-T managers')
@click.pass_context
def nsxt(ctx):
    """Manage NSX-T managers in vCloud Director (for VCD API v31.0)

\b
    Examples
        vcd nsxt register nsxt-name
            --url 'https://<FQDN or IP address> of NSX-T host'
            --user 'nsxt-admin-user-name'
            --password 'nsxt-admin-user-password'
            --desc 'description of nsxt-manager'
                Register an NSX-T manager.
\b
        vcd nsxt unregister nsxt-name
            Unregister an NSX-T manager.
\b
        vcd nsxt list
            List all registered NSX-T managers.
    """
    pass


@nsxt.command('register', short_help='register NSX-T manager')
@click.pass_context
@click.argument('nsxt-name', metavar='<nsxt-name>', required=True)
@click.option(
    '-U',
    '--url',
    required=True,
    default=None,
    metavar='[url]',
    help='https://<FQDN or IP address> of NSX-T host')
@click.option(
    '-u',
    '--user',
    required=True,
    default=None,
    metavar='[username]',
    help='NSX-T admin user name')
@click.option(
    '-p',
    '--password',
    required=True,
    default=None,
    metavar='[password]',
    help='NSX-T admin password')
@click.option(
    '-d',
    '--desc',
    required=False,
    default=None,
    metavar='[description]',
    help='description of NSX-T manager')
def register(ctx, nsxt_name, url, user, password, desc):
    try:
        restore_session(ctx)
        client = ctx.obj['client']
        platform = Platform(client)
        platform.register_nsxt_manager(nsxt_manager_name=nsxt_name,
                                       nsxt_manager_url=url,
                                       nsxt_manager_username=user,
                                       nsxt_manager_password=password,
                                       nsxt_manager_description=desc)
        stdout('NSX-T manager registered successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@nsxt.command('unregister', short_help='unregister NSX-T manager')
@click.pass_context
@click.argument('nsxt-name', metavar='<nsxt-name>', required=True)
def unregister(ctx, nsxt_name):
    try:
        restore_session(ctx)
        client = ctx.obj['client']
        platform = Platform(client)
        platform.unregister_nsxt_manager(nsxt_manager_name=nsxt_name)
        stdout('NSX-T manager unregistered successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)


@nsxt.command('list', short_help='list NSX-T managers')
@click.pass_context
def list_nsxt(ctx):
    try:
        restore_session(ctx)
        client = ctx.obj['client']
        platform = Platform(client)
        query = platform.list_nsxt_managers()
        result = []
        for record in list(query):
            result.append(to_dict(record, exclude=['href']))
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
