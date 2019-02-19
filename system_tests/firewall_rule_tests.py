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
from pyvcloud.system_test_framework.constants.ovdc_network_constant import \
    OvdcNetConstants
from pyvcloud.system_test_framework.environment import Environment
from pyvcloud.vcd.gateway import Gateway
from uuid import uuid1
from vcd_cli.org import org
from vcd_cli.login import login, logout
from vcd_cli.firewall_rule import gateway


class TestFirewallRule(BaseTestCase):
    """Adds new firewall rule in the gateway. It will trigger the cli command
    firewall create.
    """
    __name = GatewayConstants.name
    __firewall_rule_name = 'rule1' + str(uuid1())

    def test_0000_setup(self):

        self._config = Environment.get_config()
        TestFirewallRule._logger = Environment.get_default_logger()
        TestFirewallRule._client = Environment.get_sys_admin_client()
        TestFirewallRule._runner = CliRunner()
        default_org = self._config['vcd']['default_org_name']
        TestFirewallRule._ext_nw = self._config['external_network']['name']
        self._login()
        TestFirewallRule._runner.invoke(org, ['use', default_org])
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'create', TestFirewallRule.__name,
                '--name', TestFirewallRule.__firewall_rule_name, '--action',
                'accept', '--type', 'User', '--enabled', '--logging-enabled'
            ])
        self.assertEqual(0, result.exit_code)
        gateway_res = Environment.get_test_gateway(TestFirewallRule._client)
        gateway_obj = Gateway(
            TestFirewallRule._client, href=gateway_res.get('href'))
        firewall_rules = gateway_obj.get_firewall_rules()
        for rule in firewall_rules.firewallRules.firewallRule:
            if rule.name == TestFirewallRule.__firewall_rule_name:
                TestFirewallRule._rule_id = rule.id
                break

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
        result = TestFirewallRule._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        TestFirewallRule._runner.invoke(logout)

    def test_0001_list_firewall_rules(self):
        """Get information of the firewall rules.

        It will trigger the cli command with option gateway services
        firewall list.
        """
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=['services', 'firewall', 'list', TestFirewallRule.__name])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0011_list_object_types(self):
        """List object types."""
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'list-object-types',
                TestFirewallRule.__name, '--type', 'source'
            ])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0021_list_objects(self):
        """List objects for the provided object type."""
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'list-objects',
                TestFirewallRule.__name, '--type', 'source', '--object-type',
                'gatewayinterface'
            ])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0031_update(self):
        """Update Firewall Rule."""
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'update', TestFirewallRule.__name,
                TestFirewallRule._rule_id.text, '--source',
                TestFirewallRule._ext_nw + ':gatewayinterface', '--source',
                OvdcNetConstants.routed_net_name + ':network', '--source',
                '2.3.2.2:ip', '--destination',
                TestFirewallRule._ext_nw + ':gatewayinterface',
                '--destination', OvdcNetConstants.routed_net_name + ':network',
                '--destination', '2.3.2.2:ip', '--service', 'tcp', 'any',
                'any', '--service', 'tcp', 'any', 'any', '--service', 'any',
                'any', 'any', '--service', 'icmp', 'any', 'any', '--name',
                'new_name'
            ])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)
        # revert back name change to old name
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'update', TestFirewallRule.__name,
                TestFirewallRule._rule_id.text, '--name',
                TestFirewallRule.__firewall_rule_name
            ])
        self.assertEqual(0, result.exit_code)

    def test_0041_enable_firewall_rule(self):
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'enable', TestFirewallRule.__name,
                TestFirewallRule._rule_id.text
            ])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0042_disable_firewall_rule(self):
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'disable', TestFirewallRule.__name,
                TestFirewallRule._rule_id.text
            ])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0061_info_firewall_rule(self):
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'info', TestFirewallRule.__name,
                TestFirewallRule._rule_id.text
            ])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0071_delete_firewall_rule_source(self):
        source_value = 'vnic-0'
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'delete-source',
                TestFirewallRule.__name, TestFirewallRule._rule_id.text,
                source_value
            ])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0072_delete_firewall_rule_destination(self):
        destination_value = 'vnic-0'
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'delete-destination',
                TestFirewallRule.__name, TestFirewallRule._rule_id.text,
                destination_value
            ])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0073_delete_firewall_rule_service(self):
        protocol_to_delete = 'tcp'
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'delete-service',
                TestFirewallRule.__name, TestFirewallRule._rule_id.text,
                protocol_to_delete
            ])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0081_list_firewall_rule_source(self):
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'list-source', TestFirewallRule.__name,
                TestFirewallRule._rule_id.text
            ])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0082_list_firewall_rule_destination(self):
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'list-destination',
                TestFirewallRule.__name, TestFirewallRule._rule_id.text
            ])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0083_list_firewall_rule_service(self):
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'list-service',
                TestFirewallRule.__name, TestFirewallRule._rule_id.text
            ])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0091_update_firewall_rule_sequence(self):
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'reorder', '--index', '1',
                TestFirewallRule.__name, TestFirewallRule._rule_id.text
            ])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0098_delete_firewall_rule(self):
        result = TestFirewallRule._runner.invoke(
            gateway,
            args=[
                'services', 'firewall', 'delete', TestFirewallRule.__name,
                TestFirewallRule._rule_id.text
            ])
        TestFirewallRule._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0099_cleanup(self):
        """Release all resources held by this object for testing purposes."""
        self._logout()
