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
from pyvcloud.vcd.client import API_CURRENT_VERSIONS
from pyvcloud.vcd.client import ApiVersion
from pyvcloud.vcd.client import BasicLoginCredentials
from pyvcloud.vcd.client import Client
from pyvcloud.vcd.client import EntityType
from pyvcloud.vcd.client import get_links
import requests

from vcd_cli import browsercookie
from vcd_cli.profiles import Profiles
from vcd_cli.utils import as_metavar
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import vcd


@vcd.command(short_help='login to vCD')
@click.pass_context
@click.argument('host', metavar='host')
@click.argument('org', metavar='organization')
@click.argument('user', metavar='user')
@click.option(
    '-p',
    '--password',
    prompt=False,
    metavar='<password>',
    confirmation_prompt=False,
    envvar='VCD_PASSWORD',
    hide_input=True,
    help='Password')
@click.option(
    '-V',
    '--version',
    'api_version',
    required=False,
    metavar=as_metavar(API_CURRENT_VERSIONS),
    help='API version')
@click.option(
    '-s/-i',
    '--verify-ssl-certs/--no-verify-ssl-certs',
    required=False,
    default=True,
    help='Verify SSL certificates')
@click.option(
    '-w',
    '--disable-warnings',
    is_flag=True,
    required=False,
    default=False,
    help='Do not display warnings when not verifying SSL ' + 'certificates')
@click.option(
    '-v', '--vdc', required=False, default=None, help='virtual datacenter')
@click.option(
    '-d', '--session-id', required=False, default=None, help='session id')
@click.option(
    '-b',
    '--use-browser-session',
    is_flag=True,
    required=False,
    default=False,
    help='Use browser session')
def login(ctx, user, host, password, api_version, org, verify_ssl_certs,
          disable_warnings, vdc, session_id, use_browser_session):
    """Login to vCloud Director

\b
    Login to a vCloud Director service.
\b
    Examples
        vcd login mysp.com org1 usr1
            Login to host 'mysp.com'.
\b
        vcd login test.mysp.com org1 usr1 -i -w
            Login to a host with self-signed SSL certificate.
\b
        vcd login mysp.com org1 usr1 --use-browser-session
            Login using active session from browser.
\b
        vcd login session list chrome
            List active session ids from browser.
\b
        vcd login mysp.com org1 usr1 \\
            --session-id ee968665bf3412d581bbc6192508eec4
            Login using active session id.
\b
        vcd login mysp.com org1 api_token \\
            --session-id ee968665bf3412d581bbc6192508eec4
            Login using API Access Token (external identity provider - oAuth
            2.0).
\b
    Environment Variables
        VCD_PASSWORD
            If this environment variable is set, the command will use its value
            as the password to login and will not ask for one. The --password
            option has precedence over the environment variable.

    """

    if not verify_ssl_certs:
        if disable_warnings:
            pass
        else:
            click.secho(
                'InsecureRequestWarning: '
                'Unverified HTTPS request is being made. '
                'Adding certificate verification is strongly '
                'advised.',
                fg='yellow',
                err=True)
        requests.packages.urllib3.disable_warnings()

    if host == 'session' and org == 'list':
        sessions = []
        if user == 'chrome':
            cookies = browsercookie.chrome()
            for c in cookies:
                if c.name == 'vcloud_session_id':
                    sessions.append({'host': c.domain, 'session_id': c.value})
        stdout(sessions, ctx)
        return

    client = Client(
        host,
        api_version=api_version,
        verify_ssl_certs=verify_ssl_certs,
        log_file='vcd.log',
        log_requests=True,
        log_headers=True,
        log_bodies=True)
    try:
        if session_id is not None or use_browser_session:
            is_jwt_token = False
            if user == 'api_token':
                oAuthResponse = requests.post(
                    'https://{}/oauth/tenant/{}/token'.format(host, org),
                    data={'grant_type': 'refresh_token',
                          'refresh_token': session_id},
                ).json()
                session_id = oAuthResponse['access_token']
                is_jwt_token = True
            if use_browser_session:
                browser_session_id = None
                cookies = browsercookie.chrome()
                for c in cookies:
                    if c.name == 'vcloud_session_id' and \
                       c.domain == host:
                        browser_session_id = c.value
                        break
                if browser_session_id is None:
                    raise Exception('Session not found in browser.')
                session_id = browser_session_id
            client.rehydrate_from_token(session_id, is_jwt_token)
        else:
            if password is None:
                password = click.prompt('Password', hide_input=True, type=str)
            client.set_credentials(BasicLoginCredentials(user, org, password))

        negotiated_api_version = client.get_api_version()

        profiles = Profiles.load()
        logged_in_org = client.get_org()
        org_href = logged_in_org.get('href')
        vdc_href = ''
        in_use_vdc = ''

        links = []
        if float(negotiated_api_version) < float(ApiVersion.VERSION_33.value):
            links = get_links(logged_in_org, media_type=EntityType.VDC.value)
        else:
            if logged_in_org.get('name') != 'System':
                links = client.get_resource_link_from_query_object(
                    logged_in_org, media_type=EntityType.RECORDS.value,
                    type='vdc')

        if vdc is None:
            if len(links) > 0:
                in_use_vdc = links[0].name
                vdc_href = links[0].href
        else:
            for v in links:
                if vdc == v.name:
                    in_use_vdc = v.name
                    vdc_href = v.href
                    break
            if len(in_use_vdc) == 0:
                raise Exception('VDC not found')

        token = client.get_access_token()
        is_jwt_token = True
        if not token:
            token = client.get_xvcloud_authorization_token()
            is_jwt_token = False

        profiles.update(
            host,
            org,
            user,
            token,
            negotiated_api_version,
            verify_ssl_certs,
            disable_warnings,
            vdc=in_use_vdc,
            org_href=org_href,
            vdc_href=vdc_href,
            log_request=True,
            log_header=True,
            log_body=True,
            vapp='',
            vapp_href='',
            is_jwt_token=is_jwt_token)

        alt_text = f"{user} logged in, org: '{org}', vdc: '{in_use_vdc}'"
        d = {
            'user': user,
            'org': org,
            'vdc': in_use_vdc,
            'logged_in': True
        }
        stdout(d, ctx, alt_text)
    except Exception as e:
        try:
            profiles = Profiles.load()
            profiles.set('token', '')
        except Exception:
            pass
        stderr(e, ctx)


@vcd.command(short_help='logout from vCD')
@click.pass_context
def logout(ctx):
    """Logout from vCloud Director

    """
    try:
        try:
            restore_session(ctx)
            client = ctx.obj['client']
            client.logout()
        except Exception:
            pass
        if ctx is not None and ctx.obj is not None:
            profiles = ctx.obj['profiles']
            profiles.set('token', '')
            stdout('%s logged out.' % (profiles.get('user')), ctx)
        else:
            stderr('Not logged in.', ctx)
    except Exception as e:
        stderr(e, ctx)
