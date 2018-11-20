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

from click.testing import CliRunner

from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.environment import Environment
from vcd_cli.login import login, logout
from vcd_cli.pvdc import pvdc


class TestPVDC(BaseTestCase):
    """Test PVDC related commands."""

    def test_0000_setup(self):
        """Load configuration and create a click runner to invoke CLI."""
        self._config = Environment.get_config()
        TestPVDC._logger = Environment.get_default_logger()
        TestPVDC._pvdc_name = self._config['pvdc']['pvdc_name']
        sp_list = self._config['pvdc']['storage_profiles']
        TestPVDC._storage_profiles = " ".join(str(x) for x in sp_list)
        TestPVDC._runner = CliRunner()
        self._login()

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
        result = TestPVDC._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        TestPVDC._runner.invoke(logout)

    def test_0005_pvdc_list(self):
        result = self._runner.invoke(pvdc, args=['list'])
        TestPVDC._logger.debug("vcd pvdc list: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)

    def test_0010_pvdc_add_storage_profile(self):
        """Admin user can add storage profiles to a PVDC
        """
        result = self._runner.invoke(
            pvdc, args=[
                'add-sp', TestPVDC._pvdc_name, TestPVDC._storage_profiles])
        TestPVDC._logger.debug(
            "vcd pvdc add-sp pvdc_name storage_profiles: {0}".
            format(result.output))
        self.assertEqual(0, result.exit_code)

    def test_0020_pvdc_del_storage_profile(self):
        """Admin user can delete storage profiles from a PVDC
        """
        result = self._runner.invoke(
            pvdc, args=[
                'del-sp', TestPVDC._pvdc_name, TestPVDC._storage_profiles])
        TestPVDC._logger.debug(
            "vcd pvdc del-sp pvdc_name storage_profiles: {0}".
            format(result.output))
        self.assertEqual(0, result.exit_code)

    def test_0098_tearDown(self):
        """Logout ignoring any errors to ensure test session is gone."""
        self._logout()
