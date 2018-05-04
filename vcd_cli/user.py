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

import click
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.utils import to_dict

from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import abort_if_false
from vcd_cli.vcd import vcd


@vcd.group(short_help='work with users in current organization')
@click.pass_context
def user(ctx):
    """Work with users in current organization.

\b
    Examples
        vcd user create my-user my-password role-name
           create user in the current organization with my-user password
           and role-name.
\b
        vcd user create 'my user' 'my password' 'role name'
           create user in the current organization with 'my user'
           'my password' and 'role name'.
\b
        vcd user delete 'my user'
           deletes user with username "my user" from the current organization.
           Will also delete vApps owned by the user. If user has running vApps,
           this command will result in error.
\b
        vcd user update 'my user' --enable
           update user in the current organization, e.g enable the user
\b
        vcd user list
            Get list of users in the current organization.

    """
    pass


@user.command(short_help='create user in current organization')
@click.pass_context
@click.argument('user_name', metavar='<user_name>', required=True)
@click.argument('password', metavar='<password>', required=True)
@click.argument('role_name', metavar='<role-name>', required=True)
@click.option(
    '-e',
    '--email',
    required=False,
    default='',
    metavar='[email]',
    help='User\'s email address.')
@click.option(
    '-f',
    '--full-name',
    required=False,
    default='',
    metavar='[full_name]',
    help='Full name of the user.')
@click.option(
    '-D',
    '--description',
    required=False,
    default='',
    metavar='[description]',
    help='description.')
@click.option(
    '-t',
    '--telephone',
    required=False,
    default='',
    metavar='[telephone]',
    help='User\'s telephone number.')
@click.option(
    '-i',
    '--im',
    required=False,
    default='',
    metavar='[im]',
    help='User\'s im address.')
@click.option(
    '-E',
    '--enabled',
    is_flag=True,
    required=False,
    default=False,
    metavar='[enabled]',
    help='Enable user')
@click.option(
    '--alert-enabled',
    is_flag=True,
    required=False,
    default=False,
    metavar='[alert_enabled]',
    help='Enable alerts')
@click.option(
    '--alert-email',
    required=False,
    default='',
    metavar='[alert_email]',
    help='Alert email address')
@click.option(
    '--alert-email-prefix',
    required=False,
    default='',
    metavar='[alert_email_prefix]',
    help='String to prepend to the alert message subject line')
@click.option(
    '--external',
    is_flag=True,
    required=False,
    default=False,
    metavar='[is_external]',
    help='Indicates if user is imported from an external source')
@click.option(
    '--default-cached',
    is_flag=True,
    required=False,
    default=False,
    metavar='[default_cached]',
    help='Indicates if user should be cached')
@click.option(
    '-g',
    '--group-role',
    is_flag=True,
    required=False,
    default=False,
    metavar='[is_group_role]',
    help='Indicates if the user has a group role')
@click.option(
    '-s',
    '--stored-vm-quota',
    required=False,
    default=0,
    metavar='[stored_vm_quota]',
    help='Quota of vApps that this user can store')
@click.option(
    '-d',
    '--deployed-vm-quota',
    required=False,
    default=0,
    metavar='[deployed_vm_quota]',
    help='Quota of vApps that this user can deploy concurrently')
def create(ctx, user_name, password, role_name, full_name, description, email,
           telephone, im, enabled, alert_enabled, alert_email,
           alert_email_prefix, external, default_cached, group_role,
           stored_vm_quota, deployed_vm_quota):
    try:
        if len(password) < 6:
            raise Exception('Password must be at least 6 characters long.')
        restore_session(ctx)
        client = ctx.obj['client']
        in_use_org_href = ctx.obj['profiles'].get('org_href')
        org = Org(client, in_use_org_href)
        role = org.get_role_record(role_name)
        role_href = role.get('href')
        result = org.create_user(
            user_name=user_name,
            password=password,
            role_href=role_href,
            full_name=full_name,
            description=description,
            email=email,
            telephone=telephone,
            im=im,
            alert_email=alert_email,
            alert_email_prefix=alert_email_prefix,
            stored_vm_quota=stored_vm_quota,
            deployed_vm_quota=deployed_vm_quota,
            is_group_role=group_role,
            is_default_cached=default_cached,
            is_external=external,
            is_alert_enabled=alert_enabled,
            is_enabled=enabled)
        stdout('User \'%s\' is successfully created.' % result.get('name'),
               ctx)
    except Exception as e:
        stderr(e, ctx)


@user.command(short_help='delete an user in current organization')
@click.pass_context
@click.argument('user_name', metavar='<user_name>', required=True)
@click.option(
    '-y',
    '--yes',
    is_flag=True,
    callback=abort_if_false,
    expose_value=False,
    prompt='Deleting an user will also delete all assets '
    '(e.g. vApps, vms, catalogs etc.) owned by the user.'
    ' Are you sure you want to delete the user?')
def delete(ctx, user_name):
    try:
        restore_session(ctx)
        client = ctx.obj['client']
        in_use_org_href = ctx.obj['profiles'].get('org_href')
        org = Org(client, in_use_org_href)
        org.delete_user(user_name)
        stdout('User \'%s\' has been successfully deleted.' % user_name, ctx)
    except Exception as e:
        stderr(e, ctx)


@user.command(short_help='update an user in current organization')
@click.pass_context
@click.argument('user_name', metavar='<user_name>', required=True)
@click.option(
    '--enable/--disable',
    'is_enabled',
    default=None,
    help='enable/disable the user')
def update(ctx, user_name, is_enabled):
    try:
        restore_session(ctx)
        client = ctx.obj['client']
        in_use_org_href = ctx.obj['profiles'].get('org_href')
        org = Org(client, in_use_org_href)
        result = org.update_user(user_name=user_name, is_enabled=is_enabled)
        stdout('User \'%s\' is successfully updated.' % result.get('name'),
               ctx)
    except Exception as e:
        stderr(e, ctx)


@user.command('list', short_help='list users')
@click.pass_context
@click.option(
    '-o',
    '--org',
    'org_name',
    required=False,
    metavar='[org-name]',
    help='name of the org',
)
def list_users(ctx, org_name):
    try:
        restore_session(ctx)
        client = ctx.obj['client']
        if org_name is not None:
            org_href = client.get_org_by_name(org_name).get('href')
        else:
            org_href = ctx.obj['profiles'].get('org_href')
        org = Org(client, href=org_href)
        users = org.list_users()
        result = []
        for record in list(users):
            result.append(
                to_dict(
                    record,
                    exclude=[
                        'org', 'orgName', 'deployedVMQuotaRank',
                        'storedVMQuotaRank'
                    ]))
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
