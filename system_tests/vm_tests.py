# VMware vCloud Director vCD CLI
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.
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
from pyvcloud.system_test_framework.vapp_constants import VAppConstants
from pyvcloud.system_test_framework.environment import CommonRoles
from pyvcloud.system_test_framework.environment import Environment
from pyvcloud.vcd.vm import VM

from vcd_cli.login import login, logout
from vcd_cli.org import org
from vcd_cli.vm import vm

import re


class VmTest(BaseTestCase):
    """Test VM related commands

    Be aware that this test will delete existing vcd-cli sessions.
    """
    DEFAULT_ADAPTER_TYPE = 'VMXNET3'
    DEFAULT_IP_MODE = 'POOL'

    def test_0000_setup(self):
        """Load configuration and create a click runner to invoke CLI."""
        VmTest._config = Environment.get_config()
        VmTest._logger = Environment.get_default_logger()
        VmTest._client = Environment.get_client_in_default_org(
            CommonRoles.ORGANIZATION_ADMINISTRATOR)
        VmTest._media_resource = Environment.get_test_media_resource()

        VmTest._runner = CliRunner()
        default_org = VmTest._config['vcd']['default_org_name']
        VmTest._login(self)
        VmTest._runner.invoke(org, ['use', default_org])
        VmTest._test_vdc = Environment.get_test_vdc(VmTest._client)
        VmTest._test_vapp = Environment.get_test_vapp_with_network(
            VmTest._client)
        VmTest._test_vm = VM(
            VmTest._client,
            href=VmTest._test_vapp.get_vm(VAppConstants.vm1_name).get('href'))

    def test_0010_info(self):
        """Get info of the VM."""
        result = VmTest._runner.invoke(
            vm, args=['info', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        # verify output
        vm_name_regex = r"name\s*%s" % VAppConstants.vm1_name
        vapp_regex = r"vapp\s*%s" % VAppConstants.name
        # finall returns a list. checking that list is not empty.
        self.assertTrue(re.findall(vm_name_regex, result.output))
        self.assertTrue(re.findall(vapp_regex, result.output))

    def test_0020_consolidate(self):
        """Consolidate the VM."""
        default_org = self._config['vcd']['default_org_name']
        self._sys_login()
        VmTest._runner.invoke(org, ['use', default_org])
        result = VmTest._runner.invoke(
            vm, args=['consolidate', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        #logging out sys_client
        self._logout()
        #logging with org admin user
        self._login()

    def test_0030_power_on(self):
        """Power on the VM."""
        result = VmTest._runner.invoke(
            vm, args=['power-on', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0032_reboot(self):
        """Reboot the VM."""
        result = VmTest._runner.invoke(
            vm, args=['reboot', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0034_shutdown(self):
        """Shutdown the VM."""
        result = VmTest._runner.invoke(
            vm, args=['shutdown', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        # Again power on VM for further test cases.
        result = VmTest._runner.invoke(
            vm, args=['power-on', VAppConstants.name, VAppConstants.vm1_name])

    def test_0040_power_off(self):
        """Power off the VM."""
        result = VmTest._runner.invoke(
            vm, args=['power-off', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        # Again power on VM for further test cases.
        result = VmTest._runner.invoke(
            vm, args=['power-on', VAppConstants.name, VAppConstants.vm1_name])

    def test_0050_reset(self):
        """Reset the VM."""
        result = VmTest._runner.invoke(
            vm, args=['reset', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0060_suspend(self):
        """Suspend the VM."""
        result = VmTest._runner.invoke(
            vm, args=['suspend', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0070_discard_suspended_state(self):
        """Discard suspended state of the VM."""
        result = VmTest._runner.invoke(
            vm, args=['discard-suspend', VAppConstants.name,
                      VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0080_install_vmware_tools(self):
        """Install vmware tools in the VM."""
        result = VmTest._runner.invoke(
            vm, args=['power-on', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        result = VmTest._runner.invoke(
            vm, args=['install-vmware-tools', VAppConstants.name,
                      VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0090_insert_cd(self):
        """Insert CD in the VM."""
        media_href = VmTest._media_resource.Entity.get('href')
        result = VmTest._runner.invoke(
            vm, args=['insert-cd', VAppConstants.name, VAppConstants.vm1_name,
                      '--media-href', media_href])
        self.assertEqual(0, result.exit_code)

    def test_0100_eject_cd(self):
        """Eject CD from the VM."""
        media_href = VmTest._media_resource.Entity.get('href')
        result = VmTest._runner.invoke(
            vm, args=['eject-cd', VAppConstants.name, VAppConstants.vm1_name,
                      '--media-href', media_href])
        self.assertEqual(0, result.exit_code)

    def test_0110_add_nic(self):
        """Add a nic to the VM."""
        result = VmTest._runner.invoke(
            vm,
            args=[
                'add-nic', VAppConstants.name, VAppConstants.vm1_name,
                '--adapter-type', VmTest.DEFAULT_ADAPTER_TYPE, '--connect',
                '--primary', '--network', VAppConstants.network1_name,
                '--ip-address-mode', VmTest.DEFAULT_IP_MODE
            ])
        self.assertEqual(0, result.exit_code)

    def test_0120_list_nics(self):
        """List all nics of the VM."""
        result = VmTest._runner.invoke(
            vm, args=['list-nics', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0130_delete_nic(self):
        """Delete a nic of the VM."""
        result = VmTest._runner.invoke(
            vm,
            args=[
                'delete-nic', VAppConstants.name, VAppConstants.vm1_name,
                '--index', 0
            ])
        self.assertEqual(0, result.exit_code)

    def test_0140_create_snapshot(self):
        """Create snapshot of VM"""
        result = VmTest._runner.invoke(
            vm, args=['create-snapshot', VAppConstants.name,
                      VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_9998_tearDown(self):
        """logout from the session."""
        VmTest._logout(self)

    def _login(self):
        org = VmTest._config['vcd']['default_org_name']
        user = Environment.get_username_for_role_in_test_org(
            CommonRoles.ORGANIZATION_ADMINISTRATOR)
        password = VmTest._config['vcd']['default_org_user_password']
        login_args = [
            VmTest._config['vcd']['host'], org, user, "-i", "-w",
            "--password={0}".format(password)
        ]
        result = VmTest._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _sys_login(self):
        """Logs in using admin credentials"""
        host = self._config['vcd']['host']
        org = self._config['vcd']['sys_org_name']
        admin_user = self._config['vcd']['sys_admin_username']
        admin_pass = self._config['vcd']['sys_admin_pass']
        login_args = [
            host, org, admin_user, "-i", "-w",
            "--password={0}".format(admin_pass)
        ]
        result = VmTest._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        VmTest._runner.invoke(logout)
