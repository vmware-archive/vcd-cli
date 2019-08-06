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
from pyvcloud.system_test_framework.vapp_constants import VAppConstants
from pyvcloud.system_test_framework.environment import Environment
from pyvcloud.system_test_framework.environment import developerModeAware

from pyvcloud.vcd.client import FenceMode
from pyvcloud.vcd.client import IpAddressMode
from pyvcloud.vcd.client import NetworkAdapterType
from pyvcloud.vcd.client import TaskStatus
from pyvcloud.vcd.vm import VM

from vcd_cli.login import login, logout
from vcd_cli.vapp import vapp
from vcd_cli.org import org


class TestVappNat(BaseTestCase):
    """Test vapp nat functionalities implemented in pyvcloud."""
    _vapp_name = VAppConstants.name
    _vapp_network_name = VAppConstants.network1_name
    _vm_name = VAppConstants.vm1_name
    _org_vdc_network_name = 'test-direct-vdc-network'
    _nat_type_ip_translation = 'ipTranslation'
    _rule_id = '65537'
    _allocate_ip_address = '90.80.70.10'
    _ext_ip_addr = '2.2.3.20'
    _manual = 'manual'

    def test_0000_setup(self):
        self._config = Environment.get_config()
        TestVappNat._logger = Environment.get_default_logger()
        TestVappNat._client = Environment.get_sys_admin_client()
        TestVappNat._runner = CliRunner()
        default_org = self._config['vcd']['default_org_name']
        self._login()
        TestVappNat._runner.invoke(org, ['use', default_org])

        vapp = Environment.get_test_vapp_with_network(TestVappNat._client)
        vapp.reload()
        task = vapp.connect_vapp_network_to_ovdc_network(
            network_name=TestVappNat._vapp_network_name,
            orgvdc_network_name=TestVappNat._org_vdc_network_name)
        result = TestVappNat._client.get_task_monitor().wait_for_success(task)
        self.assertEqual(result.get('status'), TaskStatus.SUCCESS.value)

        vm_resource = vapp.get_vm(TestVappNat._vm_name)
        vm = VM(TestVappNat._client, resource=vm_resource)
        task = vm.add_nic(NetworkAdapterType.E1000.value, True, True,
                          TestVappNat._vapp_network_name,
                          IpAddressMode.MANUAL.value,
                          TestVappNat._allocate_ip_address)
        result = TestVappNat._client.get_task_monitor().wait_for_success(task)
        self.assertEqual(result.get('status'), TaskStatus.SUCCESS.value)
        list_vm_interface = vapp.list_vm_interface(
            TestVappNat._vapp_network_name)
        for vm_interface in list_vm_interface:
            TestVappNat._vm_id = str(vm_interface['Local_id'])
            TestVappNat._vm_nic_id = str(vm_interface['VmNicId'])

    def test_0010_enable_nat_service(self):
        result = TestVappNat._runner.invoke(vapp,
                                            args=[
                                                'network',
                                                'services',
                                                'nat',
                                                'enable-nat',
                                                TestVappNat._vapp_name,
                                                TestVappNat._vapp_network_name,
                                                '--disable',
                                            ])
        self.assertEqual(0, result.exit_code)
        result = TestVappNat._runner.invoke(vapp,
                                            args=[
                                                'network',
                                                'services',
                                                'nat',
                                                'enable-nat',
                                                TestVappNat._vapp_name,
                                                TestVappNat._vapp_network_name,
                                                '--enable',
                                            ])
        self.assertEqual(0, result.exit_code)

    def test_0020_update_nat_type(self):
        result = TestVappNat._runner.invoke(
            vapp,
            args=[
                'network', 'services', 'nat', 'set-nat-type',
                TestVappNat._vapp_name, TestVappNat._vapp_network_name,
                '--type', 'portForwarding', '--policy', 'allowTraffic'
            ])
        self.assertEqual(0, result.exit_code)
        result = TestVappNat._runner.invoke(
            vapp,
            args=[
                'network', 'services', 'nat', 'set-nat-type',
                TestVappNat._vapp_name, TestVappNat._vapp_network_name,
                '--type', 'ipTranslation', '--policy', 'allowTrafficIn'
            ])
        self.assertEqual(0, result.exit_code)

    def test_0030_get_nat_type(self):
        result = TestVappNat._runner.invoke(vapp,
                                            args=[
                                                'network', 'services', 'nat',
                                                'get-nat-type',
                                                TestVappNat._vapp_name,
                                                TestVappNat._vapp_network_name
                                            ])
        self.assertEqual(0, result.exit_code)

    def test_0040_add_nat_rule(self):
        result = TestVappNat._runner.invoke(
            vapp,
            args=[
                'network', 'services', 'nat', 'add', TestVappNat._vapp_name,
                TestVappNat._vapp_network_name, '--type',
                TestVappNat._nat_type_ip_translation, '--vm_id',
                TestVappNat._vm_id, '--nic_id', TestVappNat._vm_nic_id
            ])
        self.assertEqual(0, result.exit_code)

    def test_0050_get_list_of_nat_rule(self):
        result = TestVappNat._runner.invoke(vapp,
                                            args=[
                                                'network', 'services', 'nat',
                                                'list', TestVappNat._vapp_name,
                                                TestVappNat._vapp_network_name
                                            ])
        self.assertEqual(0, result.exit_code)

    def test_0060_update_nat_rule(self):
        result = TestVappNat._runner.invoke(
            vapp,
            args=[
                'network', 'services', 'nat', 'update', TestVappNat._vapp_name,
                TestVappNat._vapp_network_name, TestVappNat._rule_id,
                '--mapping_mode', TestVappNat._manual, '--ext_ip',
                TestVappNat._ext_ip_addr
            ])
        self.assertEqual(0, result.exit_code)

    def test_0090_delete_nat_rule(self):
        result = TestVappNat._runner.invoke(vapp,
                                            args=[
                                                'network', 'services', 'nat',
                                                'delete',
                                                TestVappNat._vapp_name,
                                                TestVappNat._vapp_network_name,
                                                TestVappNat._rule_id
                                            ])
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
        result = TestVappNat._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        TestVappNat._runner.invoke(logout)

    @developerModeAware
    def test_0098_teardown(self):
        """Test the  method vdc.delete_vapp().

        Invoke the method for all the vApps created by setup.

        This test passes if all the tasks for deleting the vApps succeed.
        """
        vdc = Environment.get_test_vdc(TestVappNat._client)
        task = vdc.delete_vapp(name=TestVappNat._vapp_name, force=True)
        result = TestVappNat._client.get_task_monitor().wait_for_success(task)
        self.assertEqual(result.get('status'), TaskStatus.SUCCESS.value)

    def test_0099_cleanup(self):
        """Release all resources held by this object for testing purposes."""
        self._logout()
