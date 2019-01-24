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

from vcd_cli.org import org
from vcd_cli.login import login, logout
from vcd_cli.firewall_rule import gateway


class TestFirewallRule(BaseTestCase):
    """Adds new firewall rule in the gateway. It will trigger the cli command
    firewall create.
    """
    __name = GatewayConstants.name
    __firewall_rule_name = 'rule1'

    def test_0000_setup(self):

        self._config = Environment.get_config()
        TestFirewallRule._logger = Environment.get_default_logger()
        TestFirewallRule._runner = CliRunner()
        default_org = self._config['vcd']['default_org_name']
        self._login()
        TestFirewallRule._runner.invoke(org, ['use', default_org])
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'create', TestFirewallRule.__name,
                '--name', TestFirewallRule.__firewall_rule_name, '--action',
                'accept', '--type', 'User', '--enabled', '--logging-enabled'])
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
        result = TestFirewallRule._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        TestFirewallRule._runner.invoke(logout)

    def test_0099_cleanup(self):
        """Release all resources held by this object for testing purposes."""
        self._logout()
