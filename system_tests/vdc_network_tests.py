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
from vcd_cli.org import org
from vcd_cli.network import network
from system_tests.constants import GatewayConstants

class VdcNetworkTests(BaseTestCase):
    """Test org vdc network related commands

    Be aware that this test will delete existing vcd-cli sessions.
    """
    _runner = None
    _name = 'test_routed_Nw'

    def test_0000_setup(self):
        """Load configuration and create a click runner to invoke CLI."""
        self._config = Environment.get_config()
        VdcNetworkTests._logger = Environment.get_default_logger()

        VdcNetworkTests._runner = CliRunner()
        default_org = self._config['vcd']['default_org_name']
        self._login()
        VdcNetworkTests._runner.invoke(org, ['use', default_org])
        result_create1 = VdcNetworkTests._runner.invoke(network, ['routed',
                                                                  'create',
                                                 VdcNetworkTests._name,
                                                 '-g', GatewayConstants.name,
                                                 '--subnet', '6.6.5.1/20'
                                                 ])

        self.assertEqual(0, result_create1.exit_code)


    def test_0098_tearDown(self):
        result_delete = self._runner.invoke(
            network, args=['routed', 'delete', VdcNetworkTests._name])
        self.assertEqual(0, result_delete.exit_code)
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
        result = VdcNetworkTests._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        VdcNetworkTests._runner.invoke(logout)
