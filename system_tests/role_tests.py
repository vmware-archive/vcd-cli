from click.testing import CliRunner

from pyvcloud.system_test_framework.base_test import BaseTestCase
from pyvcloud.system_test_framework.environment import Environment
from vcd_cli.login import login, logout
from vcd_cli.role import role

DUMMY_ROLE_NAME = 'dummyrole'
ORG_ADMIN_ROLE_NAME = 'Organization Administrator'


class TestRole(BaseTestCase):
    """Test Role related commands."""

    def test_0000_setup(self):
        self._config = Environment.get_config()
        TestRole._logger = Environment.get_default_logger()
        TestRole._runner = CliRunner()
        self._sys_login()

    def _sys_login(self):
        """Logs in using admin credentials"""
        login_args = [
            self._config['vcd']['host'],
            self._config['vcd']['sys_org_name'],
            self._config['vcd']['sys_admin_username'],
            "-i",
            "-w",
            f"--password={self._config['vcd']['sys_admin_pass']}"
        ]
        result = TestRole._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

        """def test_0010_role_clone(self):
        # org admin and sys admin can clone roles
        result = self._runner.invoke(
            role,
            args=['clone', ORG_ADMIN_ROLE_NAME, DUMMY_ROLE_NAME])
        TestRole._logger.debug(f"vcd role clone {ORG_ADMIN_ROLE_NAME} "
                               f"{DUMMY_ROLE_NAME}: {result.output}")
        self.assertEqual(0, result.exit_code)"""

    def _logout(self):
        """Logs out current session, ignoring errors"""
        TestRole._runner.invoke(logout)

    def test_9999_teardown(self):
        self._logout()
