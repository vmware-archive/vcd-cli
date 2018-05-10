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

from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import vcd


@vcd.group(short_help='manage NSX-T Managers')
@click.pass_context
def nsxt(ctx):
    """Manage NSX-T Managers in vCloud Director.

\b
    Examples
        vcd nsxt register nsxt-name (for a future release - VCD API vers 31.0)
            --url 'https://<FQDN or IP address> of NSX-T host'
            --user 'nsxt-admin-user-name'
            --password 'nsxt-admin-user-password'
            --desc 'description of nsxt-manager'
    """
    pass


@nsxt.command('register', short_help='register NSX-T Manager')
@click.pass_context
@click.argument('nsxt-name', metavar='<nsxt-name>', required=True)
@click.option(
    '--url',
    required=True,
    default=None,
    metavar='[url]',
    help='https://<FQDN or IP address> of NSX-T host')
@click.option(
    '--user',
    required=True,
    default=None,
    metavar='[user]',
    help='NSX-T admin user name')
@click.option(
    '--password',
    required=False,
    default=None,
    metavar='[password]',
    help='NSX-T admin password')
@click.option(
    '--desc',
    required=False,
    default=None,
    metavar='[desc]',
    help='description of NSX-T Manager')
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
        stdout('NSX-T Manager registered successfully.', ctx)
    except Exception as e:
        stderr(e, ctx)
