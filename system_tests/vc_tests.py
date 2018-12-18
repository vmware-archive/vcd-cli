# VMware vCloud Director vCD CLI
# Copyright (c) 2018 VMware, Inc. All Rights Reserved.
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

import uuid
from click.testing import CliRunner

from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.environment import Environment
from vcd_cli.login import login, logout
from vcd_cli.vc import vc



class VCTest(BaseTestCase):
    """Test vc-related commands

    Tests cases in this module do not have ordering dependencies,
    so setup is accomplished using Python unittest setUp and tearDown
    methods.

    Be aware that this test will delete existing vcd-cli sessions.
    """

    def setUp(self):
        """Load configuration and create a click runner to invoke CLI."""
        self._config = Environment.get_config()
        self._logger = Environment.get_default_logger()

        self._runner = CliRunner()
        self._login()

    def tearDown(self):
        """Logout ignoring any errors to ensure test session is gone."""
        self._logout()

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
        result = self._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        self._runner.invoke(logout)

    def test10_list_available_port_group(self):
        """Fetches the list of available portgroups of a vCenter
        Invoke the command 'vc list-available-port-groups'.
        """
        vc_name = self._config['vc']['vcenter_host_name']

        result = self._runner.invoke(
            vc,
            args=[
                'list-available-port-groups', vc_name
            ])
        self.assertEqual(0, result.exit_code)
