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

import os
import re
import unittest
from click.testing import CliRunner

from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.environment import CommonRoles, Environment
from vcd_cli.login import login, logout
from vcd_cli.vcd import vcd, version


class LoginAndVcdTest(BaseTestCase):
    """Test login, logout, help, and version operations.

    Test cases in this module do not have ordering dependencies, hence all
    setup is accomplished using Python unittest setUp and tearDown methods.

    Be aware that the login cases will delete existing sessions.
    """

    def setUp(self):
        """Load configuration and create a click runner to invoke CLI."""
        self._config = Environment.get_config()
        self._host = self._config['vcd']['host']
        self._org = self._config['vcd']['sys_org_name']
        self._admin_user = self._config['vcd']['sys_admin_username']
        self._admin_pass = self._config['vcd']['sys_admin_pass']
        self._logger = Environment.get_default_logger()

        self._runner = CliRunner()

    def tearDown(self):
        """Logout ignoring any errors to ensure test session is gone."""
        self._logout(check_assertions=False)

    def _logout(self, check_assertions=True):
        """Logs out, checking assertions by default"""
        result = self._runner.invoke(logout)
        if check_assertions:
            self.assertEqual(0, result.exit_code)
            self.assertTrue("logged out" in result.output)

    def test_0010_admin_login(self):
        """Login with valid admin credentials succeeds and shows 'logged in' tag
        """
        login_args = [
            self._host, self._org, self._admin_user, "-i",
            "-w", "--password={0}".format(self._admin_pass)
        ]
        result = self._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)
        self._logout()

    def test_0015_tenant_login(self):
        """Login with valid tenant credentials succeeds and shows 'logged in' tag
        """
        org = self._config['vcd']['default_org_name']
        user = Environment.get_username_for_role_in_test_org(
            CommonRoles.VAPP_USER)
        password = self._config['vcd']['default_org_user_password']
        login_args = [
            self._host, org, user, "-i",
            "-w", "--password={0}".format(password)
        ]
        result = self._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)
        self._logout()

    def test_0020_login_with_env_password(self):
        """Login works with password in VCD_PASSWORD environmental variable
        """
        login_args = [self._host, self._org, self._admin_user, "-i", "-w"]
        try:
            os.environ["VCD_PASSWORD"] = self._admin_pass
            result = self._runner.invoke(login, args=login_args)
            self.assertEqual(0, result.exit_code)
            self.assertTrue("logged in" in result.output)
        finally:
            # Pop value to prevent other cases from using it accidentally.
            os.environ.pop("VCD_PASSWORD")

    def test_0025_set_server_version(self):
        """Login can set any API version supported by server
        """
        # Use a pyvcloud client to find out the supported versions.
        client = Environment.get_sys_admin_client()
        server_versions = client.get_supported_versions_list()
        client.logout()

        # Use the aforesaid versions and login/logout to each.
        for server_version in server_versions:
            self._logger.debug(
                "Login using server API version {0}".format(server_version))
            login_args = [
                self._host, self._org, self._admin_user, "-i", "--password",
                self._admin_pass, "-w", "--version", server_version
            ]
            result = self._runner.invoke(login, args=login_args)
            self.assertEqual(0, result.exit_code)
            self.assertTrue("logged in" in result.output)
            self._logout()

    def test_0030_invalid_login(self):
        """Login with valid tenant credentials succeeds and shows 'logged in' tag
        """
        login_args = [
            self._host, self._org, self._admin_user, "-i",
            "-w", "--password={0}".format('invalidpassword')]
        result = self._runner.invoke(login, args=login_args)
        self.assertNotEqual(0, result.exit_code)
        self.assertFalse("logged in" in result.output)

    def test_0040_vcd_help(self):
        """help, -h, and --help options provide vcd command help"""
        for help in ['help', '-h', '--help']:
            res = self._runner.invoke(vcd, args=[help])
            self.assertEqual(0, res.exit_code, msg="Option: " + help)
            self.assertTrue(
                "VMware vCloud Director Command Line Interface" in res.output,
                msg="Option: " + help)

    def test_0050_version(self):
        """vcd version command shows a version string"""
        result = self._runner.invoke(version)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("vcd-cli" in result.output, msg=result.output)
        version_pattern = re.compile('[0-9]+\.[0-3]+\.[0-9]+')
        self.assertTrue(
            version_pattern.search(result.output) is not None,
            msg=result.output)


if __name__ == '__main__':
    unittest.main()
