#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from click.testing import CliRunner
from uuid import uuid1

from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.constants.gateway_constants \
    import GatewayConstants
from pyvcloud.system_test_framework.environment import Environment
from vcd_cli.vcd import vcd  # NOQA
from vcd_cli.gateway import gateway
from vcd_cli.login import login, logout
from vcd_cli.org import org
from vcd_cli.network import network


class VdcNetworkTests(BaseTestCase):
    """Test org vdc network related commands

    Be aware that this test will delete existing vcd-cli sessions.
    """
    _runner = None
    _name = 'test_routed_Nw' + str(uuid1())
    __subnet = '6.6.5.1/20'
    __ip_range1 = '6.6.5.2-6.6.5.20'
    __ip_range2 = '6.6.6.2-6.6.6.20'
    __new_ip_range = '6.6.5.12-6.6.5.22'
    __dns1 = '8.8.8.8'
    __dns2 = '8.8.8.9'
    __dns_suffix = 'example.com'

    def test_0000_setup(self):
        """Load configuration and create a click runner to invoke CLI."""
        self._config = Environment.get_config()
        VdcNetworkTests._logger = Environment.get_default_logger()

        VdcNetworkTests._runner = CliRunner()
        default_org = self._config['vcd']['default_org_name']
        self._login()
        VdcNetworkTests._runner.invoke(org, ['use', default_org])
        result_create1 = VdcNetworkTests._runner.invoke(
            network, [
                'routed', 'create', VdcNetworkTests._name, '-g',
                GatewayConstants.name, '--subnet', VdcNetworkTests.__subnet
            ])

        self.assertEqual(0, result_create1.exit_code)

    def test_0005_edit_name_description_and_shared_state(self):
        _new_name = 'test_routed_Nw_new' + str(uuid1())
        _new_description = 'New Description'
        result = self._runner.invoke(
            network,
            args=[
                'routed', 'edit', VdcNetworkTests._name, '-n', _new_name,
                '--description', _new_description, '--shared-enabled'
            ])
        self.assertEqual(0, result.exit_code)
        result = self._runner.invoke(
            network,
            args=['routed', 'edit', _new_name, '-n', VdcNetworkTests._name])
        self.assertEqual(0, result.exit_code)

    def test_0010_add_ip_ranges_of_routed_nw(self):

        result = self._runner.invoke(
            network,
            args=[
                'routed', 'add-ip-range', VdcNetworkTests._name, '--ip-range',
                VdcNetworkTests.__ip_range1, '--ip-range',
                VdcNetworkTests.__ip_range2
            ])
        self.assertEqual(0, result.exit_code)

    def test_0011_add_dns_of_routed_nw(self):

        result = self._runner.invoke(
            network,
            args=[
                'routed', 'add-dns', VdcNetworkTests._name, '--dns1',
                VdcNetworkTests.__dns1, '--dns2',
                VdcNetworkTests.__dns2, '--dns-suffix',
                VdcNetworkTests.__dns_suffix
            ])
        self.assertEqual(0, result.exit_code)

    def test_0015_modify_ip_range_of_routed_nw(self):
        """Modify Ip range of vdc routed network"""
        result = self._runner.invoke(
            network,
            args=[
                'routed', 'update-ip-range', VdcNetworkTests._name,
                '--ip-range', VdcNetworkTests.__ip_range1, '--new-ip-range',
                VdcNetworkTests.__new_ip_range
            ])
        self.assertEqual(0, result.exit_code)

    def test_0016_remove_ip_range(self):
        """Remove IP range of vdc routed network"""
        result = self._runner.invoke(
            network,
            args=[
                'routed', 'delete-ip-range', VdcNetworkTests._name,
                '--ip-range', VdcNetworkTests.__ip_range2
            ])
        self.assertEqual(0, result.exit_code)

    def test_0020_list_all_routed_nw(self):
        """List available vdc routed networks in vdc."""
        result = self._runner.invoke(network, args=['routed', 'list'])
        self.assertEqual(0, result.exit_code)

    def test_0030_routed_org_vdc_metadata(self):
        """Test metadata operations for a routed org vdc network"""
        key = "test-key1"
        value = "test-value1"
        VdcNetworkTests._set_metadata_in_routed_org_vcd_network(
            self, key, value)
        VdcNetworkTests._list_metadata_in_routed_org_vcd_network(self)
        VdcNetworkTests._remove_metadata_from_routed_org_vcd_network(self, key)

    def _set_metadata_in_routed_org_vcd_network(self, key, value):
        """Test set metadata for a routed org vdc network"""
        result = self._runner.invoke(
            network,
            args=[
                'routed', 'set-metadata', VdcNetworkTests._name, '--key', key,
                '--value', value
            ])
        self.assertEqual(0, result.exit_code)

    def _list_metadata_in_routed_org_vcd_network(self):
        """Test list metadata for a routed org vdc network"""
        result = self._runner.invoke(
            network, args=['routed', 'list-metadata', VdcNetworkTests._name])
        self.assertEqual(0, result.exit_code)

    def _remove_metadata_from_routed_org_vcd_network(self, key):
        """Test remove metadata for a routed org vdc network"""
        result = self._runner.invoke(
            network,
            args=[
                'routed', 'remove-metadata', VdcNetworkTests._name, '--key',
                key
            ])
        self.assertEqual(0, result.exit_code)

    def test_0040_list_allocated_ip_address(self):
        """Test list allocated IP address of a routed org vdc network"""
        result = self._runner.invoke(
            network,
            args=['routed', 'list-allocated-ip', VdcNetworkTests._name])
        self.assertEqual(0, result.exit_code)

    def test_0050_list_connected_vapps(self):
        """Test list connected vApps to a routed org vdc network"""
        result = self._runner.invoke(
            network,
            args=['routed', 'list-connected-vapps', VdcNetworkTests._name])
        self.assertEqual(0, result.exit_code)

    def test_0060_convert_to_sub_interface(self):
        """Test convert to sub interface of a routed org vdc network"""
        result = self._runner.invoke(
            network,
            args=['routed', 'convert-to-sub-interface', VdcNetworkTests._name])
        self.assertEqual(0, result.exit_code)

    def test_0070_convert_to_internal_interface(self):
        """Test convert to internal interface of a routed org vdc network"""
        result = self._runner.invoke(
            network,
            args=['routed', 'convert-to-internal-interface',
                  VdcNetworkTests._name])
        self.assertEqual(0, result.exit_code)

    def test_0075_convert_to_distributed_interface(self):
        """Test convert to distributed interface of a routed org vdc network"""
        try:
            result_advanced_gateway = self._runner.invoke(
                gateway,
                args=['enable-distributed-routing', GatewayConstants.name,
                      '--enable'])
            self.assertEqual(0, result_advanced_gateway.exit_code)
        except:
            # Ignore the failure as we can't check if it is already enabled
            pass

        result = self._runner.invoke(
            network,
            args=['routed', 'convert-to-distributed-interface',
                  VdcNetworkTests._name])
        self.assertEqual(0, result.exit_code)

        # Revert
        result = self._runner.invoke(
            network,
            args=['routed', 'convert-to-internal-interface',
                  VdcNetworkTests._name])
        self.assertEqual(0, result.exit_code)

        try:
            result_advanced_gateway = self._runner.invoke(
                gateway,
                args=['enable-distributed-routing', GatewayConstants.name,
                      '--disable'])
            self.assertEqual(0, result_advanced_gateway.exit_code)
        except:
            # Ignore the failure as we can't check if it is already enabled
            pass

    def test_0075_info(self):
        """Test info of a routed org vdc network"""
        result = self._runner.invoke(
            network, args=['routed', 'info', VdcNetworkTests._name])
        self.assertEqual(0, result.exit_code)

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
