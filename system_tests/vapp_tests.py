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

import os

from uuid import uuid1
from click.testing import CliRunner

from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.environment import CommonRoles
from pyvcloud.system_test_framework.environment import Environment
from pyvcloud.system_test_framework.utils import create_vapp_from_template

from pyvcloud.vcd.system import System
from pyvcloud.vcd.vdc import VDC

from vcd_cli.login import login, logout
from vcd_cli.org import org
from vcd_cli.vapp import vapp
from vcd_cli.vdc import vdc
from vcd_cli.vapp_network import network  # NOQA


class VAppTest(BaseTestCase):
    """Test vApp related commands

    Be aware that this test will delete existing vcd-cli sessions.
    """
    _test_vapp_name = 'test_vApp_' + str(uuid1())
    _test_ownername = 'org_admin'

    _vapp_network_name = 'vapp_network_' + str(uuid1())
    _vapp_network_description = 'Test vApp network'
    _vapp_network_cidr = '90.80.70.1/20'
    _vapp_network_dns1 = '8.8.8.8'
    _vapp_network_dns2 = '8.8.8.9'
    _vapp_network_dns_suffix = 'example.com'
    _vapp_network_ip_range = '90.80.70.2-90.80.70.100'
    _vapp_network_new_ip_range = '90.80.70.104-90.80.70.110'
    _vapp_network_description = 'This is test network'
    _vapp_network_update_ip_range = '90.80.70.20-90.80.70.40'
    _new_vapp_network_dns1 = '8.8.8.10'
    _new_vapp_network_dns2 = '8.8.8.11'
    _new_vapp_network_dns_suffix = 'example1.com'
    _description = 'capturing vapp in catalog'
    _ova_file_name = 'test.ova'
    _vapp_copy_name = 'customized_vApp_copy_' + str(uuid1())
    _copy_description = 'Copying a vapp'
    _ovdc_name = 'test_vdc2_ ' + str(uuid1())

    def test_0000_setup(self):
        """Load configuration and create a click runner to invoke CLI."""
        VAppTest._config = Environment.get_config()
        VAppTest._logger = Environment.get_default_logger()
        VAppTest._client = Environment.get_client_in_default_org(
            CommonRoles.ORGANIZATION_ADMINISTRATOR)

        VAppTest._runner = CliRunner()
        default_org = VAppTest._config['vcd']['default_org_name']
        VAppTest._default_org = default_org
        VAppTest._login(self)
        VAppTest._runner.invoke(org, ['use', default_org])
        VAppTest._test_vdc = Environment.get_test_vdc(VAppTest._client)
        VAppTest._test_vapp = create_vapp_from_template(
            VAppTest._client,
            VAppTest._test_vdc,
            VAppTest._test_vapp_name,
            VAppTest._config['vcd']['default_catalog_name'],
            VAppTest._config['vcd']['default_template_file_name'],
            power_on=False,
            deploy=False)
        VAppTest._catalog_name = VAppTest._config['vcd'][
            'default_catalog_name']
        VAppTest._sys_admin_client = Environment.get_sys_admin_client()
        VAppTest._pvdc_name = Environment.get_test_pvdc_name()
        default_ovdc = VAppTest._config['vcd']['default_ovdc_name']
        VAppTest._default_ovdc = default_ovdc

    def test_0010_create_vapp_network(self):
        """Create a vApp network as per configuration stated above."""
        result = VAppTest._runner.invoke(
            vapp,
            args=[
                'network', 'create', VAppTest._test_vapp_name,
                VAppTest._vapp_network_name, '--subnet',
                VAppTest._vapp_network_cidr, '--description',
                VAppTest._vapp_network_description, '--dns1',
                VAppTest._vapp_network_dns1, '--dns2',
                VAppTest._vapp_network_dns2, '--dns-suffix',
                VAppTest._vapp_network_dns_suffix, '--ip-range',
                VAppTest._vapp_network_ip_range
            ])
        self.assertEqual(0, result.exit_code)

    def test_0011_list_available_vapps(self):
        """List available vapps.
        Invoke the command 'vapp list' in
        """
        result = self._runner.invoke(vapp, args=['list'])
        self.assertEqual(0, result.exit_code)

        result = self._runner.invoke(
            vapp, args=['list', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

        result = self._runner.invoke(
            vapp,
            args=[
                'list', '--filter', 'ownerName==' + VAppTest._test_ownername
            ])
        self.assertEqual(0, result.exit_code)

        result = self._runner.invoke(
            vapp,
            args=['list', '--filter', 'name==' + VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

    def test_0020_poweron_vapp(self):
        """Power on the vapp."""
        result = VAppTest._runner.invoke(
            vapp, args=['power-on', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

    def test_0024_stop_vapp(self):
        result = VAppTest._runner.invoke(
            vapp, args=['stop', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

    def test_0025_capture(self):
        result = VAppTest._runner.invoke(
            vapp,
            args=[
                'capture', VAppTest._test_vapp_name, VAppTest._catalog_name,
                '-d', VAppTest._description
            ])
        self.assertEqual(0, result.exit_code)
        result = VAppTest._runner.invoke(
            vapp, args=['power-on', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

    def test_0026_suspend_vapp(self):
        result = VAppTest._runner.invoke(
            vapp, args=['suspend', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

    def test_0027_discard_suspended_state_vapp(self):
        result = VAppTest._runner.invoke(
            vapp, args=['discard-suspended-state', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

    def test_0028_enter_maintenance_mode(self):
        VAppTest._logout(self)
        VAppTest._sys_admin_login(self)
        VAppTest._runner.invoke(org, ['use', VAppTest._default_org])
        result = VAppTest._runner.invoke(
            vapp, args=['enter-maintenance-mode', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

    def test_0029_exit_maintenance_mode(self):
        result = VAppTest._runner.invoke(
            vapp, args=['exit-maintenance-mode', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)
        VAppTest._logout(self)
        VAppTest._login(self)
        VAppTest._runner.invoke(org, ['use', VAppTest._default_org])

    def test_0030_reset_vapp_network(self):
        """Reset a vapp network."""
        result = VAppTest._runner.invoke(
            vapp,
            args=[
                'network', 'reset', VAppTest._test_vapp_name,
                VAppTest._vapp_network_name
            ])
        self.assertEqual(0, result.exit_code)

    def test_0031_update_vapp_network(self):
        """Update a vapp network's name and description."""
        result = VAppTest._runner.invoke(
            vapp,
            args=[
                'network', 'update', VAppTest._test_vapp_name,
                VAppTest._vapp_network_name, '-d',
                VAppTest._vapp_network_description
            ])
        self.assertEqual(0, result.exit_code)

    def test_0035_add_ip_range_to_vapp_network(self):
        """Add I{ range to vapp network."""
        result = VAppTest._runner.invoke(
            vapp,
            args=[
                'network',
                'add-ip-range',
                VAppTest._test_vapp_name,
                VAppTest._vapp_network_name,
                '--ip-range',
                VAppTest._vapp_network_new_ip_range,
            ])
        self.assertEqual(0, result.exit_code)

    def test_0036_update_ip_range_to_vapp_network(self):
        """Update IP range to vapp network."""
        result = VAppTest._runner.invoke(
            vapp,
            args=[
                'network', 'update-ip-range', VAppTest._test_vapp_name,
                VAppTest._vapp_network_name, '--ip-range',
                VAppTest._vapp_network_ip_range, '--new-ip-range',
                VAppTest._vapp_network_update_ip_range
            ])
        self.assertEqual(0, result.exit_code)

    def test_0037_delete_ip_range_to_vapp_network(self):
        """Delete IP range of vapp network."""
        result = VAppTest._runner.invoke(
            vapp,
            args=[
                'network', 'delete-ip-range', VAppTest._test_vapp_name,
                VAppTest._vapp_network_name, '--ip-range',
                VAppTest._vapp_network_new_ip_range
            ])
        self.assertEqual(0, result.exit_code)

    def test_0038_add_dns_to_vapp_network(self):
        """Add DNS details to vapp network."""
        result = VAppTest._runner.invoke(
            vapp,
            args=[
                'network', 'add-dns', VAppTest._test_vapp_name,
                VAppTest._vapp_network_name, '--dns1',
                VAppTest._new_vapp_network_dns1, '--dns2',
                VAppTest._new_vapp_network_dns2, '--dns-suffix',
                VAppTest._new_vapp_network_dns_suffix
            ])
        self.assertEqual(0, result.exit_code)

    def test_0039_list_allocated_ip(self):
        """List allocated IP of vapp network."""
        result = VAppTest._runner.invoke(
            vapp,
            args=[
                'network', 'list-allocated-ip', VAppTest._test_vapp_name,
                VAppTest._vapp_network_name
            ])
        self.assertEqual(0, result.exit_code)

    def test_0044_list_vapp_networks(self):
        """List of vapp networks."""
        result = VAppTest._runner.invoke(
            vapp, args=['network', 'list', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

    def test_0045_delete_vapp_network(self):
        """Delete a vapp network."""
        result = VAppTest._runner.invoke(
            vapp,
            args=[
                'network', 'delete', VAppTest._test_vapp_name,
                VAppTest._vapp_network_name
            ])
        self.assertEqual(0, result.exit_code)

    def test_0050_update_vapp(self):
        """Update a vApp name and description."""
        new_name = VAppTest._test_vapp_name + 'updated'
        new_desc = 'vapp description'
        self._update_vapp_name_desc(VAppTest._test_vapp_name, new_name,
                                    new_desc)
        vapp_resource = VAppTest._client.get_resource(VAppTest._test_vapp)
        self.assertEqual(vapp_resource.Description.text, new_desc)
        self.assertEqual(vapp_resource.get('name'), new_name)
        # reset back to orignal name
        self._update_vapp_name_desc(new_name, VAppTest._test_vapp_name, '')
        vapp_resource = VAppTest._client.get_resource(VAppTest._test_vapp)
        self.assertEqual(vapp_resource.get('name'), VAppTest._test_vapp_name)

    def _update_vapp_name_desc(self, current_name, new_name, new_desc):
        result = VAppTest._runner.invoke(
            vapp,
            args=[
                'update', current_name, '--name', new_name, '--description',
                new_desc
            ])
        self.assertEqual(0, result.exit_code)

    def test_0060_download_ova(self):
        result = VAppTest._runner.invoke(
            vapp, args=['stop', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)
        result = VAppTest._runner.invoke(
            vapp,
            args=[
                'download', VAppTest._test_vapp_name, VAppTest._ova_file_name,
                '-o'
            ])
        self.assertEqual(0, result.exit_code)
        result = VAppTest._runner.invoke(
            vapp, args=['deploy', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

        # Remove downloaded vapp file
        os.remove(VAppTest._ova_file_name)

    def test_0070_upgrade_virtual_hardware(self):
        result = VAppTest._runner.invoke(
            vapp, args=['stop', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

        result = VAppTest._runner.invoke(
            vapp, args=['upgrade-virtual-hardware', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

        result = VAppTest._runner.invoke(
            vapp, args=['deploy', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

    def test_0080_copy_to(self):
        result = VAppTest._runner.invoke(
            vapp,
            args=[
                'copy', VAppTest._test_vapp_name, '-n',
                VAppTest._vapp_copy_name, '-d', VAppTest._copy_description
            ])
        self.assertEqual(0, result.exit_code)
        result_delete = VAppTest._runner.invoke(
            vapp,
            args=['delete', VAppTest._vapp_copy_name, '--yes', '--force'])
        self.assertEqual(0, result_delete.exit_code)

    def _create_org_vdc(self):
        # creating a org vdc
        org = Environment.get_test_org(VAppTest._sys_admin_client)
        storage_profiles = [{
            'name':
            VAppTest._config['vcd']['default_storage_profile_name'],
            'enabled':
            True,
            'units':
            'MB',
            'limit':
            0,
            'default':
            True
        }]
        system = System(
            VAppTest._sys_admin_client,
            admin_resource=VAppTest._sys_admin_client.get_admin())
        netpool_to_use = Environment._get_netpool_name_to_use(system)
        org.create_org_vdc(
            VAppTest._ovdc_name,
            VAppTest._pvdc_name,
            network_pool_name=netpool_to_use,
            network_quota=VAppTest._config['vcd']['default_network_quota'],
            storage_profiles=storage_profiles,
            uses_fast_provisioning=True,
            is_thin_provision=True)

    def test_0090_move_to(self):
        VAppTest._create_org_vdc(self)
        VAppTest._runner.invoke(vdc, ['use', VAppTest._default_ovdc])
        result = VAppTest._runner.invoke(
            vapp, args=['stop', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)
        result = VAppTest._runner.invoke(
            vapp,
            args=['move', VAppTest._test_vapp_name, '-v', VAppTest._ovdc_name])
        self.assertEqual(0, result.exit_code)
        VAppTest._runner.invoke(vdc, ['use', VAppTest._ovdc_name])
        result = VAppTest._runner.invoke(
            vapp,
            args=[
                'move', VAppTest._test_vapp_name, '-v', VAppTest._default_ovdc
            ])
        self.assertEqual(0, result.exit_code)
        VAppTest._runner.invoke(vdc, ['use', VAppTest._default_ovdc])

    def test_0100_create_snapshot(self):
        result = VAppTest._runner.invoke(
            vapp, args=['create-snapshot', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

    def test_0110_revert_to_snapshot(self):
        result = VAppTest._runner.invoke(
            vapp, args=['revert-to-snapshot', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

    def test_0120_snapshot_remove(self):
        result = VAppTest._runner.invoke(
            vapp, args=['remove-snapshot', VAppTest._test_vapp_name])
        self.assertEqual(0, result.exit_code)

    def test_9998_tearDown(self):
        """Delete vApp and logout from the session."""
        result_delete = VAppTest._runner.invoke(
            vapp,
            args=['delete', VAppTest._test_vapp_name, '--yes', '--force'])
        self.assertEqual(0, result_delete.exit_code)
        VAppTest._logout(self)

    def _login(self):
        org = VAppTest._config['vcd']['default_org_name']
        user = Environment.get_username_for_role_in_test_org(
            CommonRoles.ORGANIZATION_ADMINISTRATOR)
        password = VAppTest._config['vcd']['default_org_user_password']
        login_args = [
            VAppTest._config['vcd']['host'], org, user, "-i", "-w",
            "--password={0}".format(password)
        ]
        result = VAppTest._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _sys_admin_login(self):
        org = VAppTest._config['vcd']['sys_org_name']
        user = self._config['vcd']['sys_admin_username']
        password = VAppTest._config['vcd']['sys_admin_pass']
        login_args = [
            VAppTest._config['vcd']['host'], org, user, "-i", "-w",
            "--password={0}".format(password)
        ]
        result = VAppTest._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        VAppTest._runner.invoke(logout)
