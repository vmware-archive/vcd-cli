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
from pyvcloud.vcd.client import TaskStatus

from vcd_cli.login import login, logout
from vcd_cli.vapp import vapp
from vcd_cli.org import org


class TestVappFirewall(BaseTestCase):
    """Test vapp firewall functionalities implemented in pyvcloud."""
    _vapp_name = VAppConstants.name
    _vapp_network_name = VAppConstants.network1_name

    def test_0000_setup(self):
        self._config = Environment.get_config()
        TestVappFirewall._logger = Environment.get_default_logger()
        TestVappFirewall._client = Environment.get_sys_admin_client()
        TestVappFirewall._runner = CliRunner()
        default_org = self._config['vcd']['default_org_name']
        self._login()
        TestVappFirewall._runner.invoke(org, ['use', default_org])

        vapp = Environment.get_test_vapp_with_network(TestVappFirewall._client)
        vapp.reload()

        TestVappFirewall._vapp_network_name = \
            Environment.get_default_orgvdc_network_name()
        task = vapp.connect_org_vdc_network(
            TestVappFirewall._vapp_network_name,
            fence_mode=FenceMode.NAT_ROUTED.value)
        result = TestVappFirewall._client.get_task_monitor().wait_for_success(
            task)
        self.assertEqual(result.get('status'), TaskStatus.SUCCESS.value)

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
        result = TestVappFirewall._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        TestVappFirewall._runner.invoke(logout)

    def test_0011_enable_firewall_service(self):
        result = TestVappFirewall._runner.invoke(
            vapp,
            args=[
                'network',
                'services',
                'firewall',
                'enable-firewall',
                TestVappFirewall._vapp_name,
                TestVappFirewall._vapp_network_name,
                '--disable',
            ])
        self.assertEqual(0, result.exit_code)
        result = TestVappFirewall._runner.invoke(
            vapp,
            args=[
                'network',
                'services',
                'firewall',
                'enable-firewall',
                TestVappFirewall._vapp_name,
                TestVappFirewall._vapp_network_name,
                '--enable',
            ])
        self.assertEqual(0, result.exit_code)

    @developerModeAware
    def test_0098_teardown(self):
        """Test the  method vdc.delete_vapp().

        Invoke the method for all the vApps created by setup.

        This test passes if all the tasks for deleting the vApps succeed.
        """
        vdc = Environment.get_test_vdc(TestVappFirewall._client)
        task = vdc.delete_vapp(name=TestVappFirewall._vapp_name, force=True)
        result = TestVappFirewall._client.get_task_monitor().wait_for_success(
            task)
        self.assertEqual(result.get('status'), TaskStatus.SUCCESS.value)

    def test_0099_cleanup(self):
        """Release all resources held by this object for testing purposes."""
        self._logout()
