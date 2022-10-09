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
from pyvcloud.vcd.client import QueryResultFormat
from pyvcloud.vcd.client import RESOURCE_TYPES
from pyvcloud.vcd.utils import to_camel_case
from pyvcloud.vcd.utils import to_dict
from tabulate import tabulate

from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.utils import tabulate_names
from vcd_cli.vcd import vcd


@vcd.command(short_help='search resources')
@click.pass_context
@click.argument('resource_type', metavar='[resource-type]', required=False)
@click.option(
    '-f',
    '--filter',
    'query_filter',
    required=False,
    metavar='[query-filter]',
    help='query filter')
@click.option(
    '-t',
    '--fields',
    'fields',
    required=False,
    metavar='[fields]',
    help='fields to show')
@click.option(
    '--show-id/--hide-id',
    'show_id',
    required=False,
    is_flag=True,
    show_default=True,
    default=True,
    help='show id')
@click.option(
    '--sort-asc',
    'sort_asc',
    required=False,
    metavar='[field]',
    help='sort in ascending order on a field')
@click.option(
    '--sort-desc',
    'sort_desc',
    required=False,
    metavar='[field]',
    help='sort in descending order on a field')
@click.option(
    '--sort-next',
    'sort_next',
    required=False,
    metavar='[field]',
    help='--sort_asc or --sort-desc on a second field')
def search(ctx, resource_type, query_filter, fields, show_id, sort_asc, sort_desc, sort_next):
    """Search for resources in vCloud Director.

\b
    Description
        Search for resources of the provided type. Resource type is not case
        sensitive. When invoked without a resource type, list the available
        types to search for. Admin types are only allowed when the user is
        the system administrator. By default result is order by id.
\b
        Filters can be applied to the search.
\b
    Examples
        vcd search
            lists available resource types.
\b
        vcd search task
            Search for all tasks in current organization.
\b
        vcd search task --filter 'status==running'
            Search for running tasks in current organization.
\b
        vcd search admintask --filter 'status==running'
            Search for running tasks in all organizations,
            system administrator only.
\b
        vcd search task --filter 'id==ffb96443-d7f3-4200-825d-0f297388ebc0'
            Search for a task by id
\b
        vcd search vapp
            Search for vApps.
\b
        vcd search vapp -f 'metadata:cse.node.type==STRING:master'
            Search for vApps by metadata.
\b
        vcd search vapp -f \\
        'metadata:vapp.origin.name==STRING:photon-custom-hw11-2.0-304b817.ova'
            Search for vApps instantiated from template
\b
        vcd search vapp -f \\
        'numberOfCpus=gt=4;memoryAllocationMB=gt=10000;storageKB=gt=10000000'
            Search for resource intensive vApps
\b
        vcd search vm
            Search for virtual machines.
\b
        vcd search vm --fields 'name,vdcName,status'
          Search for virtual machines and show only some fields.
\b
        vcd search vm --fields 'name,vdcName,status' --hide-id --sort-asc vdcName
          Search for virtual machines and show only some fields order y vdcName.
\b
        vcd search adminOrgVdc --fields 'name,orgName,providerVdcName' --hide-id --sort-asc name
          Search all vdc and show only some fields order y name.
\b
        vcd search vm --fields 'containerName as containerName(vapp),name,ownerName as owner,isAutoNature as standalone' \\
            --sort-asc containerName --filter 'isVAppTemplate==false' --hide-id
          Search for virtual machines, show only some fields, use 'as' to customize field name.
\b
        vcd search vm --fields 'containerName as vapp,name' --sort-asc containerName --sort-next name --hide-id
          Search for virtual machines and show only some fields.
    """
    result = query(ctx, resource_type, query_filter, fields, sort_asc, sort_desc, sort_next)
    stdout(result, ctx, show_id=show_id, sort_headers=False)


def query(ctx, resource_type=None, query_filter=None, fields=None, sort_asc=None, sort_desc=None, sort_next=None):
    try:
        if resource_type is None:
            click.secho(ctx.get_help())
            click.echo('\nAvailable resource types:')
            click.echo(tabulate(tabulate_names(RESOURCE_TYPES, 4)))
            return
        restore_session(ctx)
        client = ctx.obj['client']
        result = []
        resource_type_cc = to_camel_case(resource_type, RESOURCE_TYPES)
        headers={}
        if fields:
            for f in fields.split(','):
                field, *label = f.split(' as ')
                headers[field] = field
                if label:
                    label = label.pop()
                    headers[field] = label
            fields = ','.join(headers.keys())
        q = client.get_typed_query(
            resource_type_cc,
            query_result_format=QueryResultFormat.ID_RECORDS,
            qfilter=query_filter,
            fields=fields,
            sort_asc=sort_asc,
            sort_desc=sort_desc)
        records = list(q.execute())
        if len(records) == 0:
            result = 'not found'
        else:
            for r in records:
                d = to_dict(r, resource_type=resource_type_cc)
                if headers:
                    d_with_custom_header = { 'id': d.pop('id') }
                    for field, label in headers.items():
                        d_with_custom_header[label] = None
                        if field in d:
                            d_with_custom_header[label] = d.pop(field)
                    d = d_with_custom_header
                result.append(d)
        if sort_next and (sort_asc or sort_desc):
            if sort_asc:
                reverse=False
                sort_key1 = sort_asc
            if sort_desc:
                reverse=True
                sort_key1 = sort_desc
            sort_key2=sort_next
            if sort_key1 in headers:
                sort_key1 = headers[sort_key1]
            if sort_key2 in headers:
                sort_key2 = headers[sort_key2]
            keys = list(result[0].keys())
            if sort_key1 not in keys:
                raise Exception('sort key \'%s\' not in %s' % (sort_key1, keys))
            if sort_key2 not in keys:
                raise Exception('sort_next \'%s\' not in %s' % (sort_key2, keys))
            result=sorted(result, key=lambda d: (d[sort_key1], d[sort_key2]), reverse=reverse)
        elif sort_next:
                raise Exception('sort_next must be used with sort_asc or sort_desc')
        return result
    except Exception as e:
        stderr(e, ctx)
