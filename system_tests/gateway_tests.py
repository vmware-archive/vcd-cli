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
from pyvcloud.system_test_framework.environment import Environment
from vcd_cli.login import login, logout
from vcd_cli.network import network
from vcd_cli.gateway import gateway
from vcd_cli.org import org
from pyvcloud.vcd.client import GatewayBackingConfigType
from pyvcloud.vcd.client import NSMAP
from pyvcloud.vcd.platform import Platform
from pyvcloud.vcd.utils import netmask_to_cidr_prefix_len


class GatewayTest(BaseTestCase):
    """Test gateway related commands

        Be aware that this test will delete existing vcd-cli sessions.
        """
    _runner = None
    _name = 'test_gateway1'
    _subnet_addr = None
    _ext_network_name = None
    _gateway_ip = None
    _logger = None

    def test_0000_setup(self):
        """Load configuration and create a click runner to invoke CLI."""
        self._config = Environment.get_config()
        GatewayTest._logger = Environment.get_default_logger()

        GatewayTest._runner = CliRunner()
        default_org = self._config['vcd']['default_org_name']
        self._login()
        GatewayTest._runner.invoke(org, ['use', default_org])

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
        ext_netws = remove_empty_lines(network_result.output)
        return ext_netws[2]

    def test_0001_create_gateway_with_mandatory_option(self):
        """Admin user can create gateway
        """
        result_create1 = GatewayTest._runner.invoke(
            gateway,
            args=['create', self._name, '-e', GatewayTest._ext_network_name])
        GatewayTest._logger.debug("vcd gateway create <name> -e <ext nw>: {"
                                  "0}".format(result_create1.output))
        self.assertEqual(0, result_create1.exit_code)
        self._delete_gateway()

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
        self.assertEqual(0, result_create2.exit_code)
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
        self.assertEqual(0, result_create3.exit_code)
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
        self.assertEqual(0, result_create5.exit_code)
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
        result_advanced_gateway = self._runner.invoke(
            gateway, args=['convert-to-advanced', 'test_gateway1'])
        self.assertEqual(0, result_advanced_gateway.exit_code)

    def test_0007_enable_distributed_routing(self):
        """Enable Distributed routing of the advanced gateway.

        It will trigger the cli command with option enable-distributed-routing
        """
        result_advanced_gateway = self._runner.invoke(
            gateway,
            args=['enable-distributed-routing', 'test_gateway1', '--enable'])
        self.assertEqual(0, result_advanced_gateway.exit_code)

    def test_0008_modify_form_factor(self):
        """Modify form factor of the gateway.

        It will trigger the cli command with option modify-form-factor
        """
        result = self._runner.invoke(
            gateway,
            args=[
                'modify-form-factor', 'test_gateway1',
                GatewayBackingConfigType.FULL.value
            ])
        self.assertEqual(0, result.exit_code)

    def test_0009_get_info(self):
        """Get information of the gateway.

        It will trigger the cli command with command 'info'
        """
        result_info = self._runner.invoke(
            gateway, args=['info', 'test_gateway1'])
        self.assertEqual(0, result_info.exit_code)

    def test_0010_redeploy_gateway(self):
        """Redeploy the gateway.

        It will trigger the cli command with option redeploy
        """
        result = self._runner.invoke(
            gateway, args=['redeploy', 'test_gateway1'])
        self.assertEqual(0, result.exit_code)

    def test_0011_sync_syslog_settings(self):
        """Sync syslog settings of the gateway.
         It will trigger the cli command with option sync-syslog-settings
        """
        result = self._runner.invoke(
            gateway, args=['sync-syslog-settings', 'test_gateway1'])
        self.assertEqual(0, result.exit_code)

    def test_0012_get_config_ip_settings(self):
        """Get information of the gateway config ip settings.

        It will trigger the cli command with option list-config-ip-settings
        """
        result_info = self._runner.invoke(
            gateway, args=['list-config-ip-settings', self._name])
        self.assertEqual(0, result_info.exit_code)

    def test_0098_tearDown(self):
        result_delete = self._runner.invoke(
            gateway, args=['delete', 'test_gateway1'])
        self.assertEqual(0, result_delete.exit_code)
        """Logout ignoring any errors to ensure test session is gone."""
        self._logout()
