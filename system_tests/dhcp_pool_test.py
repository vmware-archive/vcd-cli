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
import unittest
from click.testing import CliRunner
from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.constants.gateway_constants \
    import GatewayConstants
from pyvcloud.system_test_framework.environment import Environment
from vcd_cli.dhcp_pool import gateway
from vcd_cli.org import org
from vcd_cli.login import login, logout


class TestDhcpPool(BaseTestCase):
    """Test DHCP Pool functionalities implemented in pyvcloud."""
    # All tests in this module should be run as System Administrator.
    _pool_ip_range = '30.20.10.110-30.20.10.112'
    _gateway_name = GatewayConstants.name
    _pool_id = None

    def test_0000_setup(self):
        """Adds new DHCP pool to the gateway.

         It will trigger the cli command service dhcp-pool create
        """
        self._config = Environment.get_config()
        TestDhcpPool._logger = Environment.get_default_logger()
        TestDhcpPool._runner = CliRunner()
        default_org = self._config['vcd']['default_org_name']
        self._login()
        TestDhcpPool._runner.invoke(org, ['use', default_org])
        result = TestDhcpPool._runner.invoke(
            gateway,
            args=[
                'services', 'dhcp-pool', 'create', TestDhcpPool._gateway_name,
                '-r', TestDhcpPool._pool_ip_range])
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
        result = TestDhcpPool._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def test_0001_list_dhcp_pool(self):
        """List DHCP pool.

         It will trigger the cli command service dhcp-pool list
        """
        result = TestDhcpPool._runner.invoke(
            gateway,
            args=[
                'services', 'dhcp-pool', 'list', TestDhcpPool._gateway_name])
        ip_pool_row = self.get_row_containing_word(result.output,
                                                   TestDhcpPool._pool_ip_range)
        ip_pool_arr = ip_pool_row.strip().split()
        TestDhcpPool._pool_id = ip_pool_arr[1]
        self.assertEqual(0, result.exit_code)

    def test_0002_info_dhcp_pool(self):
        """info about DHCP pool.

         It will trigger the cli command services dhcp-pool info
        """
        result = TestDhcpPool._runner.invoke(
            gateway,
            args=[
                'services', 'dhcp-pool', 'info', TestDhcpPool._gateway_name,
                TestDhcpPool._pool_id])

        self.assertEqual(0, result.exit_code)

    def get_row_containing_word(self, output, word):
        rows = output.split('\n')
        for row in rows:
            if row.find(word) != -1:
                return row

    def test_0098_teardown(self):
        """Delete a DHCP Pool from gateway.

        It will trigger the cli command services dhcp-pool delete
        """
        self._config = Environment.get_config()
        TestDhcpPool._logger = Environment.get_default_logger()
        TestDhcpPool._runner = CliRunner()
        default_org = self._config['vcd']['default_org_name']
        TestDhcpPool._runner.invoke(org, ['use', default_org])
        result = TestDhcpPool._runner.invoke(
            gateway,
            args=[
                'services', 'dhcp-pool', 'delete', TestDhcpPool._gateway_name,
                TestDhcpPool._pool_id])
        self.assertEqual(0, result.exit_code)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        self._runner.invoke(logout)

    def test_0099_cleanup(self):
        """Release all resources held by this object for testing purposes."""
        self._logout()
