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
    _snat_orig_addr = '2.2.3.80'
    _snat_trans_addr = '2.2.3.81'
    _new_snat_desc = 'Updated SNAT Rule'
    _new_snat_orig_addr = '2.2.3.86'
    _new_snat_trans_addr = '2.2.3.87'
    _dnat_action = 'dnat'
    _dnat1_orig_addr = '2.2.3.82'
    _dnat1_trans_addr = '2.2.3.83-2.2.3.85'
    _dnat1_protocol = 'tcp'
    _dnat1_orig_port = 80
    _dnat1_trans_port = 80
    _new_dnat1_orig_addr = '2.2.3.90'
    _new_dnat1_trans_addr = '2.2.3.91-2.2.3.93'
    _new_dnat1_protocol = 'udp'
    _new_dnat1_desc = 'Updated DNAT Rule'
    _snat_id = None
    _dnat_id = None
    _index = 1

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
        It will trigger the cli command 'services nat create-snat'
        """
        result = TestNatRule._runner.invoke(
            gateway,
            args=[
                'services', 'nat', 'create-snat', TestNatRule._name, '--type',
                TestNatRule._type, '-o', TestNatRule._snat_orig_addr, '-t',
                TestNatRule._snat_trans_addr, '--desc', TestNatRule._desc,
                '--vnic', TestNatRule._vnic, '--enabled', '--logging-enabled'])
        self.assertEqual(0, result.exit_code)

    def test_0020_add_snat_rule(self):
        """Add DNAT Rule in the gateway.
        It will trigger the cli command 'services nat create-dnat'
        """
        result = TestNatRule._runner.invoke(
            gateway,
            args=[
                'services', 'nat', 'create-dnat', TestNatRule._name, '--type',
                TestNatRule._type, '-o', TestNatRule._dnat1_orig_addr, '-t',
                TestNatRule._dnat1_trans_addr, '--desc', TestNatRule._desc,
                '--vnic', TestNatRule._vnic, '--protocol',
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
        TestNatRule._snat_id = self.get_row_containing_word(
            result.output,
            TestNatRule._snat_action)

        TestNatRule._dnat_id = self.get_row_containing_word(
            result.output,
            TestNatRule._dnat_action)

    def test_0030_info_nat_rule(self):
        """Get the details of nat rule.

        Invoke the cli command 'services nat info' in nat_rule.
        """
        result = TestNatRule._runner.invoke(
            gateway,
            args=[
                'services', 'nat', 'info', TestNatRule._name,
                TestNatRule._snat_id])
        self.assertEqual(0, result.exit_code)

    def test_0035_update_snat_rule(self):
        """Update SNAT Rule in the gateway.
        It will trigger the cli command 'services nat update-snat'
        """
        result = TestNatRule._runner.invoke(
            gateway,
            args=[
                'services', 'nat', 'update-snat', TestNatRule._name,
                TestNatRule._snat_id, '-o', TestNatRule._new_snat_orig_addr,
                '-t', TestNatRule._new_snat_trans_addr, '--desc',
                TestNatRule._new_snat_desc, '--logging-disable'])
        self.assertEqual(0, result.exit_code)

    def test_0040_update_dnat_rule(self):
        """Update DNAT Rule in the gateway.
        It will trigger the cli command 'services nat update-dnat'
        """
        result = TestNatRule._runner.invoke(
            gateway,
            args=[
                'services', 'nat', 'update-dnat', TestNatRule._name,
                TestNatRule._dnat_id, '-o', TestNatRule._new_dnat1_orig_addr,
                '-t', TestNatRule._new_dnat1_trans_addr, '-p',
                TestNatRule._new_dnat1_protocol, '--desc',
                TestNatRule._new_dnat1_desc, '--logging-disable'])
        self.assertEqual(0, result.exit_code)

    def test_0045_reorder_nat_rule(self):
        """Reorder the NAT rule position on gateway.

        Invoke the cli command 'services nat reorder'.
        """
        result = TestNatRule._runner.invoke(
            gateway,
            args=[
                'services', 'nat', 'reorder', TestNatRule._name,
                TestNatRule._snat_id, '--index', TestNatRule._index])
        self.assertEqual(0, result.exit_code)

    def test_0050_delete_nat_rule(self):
        """Deletes the nat rule.
        It will trigger the cli command services nat delete
        """
        # Delete the SNAT Rule
        result = TestNatRule._runner.invoke(
            gateway,
            args=[
                'services', 'nat', 'delete', TestNatRule._name,
                TestNatRule._snat_id])
        self.assertEqual(0, result.exit_code)
        # Delete the DNAT Rule
        result = TestNatRule._runner.invoke(
            gateway,
            args=[
                'services', 'nat', 'delete', TestNatRule._name,
                TestNatRule._dnat_id])
        self.assertEqual(0, result.exit_code)

    def get_row_containing_word(self, output, word):
        rows = output.split('\n')
        for row in rows:
            if row.find(word) != -1:
                result_arr = row.strip().split()
                return result_arr[2]

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
