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

import unittest
from click.testing import CliRunner

from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.constants.gateway_constants \
    import GatewayConstants
from pyvcloud.system_test_framework.environment import Environment

from vcd_cli.nat_rule import gateway
from vcd_cli.org import org
from vcd_cli.login import login, logout


class TestNatRule(BaseTestCase):
    """Test Nat Rule functionalities implemented in pyvcloud."""
    # All tests in this module should be run as System Administrator.
    _name = GatewayConstants.name
    _type = 'User'
    _desc = "Created"
    _vnic = 0
    _runner = None
    _snat_action = 'snat'
    _snat_orig_addr = '2.2.3.7'
    _snat_trans_addr = '2.2.3.8'
    _new_snat_desc = 'SNAT Rule Edited'
    _dnat_action = 'dnat'
    _dnat1_orig_addr = '2.2.3.10'
    _dnat1_trans_addr = '2.2.3.11-2.2.3.12'
    _dnat1_protocol = 'tcp'
    _dnat1_orig_port = 80
    _dnat1_trans_port = 80

    def test_0000_setup(self):
        """Adds new ip range present to the sub allocate pool of gateway.
         It will trigger the cli command sub-allocate-ip add
        """
        self._config = Environment.get_config()
        TestNatRule._logger = Environment.get_default_logger()
        TestNatRule._runner = CliRunner()
        default_org = self._config['vcd']['default_org_name']
        self._login()
        TestNatRule._runner.invoke(org, ['use', default_org])
        config = self._config['external_network']
        gateway_sub_allocated_ip_range = \
            config['gateway_sub_allocated_ip_range']
        ext_name = config['name']
        result = TestNatRule._runner.invoke(
            gateway,
            args=[
                'sub-allocate-ip', 'add', TestNatRule._name, '-e',
                ext_name, '--ip-range', gateway_sub_allocated_ip_range])
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
        result = TestNatRule._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def test_0010_add_snat_rule(self):
        """Add SNAT Rule in the gateway.
        It will trigger the cli command services snat create
        """
        result = TestNatRule._runner.invoke(
            gateway,
            args=[
                'services', 'snat', 'create', TestNatRule._name, '--type',
                TestNatRule._type, '-o', TestNatRule._snat_orig_addr, '-t',
                TestNatRule._snat_trans_addr, '--desc', TestNatRule._desc,
                '-v', TestNatRule._vnic])
        self.assertEqual(0, result.exit_code)

    def test_0020_add_snat_rule(self):
        """Add DNAT Rule in the gateway.
        It will trigger the cli command services dnat create
        """
        result = TestNatRule._runner.invoke(
            gateway,
            args=[
                'services', 'dnat', 'create', TestNatRule._name, '--type',
                TestNatRule._type, '-o', TestNatRule._dnat1_orig_addr, '-t',
                TestNatRule._dnat1_trans_addr, '--desc', TestNatRule._desc,
                '-v', TestNatRule._vnic, '--protocol',
                TestNatRule._dnat1_protocol, '-op',
                TestNatRule._dnat1_orig_port, '-tp',
                TestNatRule._dnat1_trans_port])
        self.assertEqual(0, result.exit_code)

    def test_0025_list_nat_rules(self):
        """List all nat rules on a gateway.

        Invoke the cli command 'gateway services nat list' in nat_rule.
        """
        result = TestNatRule._runner.invoke(
            gateway, args=['services', 'nat', 'list', TestNatRule._name])
        self.assertEqual(0, result.exit_code)

    @unittest.skip
    def test_0098_teardown(self):
        """Removes the given IP ranges from existing IP ranges.
         It will trigger the cli command sub-allocate-ip remove
        """
        self._config = Environment.get_config()
        config = self._config['external_network']
        gateway_sub_allocated_ip_range = \
            config['gateway_sub_allocated_ip_range']
        ext_name = config['name']
        result = TestNatRule._runner.invoke(
            gateway,
            args=[
                'sub-allocate-ip', 'remove', TestNatRule._name, '-e',
                ext_name, '-i', gateway_sub_allocated_ip_range])
        self._logger.debug(
            "vcd gateway sub-allocate-ip remove {0}"
            "-e {1} -i {2}".format(
                self._name, ext_name, gateway_sub_allocated_ip_range))
        self.assertEqual(0, result.exit_code)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        TestNatRule._runner.invoke(logout)

    def test_0099_cleanup(self):
        """Release all resources held by this object for testing purposes."""
        self._logout()
