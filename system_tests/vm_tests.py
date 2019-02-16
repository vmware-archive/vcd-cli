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

from click.testing import CliRunner
from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.environment import Environment

from vcd_cli.login import login, logout
from vcd_cli.vm import vm


class VMTest(BaseTestCase):
    """Test vm-related commands

    Tests cases in this module do not have ordering dependencies,
    so setup is accomplished using Python unittest setUp and tearDown
    methods.

    Be aware that this test will delete existing vcd-cli sessions.
    """

    def setUp(self):
        """Load configuration and create a click runner to invoke CLI."""
        os.environ["LC_ALL"] = "en_US.UTF-8"
        os.environ["LANG"] = "en_US.UTF-8"
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

    def test_0010_vm_list(self):
        """user can list vms
        """
        self._login()
        result = self._runner.invoke(vm, args=['list', 'build-vms'])
        self._logger.debug("VM List: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)

    def test_0020_vm_show_snapshot(self):
        """user can show-snapshot vm
        """
        self._login()
        result = self._runner.invoke(vm, args=['show-snapshot', 'build-vms', 'build-03-422'])
        self._logger.debug("VM Snapshot List: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)

    def test_0030_vm_create_snapshot(self):
        """user can create-snapshot vm
        """
        self._login()
        result = self._runner.invoke(vm, args=['create-snapshot', 'build-vms', 'build-03-422', 'vanilla'])
        self._logger.debug("VM Snapshot Create: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)

    def test_0030_vm_revert_snapshot(self):
        """user can revert-snapshot vm
        """
        self._login()
        result = self._runner.invoke(vm, args=['revert-snapshot', 'build-vms', 'build-03-422'])
        self._logger.debug("VM Snapshot Revert: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)

    def test_0040_vm_remove_snapshot(self):
        """user can remove-snapshot vm
        """
        self._login()
        result = self._runner.invoke(vm, args=['remove-snapshot', 'build-vms', 'build-03-422'])
        self._logger.debug("VM Snapshot Revert: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)

    def test_0050_vm_power_on(self):
        """user can power-on vm
        """
        self._login()
        result = self._runner.invoke(vm, args=['power-on', 'build-vms', 'build-03-422'])
        self._logger.debug("VM Power On: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)

    def test_0060_vm_power_off(self):
        """user can power-off vm
        """
        self._login()
        result = self._runner.invoke(vm, args=['power-off', 'build-vms', 'build-03-422'])
        self._logger.debug("VM Power On: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)

    def test_0070_vm_power_reset(self):
        """user can power-reset vm
        """
        self._login()
        result = self._runner.invoke(vm, args=['power-reset', 'build-vms', 'build-03-422'])
        self._logger.debug("VM Power On: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)

    def test_0080_vm_reboot(self):
        """user can reboot vm
        """
        self._login()
        result = self._runner.invoke(vm, args=['reboot', 'build-vms', 'build-03-422'])
        self._logger.debug("VM Reboot: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)

    def test_0090_vm_shutdown(self):
        """user can shutdown vm
        """
        self._login()
        result = self._runner.invoke(vm, args=['shutdown', 'build-vms', 'build-03-422'])
        self._logger.debug("VM Shutdown: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)
