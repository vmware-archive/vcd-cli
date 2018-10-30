#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid
from click.testing import CliRunner

from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.environment import Environment
from vcd_cli.login import login, logout
from vcd_cli.network import network
from vcd_cli.gateway import gateway
from vcd_cli.vcd import vcd
from vcd_cli.org import org
from pyvcloud.vcd.vdc import VDC

class GatewayTest(BaseTestCase):
    """Test gateway-related commands

        Tests cases in this module do not have ordering dependencies,
        so setup is accomplished using Python unittest setUp and tearDown
        methods.

        Be aware that this test will delete existing vcd-cli sessions.
        """

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

    def test_0010_create_gateway(self):
        """Admin user can create gateway
        """
        default_org = self._config['vcd']['default_org_name']
        self._login()
        self._runner.invoke(org, ['use', default_org])
        network_result = self._runner.invoke(network, args=['external',
                                                            'list'])
        self._logger.debug("vcd network external list: {0}"
                           .format(network_result.output))
        ext_netws = network_result.output
        ext_nets_name = ext_netws.split('------')
        ext_netws_arr = ext_nets_name[1].split('\n')
        ext_network_name = ext_netws_arr[1]
        self.client = Environment.get_sys_admin_client()
        vdc = Environment.get_test_vdc(
            Environment.get_sys_admin_client())
        external_networks_resource = vdc.list_external_network()
        ext_network = None
        for ext_network_temp in external_networks_resource.Network:
            if ext_network_temp.get('name') == ext_network_name:
                ext_network = ext_network_temp
        self.assertTrue(len(ext_network) > 0)
        ext_net_resource = self.client.get_resource(ext_network.get('href'))

        first_ipscope = ext_net_resource.Configuration.IpScopes.IpScope[0]
        gateway_ip = first_ipscope.Gateway.text
        subnet_addr = gateway_ip + '/' + str(first_ipscope.SubnetPrefixLength)

        result_create1 = self._runner.invoke(gateway, args=['create',
                                                      'test_gateway1',
                                                    '-e',
                                                    ext_network_name])
        self._logger.debug("vcd gateway create <name> -e <ext nw>: {"
                           "0}".format(result_create1.output))
        self.assertEqual(0, result_create1.exit_code)

        result_delete1 = self._runner.invoke(gateway, args=['delete',
                                                     'test_gateway1'])
        self.assertEqual(0, result_delete1.exit_code)

        result_create2 = self._runner.invoke(gateway, args=['create',
                                                       'test_gateway1',
                                                    '-e',
                                                    ext_netws_arr[1],
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
        result_delete2 = self._runner.invoke(gateway, args=['delete',
                                                     'test_gateway1'])
        self.assertEqual(0, result_delete2.exit_code)

        gateway_ip_arr = gateway_ip.split('.')
        last_ip_digit = int(gateway_ip_arr[-1]) + 1
        gateway_ip_arr[-1] = str(last_ip_digit)
        next_ip = '.'.join(gateway_ip_arr)
        ip_range = next_ip+'-'+next_ip
        result_create3 = self._runner.invoke(gateway, args=['create',
                                                      'test_gateway1',
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
        result_delete3 = self._runner.invoke(gateway, args=['delete',
                                                     'test_gateway1'])
        self.assertEqual(0, result_delete3.exit_code)

        result_create4 = self._runner.invoke(gateway, args=['create',
                                                    'test_gateway1',
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
        result_delete4 = self._runner.invoke(gateway, args=['delete',
                                                            'test_gateway1'])
        self.assertEqual(0, result_delete4.exit_code)

        result_create5 = self._runner.invoke(gateway, args=['create',
                                                    'test_gateway1',
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
        result_delete5 = self._runner.invoke(gateway, args=['delete',
                                                            'test_gateway1'])
        self.assertEqual(0, result_delete5.exit_code)

