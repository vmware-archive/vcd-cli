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

from click.testing import CliRunner

import os
import yaml

from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.environment import Environment
from vcd_cli.login import login, logout
from vcd_cli.search import search


class SearchTest(BaseTestCase):
    """Test search-related commands

    Tests cases in this module do not have ordering dependencies,
    so setup is accomplished using Python unittest setUp and tearDown
    methods.

    Be aware that this test will delete existing vcd-cli sessions.
    """

    _sys_admin_id = None

    @classmethod
    def setUpClass(cls):
        if 'VCD_TEST_BASE_CONFIG_FILE' in os.environ:
            cls._config_file = os.environ['VCD_TEST_BASE_CONFIG_FILE']
        with open(cls._config_file, 'r') as f:
            cls._config_yaml = yaml.safe_load(f)

        Environment.init(cls._config_yaml)
        # We Don't need to setup further our Cloud Director so we skip attach vc, create pvcd ...

    @classmethod
    def tearDownClass(cls):
        Environment.cleanup()

    def setUp(self):
        """Load configuration , get sys_admin ID and create a click runner to invoke CLI."""
        self._config = Environment.get_config()
        self._logger = Environment.get_default_logger()

        client = Environment.get_sys_admin_client()
        org = client.get_org()
        org_href = org.get('href')
        admin_user = self._config['vcd']['sys_admin_username']
        user = client.get_user_in_org(admin_user, org_href)
        urn = user.get('id')
        self._sys_admin_id = urn.split(":").pop()
        self._logger.debug("sys_admin id: {0}".format(self._sys_admin_id))
        client.logout()

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

    def test_0010_search_without_arg(self):
        """Search command is going to output help and valid resources type
        """
        result = self._runner.invoke(search)
        self._logger.debug("vcd search: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)
        self.assertTrue("user" in result.output)
        self.assertTrue("cell" in result.output)
        self.assertTrue("virtualCenter" in result.output)
        self.assertTrue("organization" in result.output)
        self.assertTrue("adminOrgVdc" in result.output)
        self.assertTrue("vApp" in result.output)
        self.assertTrue("adminVM" in result.output)

    def test_0020_search_valid_resource_type(self):
        """Search a valid resource (ex: user)
        """
        result = self._runner.invoke(search, args=['user'])
        self._logger.debug("vcd search user: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)
        self.assertTrue("name" in result.output)
        self.assertTrue("fullName" in result.output)
        self.assertTrue("numberOfDeployedVMs" in result.output)

    def test_0030_search_with_filter(self):
        """Search with a filter (in 'user' ressources we are going to find our user)
        """
        admin_user = self._config['vcd']['sys_admin_username']
        filter = 'name==%s' % (admin_user)
        result = self._runner.invoke(search, args=['user', '--filter', filter])
        self._logger.debug(
            "vcd search user --filter {1}: {0}".format(result.output, filter))
        self.assertEqual(0, result.exit_code)
        self.assertTrue(self._sys_admin_id in result.output)
        self.assertTrue(admin_user in result.output)
        self.assertTrue("name" in result.output)
        self.assertTrue("fullName" in result.output)
        self.assertTrue("numberOfDeployedVMs" in result.output)

    def test_0031_search_with_filter_and_no_match(self):
        """Search with a filter on an unexpected user
        """
        unexpected_user = 'xxxClark_kent_is_not_zorro_but_he_is_an_hero_xxx'
        filter = 'name==%s' % (unexpected_user)
        result = self._runner.invoke(search, args=['user', '--filter', filter])
        self._logger.debug(
            "vcd search user --filter {1}: {0}".format(result.output, filter))
        self.assertEqual(0, result.exit_code)
        self.assertTrue("not found" in result.output)

    def test_0040_search_with_fields(self):
        """Search with fields: name, fullName and isEnable
        """
        admin_user = self._config['vcd']['sys_admin_username']
        fields = 'name,fullName,isEnabled'
        result = self._runner.invoke(search, args=['user', '--fields', fields])
        self._logger.debug(
            "vcd search user --fields {1}: {0}".format(result.output, fields))
        self.assertEqual(0, result.exit_code)
        self.assertTrue(self._sys_admin_id in result.output)
        self.assertTrue(admin_user in result.output)
        self.assertTrue("name" in result.output)
        self.assertTrue("fullName" in result.output)
        self.assertTrue("isEnabled" in result.output)
        self.assertFalse("numberOfDeployedVMs" in result.output)

    def test_0041_search_with_fields_as_label(self):
        """Search with fields: name as username, fullName as 'the full name' and isEnable as is-enable
        """
        admin_user = self._config['vcd']['sys_admin_username']
        fields = 'name as username,fullName as the full name,isEnabled as is-enabled'
        result = self._runner.invoke(search, args=['user', '--fields', fields])
        self._logger.debug(
            "vcd search user --fields {1}: {0}".format(result.output, fields))
        self.assertEqual(0, result.exit_code)
        self.assertTrue(self._sys_admin_id in result.output)
        self.assertTrue(admin_user in result.output)
        self.assertTrue("username" in result.output)
        self.assertTrue("the full name" in result.output)
        self.assertTrue("is-enabled" in result.output)
        self.assertFalse("isEnabled" in result.output)
        self.assertFalse("fullName" in result.output)
        self.assertFalse("numberOfDeployedVMs" in result.output)

    def test_0050_search_and_hide_id(self):
        """Search and hide id. The session user id should not be in the result.
        """
        admin_user = self._config['vcd']['sys_admin_username']
        result = self._runner.invoke(search, args=['user', '--hide-id'])
        self._logger.debug(
            "vcd search user --hide-id: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)
        self.assertFalse(self._sys_admin_id in result.output)
        self.assertTrue("name" in result.output)
        self.assertTrue("fullName" in result.output)
        self.assertTrue(admin_user in result.output)

    def test_0060_search_sort_asc(self):
        """Search and sort asc on isEnabled.
        """
        admin_user = self._config['vcd']['sys_admin_username']
        result = self._runner.invoke(
            search, args=['user', '--sort-asc', 'isEnabled'])
        self._logger.debug(
            "vcd search user --sort-asc isEnabled: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)
        self.assertTrue(self._sys_admin_id in result.output)
        self.assertTrue("name" in result.output)
        self.assertTrue("fullName" in result.output)
        self.assertTrue(admin_user in result.output)

    def test_0061_search_sort_asc_on_two_fields(self):
        """Search and sort asc on isEnabled and then on fullName.
        """
        admin_user = self._config['vcd']['sys_admin_username']
        result = self._runner.invoke(
            search, args=['user', '--sort-asc', 'isEnabled', '--sort-next', 'fullName'])
        self._logger.debug(
            "vcd search user --sort-asc isEnabled: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)
        self.assertTrue(self._sys_admin_id in result.output)
        self.assertTrue("name" in result.output)
        self.assertTrue("fullName" in result.output)
        self.assertTrue(admin_user in result.output)

    def test_0070_search_sort_desc(self):
        """Search and sort desc on isEnabled.
        """
        admin_user = self._config['vcd']['sys_admin_username']
        result = self._runner.invoke(
            search, args=['user', '--sort-desc', 'isEnabled'])
        self._logger.debug(
            "vcd search user --sort-desc isEnabled: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)
        self.assertTrue(self._sys_admin_id in result.output)
        self.assertTrue("name" in result.output)
        self.assertTrue("fullName" in result.output)
        self.assertTrue(admin_user in result.output)

    def test_0071_search_sort_desc_on_two_fields(self):
        """Search and sort desc on isEnabled and then on fullName.
        """
        admin_user = self._config['vcd']['sys_admin_username']
        result = self._runner.invoke(
            search, args=['user', '--sort-desc', 'isEnabled', '--sort-next', 'fullName'])
        self._logger.debug(
            "vcd search user --sort-desc isEnabled: {0}".format(result.output))
        self.assertEqual(0, result.exit_code)
        self.assertTrue(self._sys_admin_id in result.output)
        self.assertTrue("name" in result.output)
        self.assertTrue("fullName" in result.output)
        self.assertTrue(admin_user in result.output)
