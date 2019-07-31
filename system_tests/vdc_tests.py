# VMware vCloud Director vCD CLI
# Copyright (c) 2019 VMware, Inc. All Rights Reserved.
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
from pyvcloud.system_test_framework.environment import CommonRoles
from pyvcloud.system_test_framework.environment import Environment

from vcd_cli.login import login, logout
from vcd_cli.org import org
from vcd_cli.vdc import vdc

class TestOrgVDC(BaseTestCase):
    """Test OrgVDC functionalities implemented in pyvcloud."""

    # All tests in this module should run as System Administrator.
    _client = None

    def test_0000_setup(self):
        """Setup the org vdc required for the other tests in this module.
        """
        TestOrgVDC._config = Environment.get_config()
        logger = Environment.get_default_logger()
        TestOrgVDC._client = Environment.get_client_in_default_org(
            CommonRoles.ORGANIZATION_ADMINISTRATOR)
        TestOrgVDC._runner = CliRunner()
        default_org = TestOrgVDC._config['vcd']['default_org_name']
        TestOrgVDC._login(self)
        TestOrgVDC._runner.invoke(org, ['use', default_org])
        TestOrgVDC._vdc_resource = Environment.get_test_vdc(
            TestOrgVDC._client).get_resource()

    def test_0010_list_media(self):
        """Test the method VDC.list_media()."""
        vdc_name = TestOrgVDC._vdc_resource.get('name')
        """Get list of media."""
        result = TestOrgVDC._runner.invoke(
            vdc, args=['list-media', vdc_name])
        self.assertEqual(0, result.exit_code)

    def test_9998_teardown(self):
        """Test the method VDC.delete_vdc().

        Invoke the method for the vdc created by setup.

        This test passes if the task for deleting the vdc succeeds.
        """
        pass

    def test_9999_cleanup(self):
        """Release all resources held by this object for testing purposes."""
        TestOrgVDC._client.logout()

    def _login(self):
        org = TestOrgVDC._config['vcd']['default_org_name']
        user = Environment.get_username_for_role_in_test_org(
            CommonRoles.ORGANIZATION_ADMINISTRATOR)
        password = TestOrgVDC._config['vcd']['default_org_user_password']
        login_args = [
            TestOrgVDC._config['vcd']['host'], org, user, "-i", "-w",
            "--password={0}".format(password)
        ]
        result = TestOrgVDC._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)
