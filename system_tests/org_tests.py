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
from vcd_cli.org import org
from vcd_cli.vcd import vcd


class OrgTest(BaseTestCase):
    """Test org-related commands

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

    def test_0010_org_list(self):
        """Admin user can list orgs and see system as well as default org
        """
        default_org = self._config['vcd']['default_org_name']
        self._login()
        result = self._runner.invoke(org, args=['list'])
        self._logger.debug("vcd org list: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)
        self.assertTrue("System" in result.output)
        self.assertTrue(default_org in result.output)

    def test_0020_org_use(self):
        """Admin user can set default org and list vdcs of that org

        This case proves that 'vcd org list' sets the org scope correctly.
        """
        default_org = self._config['vcd']['default_org_name']
        default_vdc = default_org + '-vdc'
        self._login()
        result = self._runner.invoke(org, args=['use', default_org])
        self.assertEqual(0, result.exit_code)
        result2 = self._runner.invoke(vcd, args=['vdc', 'list'])
        self._logger.debug("vcd org list: {0}".format(result2.output))
        self.assertEqual(0, result2.exit_code)
        self.assertTrue(default_vdc in result2.output)

    def test_0030_org_lifecycle(self):
        """vdc org commands can create, enable, disable, and delete and org
        """
        # Use a fixed org name with a randomized description to prove
        # org creation worked.
        test_org = "my_test_org"
        description = "TEST:{0}".format(uuid.uuid1())
        self._login()
        # Ensure that the org does not exist and then create.
        self._runner.invoke(org, args=['delete', test_org])
        res_org = self._runner.invoke(
            org, args=['create', test_org, description])
        self.assertEqual(0, res_org.exit_code)

        # Ensure we can see the org info including the randomized description.
        res_info = self._runner.invoke(org, args=['info', test_org])
        self._logger.debug("vcd org info: {0}".format(res_info.output))
        self.assertEqual(0, res_info.exit_code)
        self.assertTrue(description in res_info.output)

        # Enable and disable the org.
        res_enable = self._runner.invoke(
            org, args=['update', '--enable', test_org])
        self.assertEqual(0, res_enable.exit_code)
        res_disable = self._runner.invoke(
            org, args=['update', '--disable', test_org])
        self.assertEqual(0, res_disable.exit_code)

        # Delete the org.
        res_delete = self._runner.invoke(org, args=['delete', test_org, '-y'])
        self._logger.debug("vcd org delete: {0}".format(res_delete.output))
        self.assertEqual(0, res_delete.exit_code)
