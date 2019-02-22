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
from pyvcloud.vcd.client import ApiVersion
from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.constants.gateway_constants import \
    GatewayConstants
from pyvcloud.vcd.system import System
from pyvcloud.vcd.vdc import VDC
from pyvcloud.vcd.vdc_network import VdcNetwork

from pyvcloud.system_test_framework.environment import Environment
from pyvcloud.vcd.gateway import Gateway
from vcd_cli.ipsec_vpn import gateway
from vcd_cli.org import org
from vcd_cli.login import login, logout


class TestIpSecVpn(BaseTestCase):
    """Adds IPsec VPN in the gateway. It will trigger the cli command
    IPsec VPN create.
    """
    _name = GatewayConstants.name
    _orgvdc_name = 'orgvdc2'
    _gateway_name = 'test_gateway2'
    _routed_network_name = 'routednet2'
    _routed_orgvdc_network_gateway_ip = '10.20.10.1/24'
    _ipsec_vpn_name = 'vpn1'
    _peer_id = 'peer_id1'
    _local_id = 'local_id1'
    _peer_subnet = '10.20.10.0/24'
    _local_subnet = '30.20.10.0/24,30.20.20.0/24'
    _psk = 'abcd1234'
    _changed_psk = "abcdefghijkl"
    _log_level = "warning"
    _new_name = "updated_ipsec"

    def test_0000_setup(self):
        """Add one orgvdc, one gateways and one routed orgvdc networks.

        """
        TestIpSecVpn._client = Environment.get_sys_admin_client()
        TestIpSecVpn._logger = Environment.get_default_logger()
        TestIpSecVpn._config = Environment.get_config()
        TestIpSecVpn._org = Environment.get_test_org(TestIpSecVpn._client)
        TestIpSecVpn._pvdc_name = Environment.get_test_pvdc_name()
        TestIpSecVpn._ext_config = TestIpSecVpn._config['external_network']
        TestIpSecVpn._ext_net_name = TestIpSecVpn._ext_config['name']
        # Create another vdc, gateway and routed network

        self.__create_ovdc()
        self.__create_advanced_gateway()
        self.__create_routed_ovdc_network()
        test_gateway = Environment.get_test_gateway(TestIpSecVpn._client)
        gateway_obj1 = Gateway(TestIpSecVpn._client, GatewayConstants.name,
                               href=test_gateway.get('href'))
        gateway_obj2 = TestIpSecVpn._gateway_obj
        TestIpSecVpn._local_ip = self.__get_ip_address(
            gateway=gateway_obj1, ext_net_name=TestIpSecVpn._ext_net_name)

        TestIpSecVpn._peer_ip = self.__get_ip_address(
            gateway=gateway_obj2, ext_net_name=TestIpSecVpn._ext_net_name)

        TestIpSecVpn._runner = CliRunner()
        default_org = self._config['vcd']['default_org_name']
        self._login()
        TestIpSecVpn._runner.invoke(org, ['use', default_org])
        result = TestIpSecVpn._runner.invoke(
            gateway,
            args=[
                'services', 'ipsec-vpn', 'create', TestIpSecVpn._name,
                '--name', TestIpSecVpn._ipsec_vpn_name,
                '--local-id', TestIpSecVpn._local_id,
                '--peer-id', TestIpSecVpn._peer_id,
                '--local-ip', TestIpSecVpn._local_ip,
                '--peer-ip', TestIpSecVpn._peer_ip,
                '--local-subnet', TestIpSecVpn._local_subnet,
                '--peer-subnet', TestIpSecVpn._peer_subnet,
                '--pre-shared-key', TestIpSecVpn._psk, '--enable'])
        self.assertEqual(0, result.exit_code)

    def test_0010_update_ipsec_vpn(self):
        """Update given ipsec vpn.

        It will trigger the cli command services ipsec_vpn
        update
        """
        id = TestIpSecVpn._local_ip + '-' + TestIpSecVpn._peer_ip
        result = TestIpSecVpn._runner.invoke(
            gateway,
            args=[
                'services', 'ipsec-vpn', 'update', TestIpSecVpn._name, id,
                '--new-name', TestIpSecVpn._new_name])
        self.assertEqual(0, result.exit_code)

    def test_0015_info_ipsec_vpn(self):
        """Get details of given ipsec vpn.

        It will trigger the cli command services ipsec_vpn
        info
        """
        id = TestIpSecVpn._local_ip + '-' + TestIpSecVpn._peer_ip
        result = TestIpSecVpn._runner.invoke(
            gateway,
            args=[
                'services', 'ipsec-vpn', 'info', TestIpSecVpn._name,
                id])
        self.assertEqual(0, result.exit_code)

    def test_0020_enable_activation_status(self):
        """Enables activation status of ipsec vpn.

        It will trigger the cli command services ipsec_vpn
        enable-activation-status
        """
        result = TestIpSecVpn._runner.invoke(
            gateway,
            args=[
                'services', 'ipsec-vpn', 'enable-activation-status',
                TestIpSecVpn._name, '--enable'])
        self.assertEqual(0, result.exit_code)

    def test_0025_info_activation_status(self):
        """Info activation status of ipsec vpn.

        It will trigger the cli command services ipsec_vpn
        info-activation-status
        """
        result = TestIpSecVpn._runner.invoke(
            gateway,
            args=[
                'services', 'ipsec-vpn', 'enable-activation-status',
                TestIpSecVpn._name])
        self.assertEqual(0, result.exit_code)

    def test_0025_enable_logging(self):
        """Enables logging of ipsec vpn.

        It will trigger the cli command services ipsec_vpn
        enable-logging
        """
        result = TestIpSecVpn._runner.invoke(
            gateway,
            args=[
                'services', 'ipsec-vpn', 'enable-logging',
                TestIpSecVpn._name, '--enable'])
        self.assertEqual(0, result.exit_code)

    def test_0030_info_logging_settings(self):
        """Info logging settings of ipsec vpn.

        It will trigger the cli command services ipsec_vpn
        info-logging-settings
        """
        result = TestIpSecVpn._runner.invoke(
            gateway,
            args=[
                'services', 'ipsec-vpn', 'info-logging-settings',
                TestIpSecVpn._name])
        self.assertEqual(0, result.exit_code)

    def test_0040_set_log_level(self):
        """Set log level of ipsec vpn.

        It will trigger the cli command services ipsec_vpn
        set-log-level
        """
        result = TestIpSecVpn._runner.invoke(
            gateway,
            args=[
                'services', 'ipsec-vpn', 'set-log-level',
                TestIpSecVpn._name, 'warning'])
        self.assertEqual(0, result.exit_code)

    def test_0045_list_ipsec_vpn(self):
        """List IPsec VPN of a gateway.

        It will trigger the cli command services ipsec_vpn
        list
        """
        result = TestIpSecVpn._runner.invoke(
            gateway,
            args=[
                'services', 'ipsec-vpn', 'list',
                TestIpSecVpn._name])
        self.assertEqual(0, result.exit_code)

    def test_0050_change_shared_key(self):
        """Change shared key of ipsec vpn.

        It will trigger the cli command services ipsec_vpn
        change-shared-key
        """
        result = TestIpSecVpn._runner.invoke(
            gateway,
            args=[
                'services', 'ipsec-vpn', 'change-shared-key',
                TestIpSecVpn._name, 'newsharedkey'])
        self.assertEqual(0, result.exit_code)

    def test_0090_delete_ipsec_vpn(self):
        """Deletes the ipsec vpn.

        It will trigger the cli command services ipsec_vpn delete
        """
        id = TestIpSecVpn._local_ip + '-' + TestIpSecVpn._peer_ip
        result = TestIpSecVpn._runner.invoke(
            gateway,
            args=[
                'services', 'ipsec-vpn', 'delete', TestIpSecVpn._name,
                id])
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
        result = TestIpSecVpn._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        TestIpSecVpn._runner.invoke(logout)

    def test_0098_teardown(self):
        """Removes the added vdc, gateway and routed networks.

        """
        vdc = VDC(TestIpSecVpn._client, resource=TestIpSecVpn._vdc_resource)
        task1 = vdc.delete_routed_orgvdc_network(
            name=TestIpSecVpn._routed_network_name)
        TestIpSecVpn._client.get_task_monitor().wait_for_success(task=task1)
        task2 = vdc.delete_gateway(name=TestIpSecVpn._gateway_name)
        TestIpSecVpn._client.get_task_monitor().wait_for_success(task=task2)
        vdc.enable_vdc(enable=False)
        vdc.delete_vdc()

    def test_0099_cleanup(self):
        """Release all resources held by this object for testing purposes."""
        self._logout()

    def __get_ip_address(self, gateway, ext_net_name):

        gateway_interfaces = gateway.get_resource().Configuration. \
            GatewayInterfaces
        for gateway_inf in gateway_interfaces.GatewayInterface:
            if gateway_inf.Name == ext_net_name:
                return gateway_inf.SubnetParticipation.IpAddress.text

    def __create_ovdc(self):
        """Creates an org vdc with the name specified in the test class.

        :raises: Exception: if the class variable _org_href or _pvdc_name
             is not populated.
         """

        system = System(TestIpSecVpn._client,
                        admin_resource=TestIpSecVpn._client.get_admin())
        if TestIpSecVpn._org is None:
            org_name = TestIpSecVpn._config['vcd']['default_org_name']
            org_resource_list = TestIpSecVpn._client.get_org_list()

        org = TestIpSecVpn._org
        ovdc_name = TestIpSecVpn._orgvdc_name

        if self.__check_ovdc(org, ovdc_name):
            return

        storage_profiles = [{
            'name':
                TestIpSecVpn._config['vcd']['default_storage_profile_name'],
            'enabled':
                True,
            'units':
                'MB',
            'limit':
                0,
            'default':
                True
        }]

        netpool_to_use = Environment._get_netpool_name_to_use(system)
        vdc_resource = org.create_org_vdc(
            ovdc_name,
            TestIpSecVpn._pvdc_name,
            network_pool_name=netpool_to_use,
            network_quota=TestIpSecVpn._config['vcd']['default_network_quota'],
            storage_profiles=storage_profiles,
            uses_fast_provisioning=True,
            is_thin_provision=True)

        TestIpSecVpn._client.get_task_monitor().wait_for_success(
            task=vdc_resource.Tasks.Task[0])

        org.reload()
        # The following contraption is required to get the non admin href of
        # the ovdc. vdc_resource contains the admin version of the href since
        # we created the ovdc as a sys admin.

        self.__check_ovdc(org, ovdc_name)

    def __check_ovdc(self, org, ovdc_name):
        if org.get_vdc(ovdc_name):
            vdc = org.get_vdc(ovdc_name)
            TestIpSecVpn._ovdc_href = vdc.get('href')
            TestIpSecVpn._vdc_resource = vdc
            return True
        else:
            return False

    def __does_exist_gateway(self, gateway_name):
        vdc = VDC(TestIpSecVpn._client, resource=TestIpSecVpn._vdc_resource)
        gateway = vdc.get_gateway(TestIpSecVpn._gateway_name)
        if gateway:
            TestIpSecVpn._gateway_resource = gateway
            TestIpSecVpn._gateway_href = gateway.get('href')
            TestIpSecVpn._gateway_obj = Gateway(
                TestIpSecVpn._client, href=TestIpSecVpn._gateway_href)
            return True
        else:
            return False

    def __create_advanced_gateway(self):
        """Creates a gateway."""

        ext_config = TestIpSecVpn._config['external_network']
        vdc_reource = TestIpSecVpn._vdc_resource
        api_version = TestIpSecVpn._config['vcd']['api_version']
        vdc = VDC(TestIpSecVpn._client, resource=vdc_reource)
        gateway = vdc.get_gateway(TestIpSecVpn._gateway_name)
        if self.__does_exist_gateway(TestIpSecVpn._gateway_name):
            return

        if float(api_version) <= float(
                ApiVersion.VERSION_30.value):
            gateway = vdc.create_gateway_api_version_30(
                TestIpSecVpn._gateway_name, [ext_config['name']])
        elif float(api_version) == float(ApiVersion.VERSION_31.value):
            gateway = vdc.create_gateway_api_version_31(
                TestIpSecVpn._gateway_name,
                [ext_config['name']],
                should_create_as_advanced=True)
        elif float(api_version) >= float(ApiVersion.VERSION_32.value):
            gateway = vdc.create_gateway_api_version_32(
                TestIpSecVpn._gateway_name, [ext_config['name']],
                should_create_as_advanced=True)

        TestIpSecVpn._client.get_task_monitor(). \
            wait_for_success(task=gateway.Tasks.Task[0])
        TestIpSecVpn._gateway_href = gateway.get('href')
        TestIpSecVpn._gateway_obj = Gateway(TestIpSecVpn._client,
                                            href=TestIpSecVpn._gateway_href)
        TestIpSecVpn._gateway_resource = TestIpSecVpn. \
            _gateway_obj.get_resource()

    def __create_routed_ovdc_network(self):
        """Creates a routed org vdc network.

        :raises: Exception: if the class variable _ovdc_href is not populated.
        """
        vdc_reource = TestIpSecVpn._vdc_resource
        vdc = VDC(TestIpSecVpn._client, resource=vdc_reource)
        routednet = vdc.create_routed_vdc_network(
            network_name=TestIpSecVpn._routed_network_name,
            gateway_name=TestIpSecVpn._gateway_name,
            network_cidr=TestIpSecVpn._routed_orgvdc_network_gateway_ip,
            description='org vdc network description')
        TestIpSecVpn._client.get_task_monitor() \
            .wait_for_success(task=routednet.Tasks.Task[0])

        TestIpSecVpn._routednet_href = routednet.get('href')
        TestIpSecVpn._routednet_obj = VdcNetwork(TestIpSecVpn._client,
                                                 href=TestIpSecVpn.
                                                 _routednet_href)
        TestIpSecVpn._routednet_resource = TestIpSecVpn. \
            _routednet_obj.get_resource()
