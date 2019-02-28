#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from uuid import uuid1
from click.testing import CliRunner

from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.environment import Environment
from vcd_cli.login import login, logout
from vcd_cli.network import external
from vcd_cli.network import network
from vcd_cli.gateway import gateway
from vcd_cli.org import org
from pyvcloud.vcd.client import ApiVersion
from pyvcloud.vcd.client import GatewayBackingConfigType
from pyvcloud.vcd.client import NSMAP
from pyvcloud.vcd.client import QueryResultFormat
from pyvcloud.vcd.client import ResourceType
from pyvcloud.vcd.platform import Platform
from pyvcloud.vcd.utils import netmask_to_cidr_prefix_len


class GatewayTest(BaseTestCase):
    """Test gateway related commands

        Be aware that this test will delete existing vcd-cli sessions.
        """
    _runner = None
    _name = ('test_gateway1' + str(uuid1()))[:34]
    _new_name = ('test_gateway2' + str(uuid1()))[:34]
    _external_network_name = 'external_network_' + str(uuid1())
    _subnet_addr = None
    _ext_network_name = None
    _gateway_ip = '2.2.3.1'
    _logger = None

    def test_0000_setup(self):
        """Load configuration and create a click runner to invoke CLI."""
        self._config = Environment.get_config()
        GatewayTest._logger = Environment.get_default_logger()

        GatewayTest._runner = CliRunner()
        default_org = self._config['vcd']['default_org_name']
        self._login()
        GatewayTest._runner.invoke(org, ['use', default_org])
        GatewayTest._api_version = self._config['vcd']['api_version']
        GatewayTest._ext_network_name = self._get_first_external_network()

        self.client = Environment.get_sys_admin_client()
        platform = Platform(self.client)
        ext_net_resource = platform.get_external_network(
            GatewayTest._ext_network_name)

        self.assertTrue(len(ext_net_resource) > 0)

        ip_scopes = ext_net_resource.xpath(
            'vcloud:Configuration/vcloud:IpScopes/vcloud:IpScope',
            namespaces=NSMAP)
        first_ipscope = ip_scopes[0]
        GatewayTest._gateway_ip = first_ipscope.Gateway.text
        prefix_len = netmask_to_cidr_prefix_len(GatewayTest._gateway_ip,
                                                first_ipscope.Netmask.text)
        GatewayTest._subnet_addr = GatewayTest._gateway_ip + '/' + str(
            prefix_len)

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
        result = GatewayTest._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        GatewayTest._runner.invoke(logout)

    def _get_first_external_network(self):
        """Get the first available external network.

        :return: str first external network name
        """
        network_result = GatewayTest._runner.invoke(
            network, args=['external', 'list'])
        GatewayTest._logger.debug("vcd network external list: {0}".format(
            network_result.output))
        ext_netws = network_result.output
        ext_nets_name = ext_netws.split('\n')
        GatewayTest._logger.debug(ext_nets_name)
        return ext_nets_name[2]

    def test_0001_create_gateway_with_mandatory_option(self):
        """Admin user can create gateway
        """
        result_create1 = GatewayTest._runner.invoke(
            gateway,
            args=['create', self._name, '-e', GatewayTest._ext_network_name])
        GatewayTest._logger.debug("vcd gateway create <name> -e <ext nw>: {"
                                  "0}".format(result_create1.output))
        self.assertTrue(
            self._validate_result_for_unclosed_sslsocket_warning(
                result_create1))
        self._delete_gateway()

    def _validate_result_for_unclosed_sslsocket_warning(self, result):
        if (result.exit_code == -1 and
                'ResourceWarning: unclosed <ssl.SSLSocket' in result.output):
            return True
        return 0 == result.exit_code

    def test_0002_create_gateway_with_configure_ip_setting(self):
        """Create gateway with options --configure-ip-setting.

        It will delete the gateway after creation
        """
        result_create2 = GatewayTest._runner.invoke(
            gateway,
            args=[
                'create', self._name, '-e', GatewayTest._ext_network_name,
                '--configure-ip-setting', GatewayTest._ext_network_name,
                GatewayTest._subnet_addr, 'Auto'
            ])
        GatewayTest._logger.debug("vcd gateway create <name> -e <ext nw> "
                                  "--configure-ip-setting', '{0}', '{1}', "
                                  "'Auto']: {2}".format(
                                      GatewayTest._ext_network_name,
                                      GatewayTest._subnet_addr,
                                      result_create2.output))
        self.assertTrue(
            self._validate_result_for_unclosed_sslsocket_warning(
                result_create2))
        self._delete_gateway()

    def _get_ip_range(self):
        gateway_ip_arr = GatewayTest._gateway_ip.split('.')
        last_ip_digit = int(gateway_ip_arr[-1]) + 1
        gateway_ip_arr[-1] = str(last_ip_digit)
        next_ip = '.'.join(gateway_ip_arr)
        ip_range = next_ip + '-' + next_ip
        return ip_range

    def test_0003_create_gateway_with_sub_allocate_ip_and_subnet(self):
        """Create gateway with options --sub-allocate-ip --subnet --ip-range.

        It will delete the gateway after creation
        """
        ip_range = self._get_ip_range()
        result_create3 = GatewayTest._runner.invoke(
            gateway,
            args=[
                'create', self._name, '-e', GatewayTest._ext_network_name,
                '--sub-allocate-ip', GatewayTest._ext_network_name, '--subnet',
                GatewayTest._subnet_addr, '--ip-range', ip_range,
                '--sub-allocate-ip', GatewayTest._ext_network_name, '--subnet',
                GatewayTest._subnet_addr, '--ip-range', ip_range
            ])
        GatewayTest._logger.debug("vcd gateway create <name> -e <ext nw> "
                                  "--sub-allocate-ip', {0}, '--subnet',{1}, "
                                  "{2}]: {3}".format(
                                      GatewayTest._ext_network_name,
                                      GatewayTest._subnet_addr, ip_range,
                                      result_create3.output))
        self.assertTrue(
            self._validate_result_for_unclosed_sslsocket_warning(
                result_create3))
        self._delete_gateway()

    def test_0004_create_gateway_with_default_gateway_and_dns_relay_enabled(
            self):
        """Create gateway with options --default-gateway --default-gateway-ip
        --dns-relay-enabled --advanced-enabled.

        It will delete the gateway after creation.
        """
        result_create5 = GatewayTest._runner.invoke(
            gateway,
            args=[
                'create', self._name, '-e', GatewayTest._ext_network_name,
                '--default-gateway', GatewayTest._ext_network_name,
                '--default-gateway-ip', GatewayTest._gateway_ip,
                '--dns-relay-enabled', '--advanced-enabled'
            ])
        GatewayTest._logger.debug(
            "vcd gateway create <name> -e <ext nw> "
            "--defalut-gateway <ext_nw>"
            "--default-gateway-ip {0} --dns-relay-enabled "
            "--advanced-enabled : {"
            "1}".format(GatewayTest._gateway_ip, result_create5.output))
        self.assertTrue(
            self._validate_result_for_unclosed_sslsocket_warning(
                result_create5))
        self._delete_gateway()

    def test_0005_create_gateway_with_configure_rate_limit(self):
        """Create gateway with options --configure-rate-limit.

        It will delete the gateway after creation
        """
        result_create4 = GatewayTest._runner.invoke(
            gateway,
            args=[
                'create', self._name, '-e', GatewayTest._ext_network_name,
                '--configure-rate-limit', GatewayTest._ext_network_name, 100,
                101
            ])
        GatewayTest._logger.debug("vcd gateway create <name> -e <ext nw> "
                                  "--configure-rate-limit', {0}, 100, "
                                  "101]: {1}".format(
                                      GatewayTest._ext_network_name,
                                      result_create4.output))
        self.assertEqual(0, result_create4.exit_code)

    def _delete_gateway(self):
        result_delete1 = GatewayTest._runner.invoke(
            gateway, args=['delete', self._name])
        self.assertEqual(0, result_delete1.exit_code)

    def test_0006_convert_to_advanced_gateway(self):
        """Convert legacy gateway to advance gateway.

        It will trigger the cli command with option convert-to-advanced
        """
        if float(GatewayTest._api_version) >= float(
                ApiVersion.VERSION_32.value):
            return
        result_advanced_gateway = self._runner.invoke(
            gateway, args=['convert-to-advanced', self._name])
        self.assertEqual(0, result_advanced_gateway.exit_code)

    def test_0007_enable_distributed_routing(self):
        """Enable Distributed routing of the advanced gateway.

        It will trigger the cli command with option enable-distributed-routing
        """
        result_advanced_gateway = self._runner.invoke(
            gateway,
            args=['enable-distributed-routing', self._name, '--enable'])
        self.assertEqual(0, result_advanced_gateway.exit_code)

    def test_0008_modify_form_factor(self):
        """Modify form factor of the gateway.

        It will trigger the cli command with option modify-form-factor
        """
        result = self._runner.invoke(
            gateway,
            args=[
                'modify-form-factor', self._name,
                GatewayBackingConfigType.FULL.value
            ])
        self.assertEqual(0, result.exit_code)

    def test_0009_get_info(self):
        """Get information of the gateway.

        It will trigger the cli command with command 'info'
        """
        result_info = self._runner.invoke(gateway, args=['info', self._name])
        self.assertEqual(0, result_info.exit_code)

    def test_0010_redeploy_gateway(self):
        """Redeploy the gateway.

        It will trigger the cli command with option redeploy
        """
        result = self._runner.invoke(gateway, args=['redeploy', self._name])
        self.assertEqual(0, result.exit_code)

    def test_0011_sync_syslog_settings(self):
        """Sync syslog settings of the gateway.
         It will trigger the cli command with option sync-syslog-settings
        """
        result = self._runner.invoke(
            gateway, args=['sync-syslog-settings', self._name])
        self.assertEqual(0, result.exit_code)

    def test_0012_get_config_ip_settings(self):
        """Get information of the gateway config ip settings.

        It will trigger the cli command with option list-config-ip-settings
        """
        result_info = self._runner.invoke(
            gateway, args=['list-config-ip-settings', self._name])
        GatewayTest._logger.debug('result output {0}'.format(result_info))
        self.assertTrue(
            self._validate_result_for_unclosed_sslsocket_warning(result_info))

    def _create_external_network(self):
        """Create an external network as per configuration stated above.

        Choose first unused port group which is not a VxLAN. Unused port groups
        have network names set to '--'. VxLAN port groups have name starting
        with 'vxw-'.

        Invoke the command 'external create' in network.
        """
        _config = Environment.get_config()
        vc_name = _config['vc']['vcenter_host_name']
        name_filter = ('vcName', vc_name)
        sys_admin_client = Environment.get_sys_admin_client()
        query = sys_admin_client.get_typed_query(
            ResourceType.PORT_GROUP.value,
            query_result_format=QueryResultFormat.RECORDS,
            equality_filter=name_filter)

        _port_group = None
        for record in list(query.execute()):
            if record.get('networkName') == '--':
                if not record.get('name').startswith('vxw-'):
                    _port_group = record.get('name')
                    break

        self.assertIsNotNone(_port_group, 'None of the port groups are free.')

        result = self._runner.invoke(
            external,
            args=[
                'create', self._external_network_name, '--vc', vc_name,
                '--port-group', _port_group, '--gateway', '10.10.30.1',
                '--netmask', '255.255.255.0', '--ip-range',
                '10.10.30.101-10.10.30.150', '--description',
                self._external_network_name, '--dns1', '8.8.8.8', '--dns2',
                '8.8.8.9', '--dns-suffix', 'example.com'
            ])
        self.assertEqual(0, result.exit_code)

    def _delete_external_network(self):
        """Delete the external network created.

            Invoke the command 'external delete' in network.
        """
        result = self._runner.invoke(
            external, args=['delete', self._external_network_name])
        self.assertEqual(0, result.exit_code)

    def test_0013_add_external_network(self):
        """Adds external network to the gateway.
         It will trigger the cli command configure-external-network add
        """
        self._create_external_network()
        result = self._runner.invoke(
            gateway,
            args=[
                'configure-external-network', 'add', self._name, '-e',
                self._external_network_name, '--configure-ip-setting',
                '10.10.30.1/24', '10.10.30.110'
            ])
        GatewayTest._logger.debug(
            "vcd gateway configure-external-network add "
            "-e {0} --configure-ip-setting {1}\n{2}".format(
                self._external_network_name, '10.10.30.1/24 10.10.30.110',
                result.output))
        self.assertTrue(
            self._validate_result_for_unclosed_sslsocket_warning(result))

    def test_0014_remove_external_network(self):
        """Removes external network from the gateway.
         It will trigger the cli command configure-external-network remove
        """
        result = self._runner.invoke(
            gateway,
            args=[
                'configure-external-network', 'remove', self._name, '-e',
                self._external_network_name
            ])
        self.assertTrue(
            self._validate_result_for_unclosed_sslsocket_warning(result))
        self._delete_external_network()

    def test_0015_edit_gateway_name(self):
        """Edits the gateway name.
         It will trigger the cli command update
        """
        result = self._runner.invoke(
            gateway, args=['update', self._name, '-n', self._new_name])
        self.assertEqual(0, result.exit_code)
        """ resetting back to original name"""
        result = self._runner.invoke(
            gateway, args=['update', self._new_name, '-n', self._name])
        self.assertEqual(0, result.exit_code)

    @unittest.skip("Its running for base gateway and not for other "
                   "test gateway so skipping test "
                   "case for now")
    def test_0016_edit_config_ip_settings(self):
        """Edits the gateway config ip settings.

        It will trigger the cli command with option config-ip-settings
        """
        GatewayTest._logger.debug(
            "vcd gateway configure-ip-settings {} -e {} "
            "-s {} True {}".format(self._name, GatewayTest._ext_network_name,
                                   GatewayTest._subnet_addr,
                                   GatewayTest._new_config_ip))
        result = self._runner.invoke(
            gateway,
            args=[
                'configure-ip-settings', self._name, '--external-network',
                GatewayTest._ext_network_name, '--subnet-available',
                GatewayTest._subnet_addr, True, GatewayTest._new_config_ip
            ])
        GatewayTest._logger.debug("result {} ".format(result.output))
        self.assertEqual(0, result.exit_code)

    def test_0017_add_sub_allocated_ip_pools(self):
        """Adds new ip range present to the sub allocate pool of gateway.
         It will trigger the cli command sub-allocate-ip add
        """
        self._config = Environment.get_config()
        config = self._config['external_network']
        gateway_sub_allocated_ip_range = \
            config['gateway_sub_allocated_ip_range']
        ext_name = config['name']
        result = self._runner.invoke(
            gateway,
            args=[
                'sub-allocate-ip', 'add', self._name, '-e', ext_name,
                '--ip-range', gateway_sub_allocated_ip_range
            ])
        self.assertEqual(0, result.exit_code)

    def test_0018_edit_sub_allocated_ip_pools(self):
        """Edits existing ip range present in the sub allocate pool of gateway.
         It will trigger the cli command sub-allocate-ip update
        """
        self._config = Environment.get_config()
        config = self._config['external_network']
        gateway_sub_allocated_ip_range = \
            config['gateway_sub_allocated_ip_range']
        gateway_sub_allocated_ip_range1 = \
            config['new_gateway_sub_allocated_ip_range']
        ext_name = config['name']
        result = self._runner.invoke(
            gateway,
            args=[
                'sub-allocate-ip', 'update', self._name, '-e', ext_name, '-o',
                gateway_sub_allocated_ip_range, '-n',
                gateway_sub_allocated_ip_range1
            ])
        self.assertEqual(0, result.exit_code)

    def test_0019_remove_sub_allocated_ip_pools(self):
        """Removes the given IP ranges from existing IP ranges.
         It will trigger the cli command sub-allocate-ip remove
        """
        self._config = Environment.get_config()
        config = self._config['external_network']
        gateway_sub_allocated_ip_range = \
            config['new_gateway_sub_allocated_ip_range']
        ext_name = config['name']
        result = self._runner.invoke(
            gateway,
            args=[
                'sub-allocate-ip', 'remove', self._name, '-e', ext_name, '-i',
                gateway_sub_allocated_ip_range
            ])

        GatewayTest._logger.debug("vcd gateway sub-allocate-ip remove {0}"
                                  "-e {1} -i {2}".format(
                                      self._name, ext_name,
                                      gateway_sub_allocated_ip_range))
        self.assertEqual(0, result.exit_code)

    @unittest.skip("Its running for base gateway and not for other "
                   "test gateway so skipping test "
                   "case for now")
    def test_0020_update_rate_limit(self):
        """Updates existing rate limit of gateway.
         It will trigger the cli command configure-rate-limits list
        """
        self._config = Environment.get_config()
        config = self._config['external_network']
        ext_name = config['name']
        result = self._runner.invoke(
            gateway,
            args=[
                'configure-rate-limits', 'list', self._name, '-r',
                [(ext_name, '101.0', '101.0')]
            ])
        self.assertEqual(0, result.exit_code)

    def test_0021_list_rate_limit(self):
        """Lists rate limit of gateway.
         It will trigger the cli command configure-rate-limits update
        """
        result = self._runner.invoke(
            gateway, args=['configure-rate-limits', 'list', self._name])
        self.assertEqual(0, result.exit_code)

    def test_0022_disable_rate_limit(self):
        """Disables rate limit of gateway.
         It will trigger the cli command configure-rate-limits disable
        """
        self._config = Environment.get_config()
        config = self._config['external_network']
        ext_name = config['name']
        result = self._runner.invoke(
            gateway,
            args=[
                'configure-rate-limits', 'disable', self._name, '-e', ext_name
            ])
        self.assertEqual(0, result.exit_code)

    def test_0023_configure_default_gateways(self):
        """Configures gateway for provided external networks and gateway IP.
         It will trigger the cli command configure-default-gateway update
        """
        self._config = Environment.get_config()
        config = self._config['external_network']
        GatewayTest._logger.debug("config :{0} ".format(config))
        ext_name = config['name']
        ip_scopes = config['ip_scopes'][0]
        subnet = ip_scopes['subnet']
        ip = subnet.split('/')[0]
        GatewayTest._logger.debug("vcd gateway configure-default-gateway "
                                  "update {0} -e {1} --gateway-ip {"
                                  "2}".format(self._name, ext_name, ip))
        result = self._runner.invoke(
            gateway,
            args=[
                'configure-default-gateway', 'update', self._name, '-e',
                ext_name, '--gateway-ip', ip, '--enable'
            ])
        self.assertEqual(0, result.exit_code)

    def test_0024_enable_dns_relay(self):
        """Enables/disables the dns relay of the default gateway.
         It will trigger the cli command configure-default-gateway
             enable-dns-relay
        """
        result = self._runner.invoke(
            gateway,
            args=[
                'configure-default-gateway', 'enable-dns-relay', self._name,
                '--enable'
            ])
        self.assertEqual(0, result.exit_code)

    def test_0025_list_configure_default_gateways(self):
        """Lists the configured default gateway.
         It will trigger the cli command configure-default-gateway list
        """
        result = self._runner.invoke(
            gateway, args=['configure-default-gateway', 'list', self._name])
        self.assertEqual(0, result.exit_code)

    @unittest.skip("Skipping test case because set syslog server is not in "
                   "code. It should be unskipped after set syslog server is "
                   "written")
    def test_0030_get_tenant_syslog_ip(self):
        """Get information of the gateway tenant syslog ip server.

        It will trigger the cli command with option list-syslog-server
        """
        result_info = self._runner.invoke(
            gateway, args=['list-syslog-server', self._name])
        GatewayTest._logger.debug('result output {0}'.format(result_info))
        self.assertTrue(
            self._validate_result_for_unclosed_sslsocket_warning(result_info))

    def test_0031_set_tenant_syslog_ip(self):
        """Set information of the gateway tenant syslog ip server.

        It will trigger the cli command with option set-syslog-server
        """
        ip = '192.168.5.6'
        result = self._runner.invoke(
            gateway, args=['set-syslog-server', self._name, ip])
        GatewayTest._logger.debug('result output {0}'.format(result))
        self.assertEqual(0, result.exit_code)

    def test_0098_tearDown(self):
        result_delete = self._runner.invoke(
            gateway, args=['delete', self._name])
        self.assertEqual(0, result_delete.exit_code)
        """Logout ignoring any errors to ensure test session is gone."""
        self._logout()
