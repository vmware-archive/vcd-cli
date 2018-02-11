# vCloud CLI 0.1
#
# Copyright (c) 2014 VMware, Inc. All Rights Reserved.
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
from pyvcloud.vcd.vdc import VDC

from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import vcd


@vcd.group(short_help='manage edge gateways')
@click.pass_context
def gateway(ctx):
    """Manage edge gateways in vCloud Director.

\b
    Examples
        vcd gateway list
            Get list of edge gateways in current virtual datacenter.
    """
    pass


@gateway.command('list', short_help='list edge gateways')
@click.pass_context
def list_gateways(ctx):
    try:
        restore_session(ctx, vdc_required=True)
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        result = vdc.list_edge_gateways()
        for e in result:
            del e['href']
        stdout(result, ctx, show_id=False)
    except Exception as e:
        stderr(e, ctx)


@gateway.command(short_help='show edge gateway details')
@click.pass_context
@click.argument('name',
                metavar='<name>',
                required=True)
def info(ctx, name):
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        edge_gateways = vdc.list_edge_gateways()
        for gw in edge_gateways:
            if name == gw.get('name'):
                resource = client.get_resource(gw.get('href'))
                result = edge_gateway_to_dict(resource)
                stdout(result, ctx)
                return
        raise Exception('not found')


def edge_gateway_to_dict(gw):
    result = {}
    result['name'] = gw.get('name')
    result['href'] = gw.get('href')
    return result


@gateway.command(short_help='show edge gateway nat rules')
@click.pass_context
@click.argument('name',
                metavar='<name>',
                required=True)
def natrules(ctx, name):
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        edge_gateways = vdc.list_edge_gateways()
        for gw in edge_gateways:
            if name == gw.get('name'):
                resource = client.get_resource(gw.get('href'))
                result = edge_gateway_nat_rules_to_dict(resource)
                stdout(result, ctx)
                return
        raise Exception('not found')


def edge_gateway_nat_rules_to_dict(gw):
    result = []
    for nr in gw.Configuration.EdgeGatewayServiceConfiguration.NatService.NatRule:
        nrd = {'Id': nr.Id, 'RuleType': nr.RuleType, 'IsEnabled': nr.IsEnabled}
        gnr = nr.GatewayNatRule
        if hasattr(gnr, 'Interface'):
            nrd['Interface'] = gnr.Interface.get('name')
        if hasattr(gnr, 'OriginalIp'):
            nrd['OriginialIp'] = gnr.OriginalIp
        if hasattr(gnr, 'OriginalPort'):
            nrd['OriginialPort'] = gnr.OriginalPort
        if hasattr(gnr, 'TranslatedIp'):
            nrd['TranslatedIp'] = gnr.TranslatedIp
        if hasattr(gnr, 'TranslatedPort'):
            nrd['TranslatedPort'] = gnr.TranslatedPort
        if hasattr(gnr, 'Protocol'):
            nrd['Protocol'] = gnr.Protocol
        result.append(nrd)
    return result


@gateway.command(short_help='show edge gateway firewall rules')
@click.pass_context
@click.argument('name',
                metavar='<name>',
                required=True)
def firewallrules(ctx, name):
        client = ctx.obj['client']
        vdc_href = ctx.obj['profiles'].get('vdc_href')
        vdc = VDC(client, href=vdc_href)
        edge_gateways = vdc.list_edge_gateways()
        for gw in edge_gateways:
            if name == gw.get('name'):
                resource = client.get_resource(gw.get('href'))
                result = edge_gateway_firewall_rules_to_dict(resource)
                stdout(result, ctx)
                return
        raise Exception('not found')


def edge_gateway_firewall_rules_to_dict(gw):
    result = []
    for fr in gw.Configuration.EdgeGatewayServiceConfiguration.FirewallService.FirewallRule:
        frd = {'Id': fr.Id, 'IsEnabled': fr.IsEnabled, 'Policy': fr.Policy}
        if hasattr(fr, 'Description'):
            frd['Description'] = fr.Description
        protocols = ""
        if hasattr(fr.Protocols, 'Tcp'):
            protocols += 'tcp '
        if hasattr(fr.Protocols, 'Udp'):
            protocols += 'udp '
        if hasattr(fr.Protocols, 'Icmp'):
            protocols += 'icmp '
        if hasattr(fr.Protocols, 'Any'):
            protocols += 'any'
        frd['Protocols'] = protocols
        if hasattr(fr, 'Port'):
            if fr.Port == -1:
                frd['Port'] = 'Any'
            else:
                frd['Port'] = fr.Port
        if hasattr(fr, 'DestinationPortRange'):
            frd['DestinationPortRange'] = fr.DestinationPortRange
        if hasattr(fr, 'DestinationIp'):
            frd['DestinationIp'] = fr.DestinationIp
        if hasattr(fr, 'SourcePort'):
            if fr.SourcePort == -1:
                frd['SourcePort'] = 'Any'
            else:
                frd['SourcePort'] = fr.SourcePort
        if hasattr(fr, 'SourcePortRange'):
            frd['SourcePortRange'] = fr.SourcePortRange
        if hasattr(fr, 'SourceIp'):
            frd['SourceIp'] = fr.SourceIp
        if hasattr(fr, 'EnableLogging'):
            frd['EnableLogging'] = fr.EnableLogging
        result.append(frd)
    return result
