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
from pyvcloud.system_test_framework.utils import create_empty_vapp
from pyvcloud.vcd.client import TaskStatus
from pyvcloud.vcd.vm import VM
from uuid import uuid1
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
    _empty_vapp_name = 'empty_vApp_' + str(uuid1())
    _empty_vapp_description = 'empty vApp description'
    _empty_vapp_runtime_lease = 86400  # in seconds
    _empty_vapp_storage_lease = 86400  # in seconds
    _empty_vapp_owner_name = None
    _empty_vapp_href = None
    _target_vm_name = 'target_vm'
    _idisk_name = 'SCSI'
    _idisk_size = '5242880'
    _idisk_description = '5Mb SCSI disk'

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
        logger = Environment.get_default_logger()

        vdc = Environment.get_test_vdc(VmTest._client)
        logger.debug('Creating empty vApp.')
        VmTest._empty_vapp_href = \
            create_empty_vapp(client=VmTest._client,
                              vdc=vdc,
                              name=VmTest._empty_vapp_name,
                              description=VmTest._empty_vapp_description)

        # Create independent disk
        VmTest._idisk = vdc.create_disk(name=self._idisk_name,
                                        size=self._idisk_size,
                                        description=self._idisk_description)

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

    def test_0025_copy_to(self):
        """Copy VM from one vApp to another."""
        result = VmTest._runner.invoke(
            vm, args=['copy', VAppConstants.name, VAppConstants.vm1_name,
                      '--target-vapp-name', VmTest._empty_vapp_name,
                      '--target-vm-name', VmTest._target_vm_name])
        self.assertEqual(0, result.exit_code)

    def test_0026_move_to(self):
        """Move VM from one vApp to another."""
        test_vapp = VmTest._test_vapp
        test_vapp_resource = test_vapp.get_resource()
        VmTest._test_vapp_name = test_vapp_resource.get('name')
        result = VmTest._runner.invoke(
            vm, args=['move', VmTest._empty_vapp_name, VmTest._target_vm_name,
                      '--target-vapp-name', VmTest._test_vapp_name,
                      '--target-vm-name', VmTest._target_vm_name])
        self.assertEqual(0, result.exit_code)

    def test_0028_delete(self):
        """Delete VM from vApp"""
        result = VmTest._runner.invoke(
            vm, args=['delete', VmTest._test_vapp_name,
                      VmTest._target_vm_name])
        self.assertEqual(0, result.exit_code)

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

    def test_0150_revert_to_snapshot(self):
        """Revert VM to current snapshot."""
        result = VmTest._runner.invoke(
            vm, args=['revert-to-snapshot', VAppConstants.name,
                      VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0160_attach_dsk_to_vm(self):
        """Attach independent disk to VM."""
        vdc = Environment.get_test_vdc(VmTest._client)
        idisk = vdc.get_disk(name=VmTest._idisk_name)
        result = VmTest._runner.invoke(
            vm,
            args=[
                'attach-disk', VAppConstants.name, VAppConstants.vm1_name,
                '--idisk-href',
                idisk.get('href')
            ])
        self.assertEqual(0, result.exit_code)

    def test_0170_deploy_undeploy_vm(self):
        # Undeploy VM
        result = VmTest._runner.invoke(
            vm, args=['undeploy', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        result = VmTest._runner.invoke(
            vm, args=['deploy', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0180_upgrade_virtual_hardware(self):
        # Undeploy VM
        result = VmTest._runner.invoke(
            vm, args=['undeploy', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        # Upgrade virtual hardware of VM.
        result = VmTest._runner.invoke(
            vm,
            args=[
                'upgrade-virtual-hardware', VAppConstants.name,
                VAppConstants.vm1_name
            ])
        self.assertEqual(0, result.exit_code)
        # Again deploy VM for further test cases.
        result = VmTest._runner.invoke(
            vm, args=['deploy', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0190_general_setting_detail(self):
        # general setting details
        result = VmTest._runner.invoke(
            vm,
            args=[
                'general-setting', VAppConstants.name, VAppConstants.vm1_name
            ])
        self.assertEqual(0, result.exit_code)

    def test_0200_list_storage_profile(self):
        result = VmTest._runner.invoke(
            vm,
            args=[
                'list-storage-profile', VAppConstants.name,
                VAppConstants.vm1_name
            ])
        self.assertEqual(0, result.exit_code)

    def test_9998_tearDown(self):
        """Delete the vApp created during setup.

        This test passes if the task for deleting the vApp succeed.
        """
        vapps_to_delete = []

        if VmTest._empty_vapp_href is not None:
            vapps_to_delete.append(VmTest._empty_vapp_name)

        self._sys_login()
        vdc = Environment.get_test_vdc(VmTest._client)
        vdc.delete_disk(name=self._idisk_name)
        self._logout()

        self._login()

        for vapp_name in vapps_to_delete:
            task = vdc.delete_vapp(name=vapp_name, force=True)
            result = VmTest._client.get_task_monitor().wait_for_success(task)
            self.assertEqual(result.get('status'), TaskStatus.SUCCESS.value)


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
