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
from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.constants.gateway_constants import \
    GatewayConstants
from pyvcloud.system_test_framework.environment import Environment
from pyvcloud.vcd.gateway import Gateway
from vcd_cli.ipsec_vpn import gateway
from vcd_cli.org import org
from vcd_cli.login import login, logout


class TestCertificates(BaseTestCase):
    """Adds certificates in the gateway. It will trigger the cli command
    for certificates.
    """
    _name = GatewayConstants.name
    _certificate_file_path = 'certificate.pem'
    _private_key_file_path = 'private_key.pem'

    def test_0000_setup(self):
        TestCertificates._client = Environment.get_sys_admin_client()
        TestCertificates._config = Environment.get_config()
        TestCertificates._org = Environment.get_test_org(
            TestCertificates._client)
        test_gateway = Environment.get_test_gateway(TestCertificates._client)
        gateway_obj1 = Gateway(TestCertificates._client, GatewayConstants.name,
                               href=test_gateway.get('href'))
        TestCertificates.gateway_obj = gateway_obj1
        TestCertificates._runner = CliRunner()
        default_org = self._config['vcd']['default_org_name']
        self._login()
        TestCertificates._runner.invoke(org, ['use', default_org])

    def test_0010_add_service_certificate(self):
        """Adds service certificate.

        It will trigger the cli command services service-certificate add
        """
        result = TestCertificates._runner.invoke(
            gateway,
            args=[
                'services', 'service-certificate', 'add',
                TestCertificates._name, '--certificate-path',
                TestCertificates._certificate_file_path,
                '--private-key-path',
                TestCertificates._private_key_file_path])
        self.assertEqual(0, result.exit_code)

    def test_0015_list_service_certificate(self):
        """Lists service certificate.

        It will trigger the cli command services service-certificat list
        """
        result = TestCertificates._runner.invoke(
            gateway,
            args=[
                'services', 'service-certificate', 'list',
                TestCertificates._name])
        self.assertEqual(0, result.exit_code)

    def test_0020_delete_service_certificate(self):
        """Delete service certificate.

        It will trigger the cli command services service-certificat delete
        """
        gateway_obj1 = TestCertificates.gateway_obj
        certificate_list = gateway_obj1.list_service_certificates()
        certificate = certificate_list[0]
        id = certificate["Object_Id"]

        result = TestCertificates._runner.invoke(
            gateway,
            args=['services', 'service-certificate', 'delete',
                  TestCertificates._name, id])
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
        result = TestCertificates._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        TestCertificates._runner.invoke(logout)

    def test_0098_teardown(self):
        return

    def test_0099_cleanup(self):
        """Release all resources held by this object for testing purposes."""
        self._logout()
