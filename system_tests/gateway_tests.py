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
from pyvcloud.vcd.client import NSMAP
from pyvcloud.vcd.platform import Platform

class GatewayTest(BaseTestCase):
    """Test gateway related commands

        Be aware that this test will delete existing vcd-cli sessions.
        """

    _name = 'test_gateway1'
    def setUp(self):
        """Load configuration and create a click runner to invoke CLI."""
        self._config = Environment.get_config()
        self._logger = Environment.get_default_logger()

        self._runner = CliRunner()

    def tearDown(self):
        """Logout ignoring any errors to ensure test session is gone."""
        self._logout()

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
        result = self._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        self._runner.invoke(logout)

    def _get_first_external_network(self):
        """Get the first available external network.

        :return: str first external network name
        """
        network_result = self._runner.invoke(network, args=['external',
                                                            'list'])
        self._logger.debug("vcd network external list: {0}"
                           .format(network_result.output))
        ext_netws = network_result.output
        ext_nets_name = ext_netws.split('------')
        ext_netws_arr = ext_nets_name[1].split('\n')
        return ext_netws_arr[1]

    def test_0010_create_gateway(self):
        """Admin user can create gateway
        """
        default_org = self._config['vcd']['default_org_name']
        self._login()
        self._runner.invoke(org, ['use', default_org])

        ext_network_name =self._get_first_external_network()

        self.client = Environment.get_sys_admin_client()
        platform = Platform(self.client)
        ext_net_resource = platform.get_external_network(ext_network_name)

        self.assertTrue(len(ext_net_resource) > 0)

        ip_scopes = ext_net_resource.xpath(
            'vcloud:Configuration/vcloud:IpScopes/vcloud:IpScope',
            namespaces=NSMAP)
        first_ipscope = ip_scopes[0]
        gateway_ip = first_ipscope.Gateway.text
        subnet_addr = gateway_ip + '/' + str(first_ipscope.SubnetPrefixLength)

        result_create1 = self._runner.invoke(gateway, args=['create',
                                                      self._name,
                                                    '-e',
                                                    ext_network_name])
        self._logger.debug("vcd gateway create <name> -e <ext nw>: {"
                           "0}".format(result_create1.output))
        self.assertEqual(0, result_create1.exit_code)
        self._delete_gateway()

        result_create2 = self._runner.invoke(gateway, args=['create',
                                                            self._name, '-e',
                                                            ext_network_name,
                                                    '--configure-ip-setting',
                                                    ext_network_name,
                                                    subnet_addr,
                                                    'Auto'])
        self._logger.debug("vcd gateway create <name> -e <ext nw> "
                           "--configure-ip-setting', '{0}', '{1}', "
                           "'Auto']: {2}".format(ext_network_name,
                                                 subnet_addr,
                                                 result_create2.output))
        self.assertEqual(0, result_create2.exit_code)
        self._delete_gateway()

        gateway_ip_arr = gateway_ip.split('.')
        last_ip_digit = int(gateway_ip_arr[-1]) + 1
        gateway_ip_arr[-1] = str(last_ip_digit)
        next_ip = '.'.join(gateway_ip_arr)
        ip_range = next_ip+'-'+next_ip
        result_create3 = self._runner.invoke(gateway, args=['create',
                                                      self._name,
                                                    '-e',
                                                    ext_network_name,
                                                    '--sub-allocate-ip',
                                                    ext_network_name,
                                                            '--subnet',
                                                            subnet_addr,
                                                    '--ip-range',
                                                    ip_range])
        self._logger.debug("vcd gateway create <name> -e <ext nw> "
                           "--sub-allocate-ip', {0}, '--subnet',{1}, "
                           "{2}]: {3}".format(ext_network_name,
                                              subnet_addr,
                                              ip_range,
                                              result_create3.output))
        self.assertEqual(0, result_create3.exit_code)
        self._delete_gateway()

        result_create4 = self._runner.invoke(gateway, args=['create',
                                                    self._name,
                                                    '-e',
                                                    ext_network_name,
                                                    '--configure-rate-limit',
                                                     ext_network_name,
                                                     100, 101])
        self._logger.debug("vcd gateway create <name> -e <ext nw> "
                           "--configure-rate-limit', {0}, 100, "
                           "101]: {1}".format(ext_network_name,
                                              result_create4.output))
        self.assertEqual(0, result_create4.exit_code)
        self._delete_gateway()

        result_create5 = self._runner.invoke(gateway, args=['create',
                                                    self._name,
                                                    '-e',
                                                    ext_network_name,
                                                    '--default-gateway',
                                                    ext_network_name,
                                                    '--default-gw-ip',
                                                    gateway_ip,
                                                    '--dns-relay-enabled',
                                                    '--advanced-enabled'])
        self._logger.debug("vcd gateway create <name> -e <ext nw> "
                           "--defalut-gateway <ext_nw>"
                           "--default-gw-ip {0} --dns-relay-enabled "
                           "--advanced-enabled : {"
                           "1}".format(gateway_ip, result_create5.output))
        self.assertEqual(0, result_create5.exit_code)
        self._delete_gateway()

    def _delete_gateway(self):
        result_delete1 = self._runner.invoke(gateway, args=['delete',
                                                            self._name])
        self.assertEqual(0, result_delete1.exit_code)
