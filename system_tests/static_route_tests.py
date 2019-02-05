# VMware vCloud Director Python SDK
# Copyright (c) 2014-2019 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from click.testing import CliRunner

from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.constants.gateway_constants \
    import GatewayConstants
from pyvcloud.system_test_framework.environment import Environment

from vcd_cli.static_route import gateway
from vcd_cli.org import org
from vcd_cli.login import login, logout


class TestStaticRoute(BaseTestCase):
    """Test Static Route functionalities implemented in pyvcloud."""
    # All tests in this module should be run as System Administrator.
    _next_hop = '2.2.3.81'
    _network = '192.169.1.0/24'
    _name = GatewayConstants.name
    _mtu = 1500
    _type = 'User'
    _vnic = 0
    _desc = 'Static Route created'

    def test_0000_setup(self):
        """Add Static Route in the gateway.
        It will trigger the cli command 'services static create'
        """
        self._config = Environment.get_config()
        TestStaticRoute._logger = Environment.get_default_logger()
        TestStaticRoute._runner = CliRunner()
        default_org = self._config['vcd']['default_org_name']
        self._login()
        TestStaticRoute._runner.invoke(org, ['use', default_org])
        result = TestStaticRoute._runner.invoke(
            gateway,
            args=[
                'services', 'static', 'create', TestStaticRoute._name,
                '--type', TestStaticRoute._type, '--network',
                TestStaticRoute._network, '--next-hop',
                TestStaticRoute._next_hop, '--mtu', TestStaticRoute._mtu,
                '--desc', TestStaticRoute._desc, '-v',
                TestStaticRoute._vnic])
        self.assertEqual(0, result.exit_code)

    def _login(self):
        """Logs in using admin credentials"""
        host = self._config['vcd']['host']
        org = self._config['vcd']['sys_org_name']
        admin_user = self._config['vcd']['sys_admin_username']
        admin_pass = self._config['vcd']['sys_admin_pass']
        login_args = [
            host, org, admin_user, "-i", "-w",
            "--password={0}".format(admin_pass)
        ]
        result = TestStaticRoute._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def test_0025_list_static_routes(self):
        """List all static routes on a gateway.

        Invoke the cli command 'services static list'.
        """
        result = TestStaticRoute._runner.invoke(
            gateway,
            args=[
                'services', 'static', 'list',
                TestStaticRoute._name])
        self.assertEqual(0, result.exit_code)

    def test_0098_teardown(self):
        """Will implement with delete."""

    def _logout(self):
        """Logs out current session, ignoring errors"""
        TestStaticRoute._runner.invoke(logout)

    def test_0099_cleanup(self):
        """Release all resources held by this object for testing purposes."""
        self._logout()
