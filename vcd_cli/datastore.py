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
from vcd_cli.vcd import vcd  # NOQA

@vcd.group(short_help='manage datastores')
@click.pass_context
def datastore(ctx):
    """Manage datastores in vCloud Director.

\b
    Examples
        vcd datastore list
            Get list of datastores attached to the vCD system.

    """
    pass


@datastore.command('list', short_help='list datastores')
@click.pass_context
def list_datastores(ctx):
    try:
        restore_session(ctx)
        platform = Platform(ctx.obj['client'])
        result = platform.list_datastores()
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)
