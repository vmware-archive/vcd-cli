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

from uuid import uuid1
from click.testing import CliRunner

from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.environment import Environment

from vcd_cli.login import login, logout
from vcd_cli.network import external

from pyvcloud.vcd.client import QueryResultFormat
from pyvcloud.vcd.client import ResourceType
from helpers.portgroup_helper import PortgroupHelper


class ExtNetTest(BaseTestCase):
    """Test external network related commands

    Tests cases in this module do not have ordering dependencies,
    so setup is accomplished using Python unittest setUp and tearDown
    methods.

    Be aware that this test will delete existing vcd-cli sessions.
    """

    # All tests in this module should run as System Administrator.
    _sys_admin_client = None
    _name = 'external_network_' + str(uuid1())
    _description = 'Description of external_network_' + str(uuid1())
    _port_group = None
    _portgroupType = "DV_PORTGROUP"
    _gateway = '10.20.30.1'
    _netmask = '255.255.255.0'
    _ip_range = '10.20.30.2-10.20.30.99'
    _dns1 = '8.8.8.8'
    _dns2 = '8.8.8.9'
    _dns_suffix = 'example.com'
    _gateway1 = '10.10.30.1'
    _ip_range1 = '10.10.30.2-10.10.30.99'
    _ip_range2 = '10.10.30.30-10.10.30.60'
    _ip_range3 = '10.10.30.101-10.10.30.110'

    def setUp(self):
        """Load configuration and create a click runner to invoke CLI."""
        self._config = Environment.get_config()
        self._logger = Environment.get_default_logger()

        self._runner = CliRunner()
        self._login()

    def tearDown(self):
        """Logout ignoring any errors to ensure test session is gone."""
        self._logout()

    def _login(self):
        """Logs in using admin credentials"""
        host = self._config['vcd']['host']
        org = self._config['vcd']['sys_org_name']
        admin_user = self._config['vcd']['sys_admin_username']
        admin_pass = self._config['vcd']['sys_admin_pass']
        ExtNetTest._vc2_host_ip = self._config['vc2']['vcenter_host_ip']
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

    def test_0010_create(self):
        """Create an external network as per configuration stated above.

        Choose first unused port group which is not a VxLAN. Unused port groups
        have network names set to '--'. VxLAN port groups have name starting
        with 'vxw-'.

        Invoke the command 'external create' in network.
        """
        vc_name = self._config['vc']['vcenter_host_name']
        name_filter = ('vcName', vc_name)
        sys_admin_client = Environment.get_sys_admin_client()
        query = sys_admin_client.get_typed_query(
            ResourceType.PORT_GROUP.value,
            query_result_format=QueryResultFormat.RECORDS,
            equality_filter=name_filter)

        for record in list(query.execute()):
            if record.get('networkName') == '--':
                if not record.get('name').startswith('vxw-'):
                    self._port_group = record.get('name')
                    break

        self.assertIsNotNone(self._port_group,
                             'None of the port groups are free.')

        result = self._runner.invoke(
            external,
            args=[
                'create', self._name, '--vc', vc_name, '--port-group',
                self._port_group, '--gateway', self._gateway, '--netmask',
                self._netmask, '--ip-range', self._ip_range, '--description',
                self._description, '--dns1', self._dns1, '--dns2', self._dns2,
                '--dns-suffix', self._dns_suffix
            ])
        self.assertEqual(0, result.exit_code)

    def test_0020_update(self):
        """Update name and description of the external network created.

        Invoke the command 'external update' in network.
        """
        new_name = "updated_" + self._name
        new_description = "Updated " + self._name
        result = self._runner.invoke(
            external,
            args=[
                'update', self._name, '--name', new_name, '--description',
                new_description
            ])
        self.assertEqual(0, result.exit_code)

        # Update name and description back to original
        result = self._runner.invoke(
            external,
            args=[
                'update', new_name, '--name', self._name, '--description',
                self._description
            ])
        self.assertEqual(0, result.exit_code)

    def test_0030_add_subnet(self):
        """Add subnet to the external network created.

        Invoke the command 'external add-subnet' in network.
        """
        result = self._runner.invoke(
            external,
            args=[
                'add-subnet', self._name, '--gateway', self._gateway1,
                '--netmask', self._netmask, '--ip-range', self._ip_range1,
                '--dns1', self._dns1, '--dns2', self._dns2, '--dns-suffix',
                self._dns_suffix
            ])
        self.assertEqual(0, result.exit_code)

    def test_0031_enable_subnet(self):
        """Enable/Disable subnet of an external network.

        Invoke the command 'external enable-subnet' in network.
        """
        result = self._runner.invoke(
            external,
            args=[
                'enable-subnet', self._name, '--gateway', self._gateway1,
                '--enable'
            ])
        self.assertEqual(0, result.exit_code)
        result = self._runner.invoke(
            external,
            args=[
                'enable-subnet', self._name, '--gateway', self._gateway1,
                '--disable'
            ])
        self.assertEqual(0, result.exit_code)

    def test_0040_attach_port_group(self):
        """Attach a portgroup to an external network.
        Invoke the command 'external attach-port-group' in network.
        """
        if ExtNetTest._vc2_host_ip is None or ExtNetTest._vc2_host_ip == '':
            return
        ExtNetTest._client = Environment.get_sys_admin_client()

        port_group_helper = PortgroupHelper(ExtNetTest._client)
        vc_name = self._config['vc2']['vcenter_host_name']
        pg_name = port_group_helper. \
            get_available_portgroup_name(vc_name, ExtNetTest._portgroupType)
        result = self._runner.invoke(
            external,
            args=[
                'attach-port-group', self._name, '--vc', vc_name,
                '--port-group', pg_name
            ])
        self.assertEqual(0, result.exit_code)

    def test_0041_detach_port_group(self):
        """Detach port group from an external network.
        Invoke the command 'external detach-port-group' in network.
        """
        if ExtNetTest._vc2_host_ip is None or ExtNetTest._vc2_host_ip == '':
            return
        ExtNetTest._client = Environment.get_sys_admin_client()
        port_group_helper = PortgroupHelper(ExtNetTest._client)
        vc_name = self._config['vc2']['vcenter_host_name']
        pg_name = port_group_helper. \
            get_ext_net_used_portgroup_name(vc_name, self._name)
        result = self._runner.invoke(
            external,
            args=[
                'detach-port-group', self._name, '--vc', vc_name,
                '--port-group', pg_name
            ])
        self.assertEqual(0, result.exit_code)

    def test_0050_add_ip_range(self):
        """Add an IP range to a subnet in an external network.

        Invoke the command 'external add-ip-range' in network.
        """
        result = self._runner.invoke(
            external,
            args=[
                'add-ip-range', self._name, '--gateway', self._gateway1,
                '--ip-range', self._ip_range3
            ])
        self.assertEqual(0, result.exit_code)

    def test_0051_update_ip_range(self):
        """Update an IP range of a subnet in an external network.

        Invoke the command 'external update-ip-range' in network.
        """
        result = self._runner.invoke(
            external,
            args=[
                'update-ip-range', self._name, '--gateway', self._gateway1,
                '--ip-range', self._ip_range1, '--new-ip-range',
                self._ip_range2
            ])
        self.assertEqual(0, result.exit_code)

    def test_0052_delete_ip_range(self):
        """Remove an IP range of a subnet in an external network.

        Invoke the command 'external delete-ip-range' in network.
        """
        result = self._runner.invoke(
            external,
            args=[
                'delete-ip-range', self._name, '--gateway', self._gateway1,
                '--ip-range', self._ip_range2
            ])
        self.assertEqual(0, result.exit_code)

    def test_0055_list_available_prov_vdc(self):
        """List available provider vdcs.

        Invoke the command 'external list-pvdc' in network.
        """
        result = self._runner.invoke(external, args=['list-pvdc', self._name])
        self.assertEqual(0, result.exit_code)

    def test_0060_list_available_gateways(self):
        """List available gateways.

        Invoke the command 'external list-gateway' in network.
        """
        result = self._runner.invoke(
            external, args=['list-gateway', self._name])
        self.assertEqual(0, result.exit_code)

    def test_0065_list_allocated_ip(self):
        """List allocated ip.

        Invoke the command 'external list-allocated-ip' in network.
        """
        result = self._runner.invoke(
            external, args=['list-allocated-ip', self._name])
        self.assertEqual(0, result.exit_code)

    def test_0070_list_sub_allocated_ip(self):
        """List sub allocated ip.

        Invoke the command 'external list-sub-allocated-ip' in network.
        """
        result = self._runner.invoke(
            external, args=['list-sub-allocated-ip', self._name])
        self.assertEqual(0, result.exit_code)

    def test_0075_list_associated_direct_org_vdc_networks(self):
        """List associated direct org vDC networks.

        Invoke the command 'external list-direct-org-vdc-network' in network.
        """
        result = self._runner.invoke(
            external, args=['list-direct-org-vdc-network', self._name])
        self.assertEqual(0, result.exit_code)

    def test_0080_list_vsphere_networks(self):
        """List associated vSphere Networks.

        Invoke the command 'external list-vsphere-network' in network.
        """
        result = self._runner.invoke(
            external, args=['list-vsphere-network', self._name])
        self.assertEqual(0, result.exit_code)

    def test_0090_info(self):
        """Show external network details.

        Invoke the command 'external info' in network.
        """
        result = self._runner.invoke(
            external, args=['info', self._name])
        self.assertEqual(0, result.exit_code)

    def test_0100_delete(self):
        """Delete the external network created.

            Invoke the command 'external delete' in network.
        """
        result = self._runner.invoke(external, args=['delete', self._name])
        self.assertEqual(0, result.exit_code)
