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

from utilities.prompt_launcher import PromptLauncher, Prompt
from pyvcloud.vcd.ui_plugin import UiPlugin
from pyvcloud.vcd.ext_generator import ExtGenerator
from pyvcloud.vcd.validator_factory import ValidatorFactory
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.vcd import vcd


def projectPromptsFn():
    prompts = PromptLauncher([
        Prompt(
            "template_path",
            str,
            message="Please enter a valid absolute template path",
            validator=ValidatorFactory.checkForFolderExistence(),
            err_message="The path has to be valid absolute path"
        ),
        Prompt(
            "projectName",
            str,
            message="Project name",
            default="ui_plugin"
        )
    ])

    return prompts.multi_prompt()


def pluginPromptsFn(manifest):
    prompts = PromptLauncher([
        Prompt(
            "urn",
            str,
            message="Plugin urn",
            default=manifest["urn"]
        ),
        Prompt(
            "name",
            str,
            message="Plugin name",
            default=manifest["name"]
        ),
        Prompt(
            "containerVersion",
            str,
            message="Plugin containerVersion",
            default=manifest["containerVersion"]
        ),
        Prompt(
            "version",
            str,
            message="Plugin version",
            default=manifest["version"]
        ),
        Prompt(
            "scope",
            str,
            message="Plugin scope",
            default=manifest["scope"]
        ),
        Prompt(
            "permissions",
            str,
            message="Plugin permissions",
            default=manifest["permissions"]
        ),
        Prompt(
            "description",
            str,
            message="Plugin description",
            default=manifest["description"],
            err_message="""Plugin description has to be greather then 3
                and less then 255 characters""",
            validator=ValidatorFactory.length(0, 255),
        ),
        Prompt(
            "vendor",
            str,
            message="Plugin vendor",
            default=manifest["vendor"]
        ),
        Prompt(
            "license",
            str,
            message="Plugin license",
            default=manifest["license"]
        ),
        Prompt(
            "link",
            str,
            message="Plugin link",
            default=manifest["link"],
            err_message="""The link url is not valid, please enter valid url
                address and with length between 8 - 100 characters.""",
            validator=[
                    ValidatorFactory.length(8, 100),
                    ValidatorFactory.pattern(r'^((http|https)://)')
            ]
        ),
        Prompt("route", str, message="Plugin route",
               default=manifest["route"])
    ])

    return prompts.multi_prompt()


@vcd.group(short_help='Manage UI Extensions')
@click.pass_context
def uiext(ctx):
    """Manage UI Extensions in vCloud Director.

\b
    Examples
        vcd uiext list
            Get list of Extensions for current tenant.
\b
        vcd uiext deploy --publish ( -p ) --preview ( -pr ) --path
            Deploy extension to vCD and if this extension already exists it
            will be replaced and/or be published for all tenants.
            If --preview ( -pr ) flag is provided user will see in his command
            line his UI extension configuration.
            You can specify absolute path to your UI extension root directory
            if not path given current working directory will
            be considered as UI extension root directory.
\b
        vcd uiext delete --all ( -a ) --extension
            Delete specific or all plugins, if no flags or options are
            provided the user will be promped for UI extension id.
    """
    pass


@uiext.command('generate', short_help='generate UI Extension')
@click.pass_context
def generate_extension(ctx):
    try:
        gen = ExtGenerator()
        gen.generate(projectPromptsFn, pluginPromptsFn)
    except Exception as e:
        stderr(e, ctx)


@uiext.command('list', short_help='list UI Extensions')
@click.pass_context
def list_extensions(ctx):
    try:
        restore_session(ctx, vdc_required=False)
        client = ctx.obj['client']
        ui = UiPlugin(client)

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
        restore_session(ctx, vdc_required=False)
        client = ctx.obj['client']
        ui = UiPlugin(client)
        result = None

        if path:
            if os.path.exists(path) is False:
                raise FileNotFoundError()
            result = ui.deploy(path, publish, preview)
        else:
            result = ui.deploy(os.getcwd(), publish, preview)

        if result is not None:
            print(result)
    except Exception as e:
        stderr(e, ctx)


@uiext.command('delete', short_help='Delete one or all extensions from vCD')
@click.pass_context
@click.option('--extension', default=None, help='Enter UI extension id.')
@click.option('--all', '-a', default=False, is_flag=True)
def delete(ctx, extension, all):
    try:
        restore_session(ctx, vdc_required=False)
        client = ctx.obj['client']
        ui = UiPlugin(client)

        ui.delete(specific=extension, deleteAll=all)
    except Exception as e:
        stderr(e, ctx)
