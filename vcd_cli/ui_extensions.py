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
import pprint
import os

from utilities.ui_ext.cli_spinners import CliSpinner
from utilities.ui_ext.ext_generator import ExtGenerator
from pyvcloud.vcd.ui_plugin import UiPlugin
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.vcd import vcd


def get_ext_id_dynamically():
    return click.prompt(
        "Enter the id of the UI extension which you want to delete",
        type=str
    )


@vcd.group(short_help='Manage UI Extensions')
@click.pass_context
def uiext(ctx):
    """Manage UI Extensions in vCloud Director.

\b
    Examples
        vcd ext list
            Get list of Extensions for current tenant.
\b
        vcd ext deploy --publish ( -p ) --preview ( -pr ) --path
            Deploy extension to vCD and if this extension already exists it
            will be replaced and/or be published for all tenants.
            If --preview ( -pr ) flag is provided user will see in his command
            line his UI extension configuration.
            You can specify absolute path to your UI extension root directory
            if not path given current working directory will
            be considered as UI extension root directory.
\b
        vcd ext delete --all ( -a ) --extension
            Delete specific or all plugins, if no flags or options are
            provided the user will be promped for UI extension id.
    """
    pass


@uiext.command('generate', short_help='generate UI Extension')
@click.pass_context
def generate_extension(ctx):
    try:
        gen = ExtGenerator()
        gen.generate()
    except Exception as e:
        stderr(e, ctx)


@uiext.command('list', short_help='list UI Extensions')
@click.pass_context
def list_extensions(ctx):
    try:
        spinner = CliSpinner(text="Listing", spinner="dots", placement="right")
        spinner.start()

        restore_session(ctx, vdc_required=False)
        client = ctx.obj['client']
        token = client._session.headers['x-vcloud-authorization']
        base_uri = client._uri.split("/api")[0]
        ui = UiPlugin(base_uri, token)

        spinner.stop()

        pprint.pprint((ui.getUiExtensions().json()))
    except Exception as e:
        stderr(e, ctx)


@uiext.command('deploy', short_help="""Deploy extension to vCD and if this
extension already exists it
will be replaced and/or be published for all tenants""")
@click.pass_context
@click.option('--path', default=None, type=str)
@click.option('--publish', '-p', default=False, is_flag=True)
@click.option('--preview', '-pr', default=False, is_flag=True)
def deploy(ctx, path, publish, preview):
    try:
        spinner = CliSpinner(text="Deploy", spinner="line")
        spinner.start()

        restore_session(ctx, vdc_required=False)
        client = ctx.obj['client']
        token = client._session.headers['x-vcloud-authorization']
        base_uri = client._uri.split("/api")[0]
        ui = UiPlugin(base_uri, token)

        if path:
            if os.path.exists(path) is False:
                spinner.stop()
                raise FileNotFoundError()

            ui.deploy(path, publish, preview)
            spinner.stop("Completed!")
        else:
            ui.deploy(os.getcwd(), publish, preview)
            spinner.stop("Completed!")
    except Exception as e:
        stderr(e, ctx)


@uiext.command('delete', short_help='Delete one or all extensions from vCD')
@click.pass_context
@click.option('--extension', default=None, help='Enter UI extension id.')
@click.option('--all', '-a', default=False, is_flag=True)
def delete(ctx, extension, all):
    try:
        spinner = CliSpinner(text="Delete", spinner="line")
        spinner.start()

        restore_session(ctx, vdc_required=False)
        client = ctx.obj['client']
        token = client._session.headers['x-vcloud-authorization']
        base_uri = client._uri.split("/api")[0]
        ui = UiPlugin(base_uri, token)
        ui.delete(specific=extension, deleteAll=all)
        spinner.stop()
    except Exception as e:
        stderr(e, ctx)
