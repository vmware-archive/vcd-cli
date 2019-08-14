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
from pyvcloud.system_test_framework.vapp_constants import VAppConstants
from pyvcloud.system_test_framework.environment import CommonRoles
from pyvcloud.system_test_framework.environment import Environment
from pyvcloud.system_test_framework.utils import \
    create_customized_vapp_from_template
from pyvcloud.system_test_framework.utils import create_empty_vapp
from pyvcloud.system_test_framework.utils import create_independent_disk
from pyvcloud.vcd.client import EntityType
from pyvcloud.vcd.client import NSMAP
from pyvcloud.vcd.client import RelationType
from pyvcloud.vcd.client import TaskStatus
from pyvcloud.vcd.vapp import VApp
from pyvcloud.vcd.vm import VM
from uuid import uuid1
from vcd_cli.vcd import vcd  # NOQA
from vcd_cli.login import login, logout
from vcd_cli.org import org
from vcd_cli.vdc import vdc
from vcd_cli.vm import vm

import re


class VmTest(BaseTestCase):
    """Test VM related commands

    Be aware that this test will delete existing vcd-cli sessions.
    """
    DEFAULT_ADAPTER_TYPE = 'VMXNET3'
    DEFAULT_IP_MODE = 'POOL'
    _empty_vapp_name = 'empty_vApp_' + str(uuid1())
    _empty_vapp_description = 'empty vApp description'
    _empty_vapp_runtime_lease = 86400  # in seconds
    _empty_vapp_storage_lease = 86400  # in seconds
    _empty_vapp_owner_name = None
    _empty_vapp_href = None
    _target_vm_name = 'target_vm'
    _idisk_name = 'SCSI'
    _idisk_size = '5242880'
    _idisk_description = '5Mb SCSI disk'

    _test_vapp_vmtools_name = 'test_vApp_vmtools_' + str(uuid1())
    _test_vapp_vmtools_vm_name = 'yVM'
    _metric_pattern = '*.average'

    _vapp_name = 'testVapp' + str(uuid1())
    _vm_name = 'testvm1'
    _vm_name_update = 'testvm'
    _description_update = 'Description'
    _computer_name_update = 'mycom'
    _boot_delay_update = 60
    _enter_bios_setup_update = True
    _new_ovf_info = 'new info'

    def test_0000_setup(self):
        """Load configuration and create a click runner to invoke CLI."""
        logger = Environment.get_default_logger()
        VmTest._config = Environment.get_config()
        VmTest._logger = logger
        VmTest._client = Environment.get_client_in_default_org(
            CommonRoles.ORGANIZATION_ADMINISTRATOR)
        VmTest._media_resource = Environment.get_test_media_resource()

        VmTest._runner = CliRunner()
        default_org = VmTest._config['vcd']['default_org_name']
        VmTest._login(self)
        VmTest._runner.invoke(org, ['use', default_org])

        default_ovdc = VmTest._config['vcd']['default_ovdc_name']
        VmTest._default_ovdc = default_ovdc
        VmTest._runner.invoke(vdc, ['use', VmTest._default_ovdc])

        VmTest._test_vdc = Environment.get_test_vdc(VmTest._client)
        VmTest._test_vapp = Environment.get_test_vapp_with_network(
            VmTest._client)
        VmTest._test_old_vapp_href = VmTest._test_vapp.get_resource().get('href')
        self.assertIsNotNone(VmTest._test_old_vapp_href)
        logger.debug("Old vapp href is : " + VmTest._test_old_vapp_href)

        VmTest._test_vm = VM(
            VmTest._client,
            href=VmTest._test_vapp.get_vm(VAppConstants.vm1_name).get('href'))
        self.assertIsNotNone(VmTest._test_vapp.get_vm(VAppConstants.vm1_name).get('href'))
        logger.debug("Old vapp VM href is : " +
            VmTest._test_vapp.get_vm(VAppConstants.vm1_name).get('href'))

        vdc1 = Environment.get_test_vdc(VmTest._client)
        logger.debug('Creating empty vApp.')
        VmTest._empty_vapp_href = \
            create_empty_vapp(client=VmTest._client,
                              vdc=vdc1,
                              name=VmTest._empty_vapp_name,
                              description=VmTest._empty_vapp_description)
        self.assertIsNotNone(VmTest._empty_vapp_href)
        logger.debug("Empty vapp href is: " + VmTest._empty_vapp_href)

        # Create independent disk
        VmTest._idisk_id = create_independent_disk(client=VmTest._client,
                                                   vdc=vdc1,
                                                   name=self._idisk_name,
                                                   size=self._idisk_size,
                                                   description=self._idisk_description)
        self.assertIsNotNone(VmTest._idisk_id)

        logger.debug("Independent disk id is: " + VmTest._idisk_id )

        # Upload template with vm tools.
        catalog_author_client = Environment.get_client_in_default_org(
            CommonRoles.CATALOG_AUTHOR)
        org_admin_client = Environment.get_client_in_default_org(
            CommonRoles.ORGANIZATION_ADMINISTRATOR)
        org1 = Environment.get_test_org(org_admin_client)
        catalog_name = Environment.get_config()['vcd']['default_catalog_name']
        catalog_items = org1.list_catalog_items(catalog_name)
        config = Environment.get_config()
        template_name = config['vcd']['default_template_vmtools_file_name']
        catalog_item_flag = False
        for item in catalog_items:
            if item.get('name').lower() == template_name.lower():
                logger.debug('Reusing existing template ' +
                             template_name)
                catalog_item_flag = True
                break
        if not catalog_item_flag:
            logger.debug('Uploading template ' + template_name +
                         ' to catalog ' + catalog_name + '.')
            org1.upload_ovf(catalog_name=catalog_name, file_name=template_name)
            # wait for the template import to finish in vCD.
            catalog_item = org1.get_catalog_item(
                name=catalog_name, item_name=template_name)
            template = catalog_author_client.get_resource(
                catalog_item.Entity.get('href'))
            catalog_author_client.get_task_monitor().wait_for_success(
                task=template.Tasks.Task[0])
            logger.debug("Template upload comleted for: " + template_name)

        # Create Vapp with template of vmware tools
        logger.debug('Creating vApp ' + VmTest._test_vapp_vmtools_name)
        VmTest._test_vapp_vmtools_href = create_customized_vapp_from_template(
            client=VmTest._client,
            vdc=vdc1,
            name=VmTest._test_vapp_vmtools_name,
            catalog_name=catalog_name,
            template_name=template_name)
        self.assertIsNotNone(VmTest._test_vapp_vmtools_href)
        logger.debug("vmtools vapp href is: " + VmTest._test_vapp_vmtools_href)
        vapp = VApp(VmTest._client, href=VmTest._test_vapp_vmtools_href)
        VmTest._test_vapp_vmtools = vapp
        vm_resource = vapp.get_vm(VmTest._test_vapp_vmtools_vm_name)
        VmTest._test_vapp_vmtools_vm_href = vm_resource.get('href')
        self.assertIsNotNone(VmTest._test_vapp_vmtools_vm_href)
        temp_name = config['vcd']['default_template_file_name']
        VmTest._test_vapp_href = create_customized_vapp_from_template(
            client=VmTest._client,
            vdc=vdc1,
            name=VmTest._vapp_name,
            catalog_name=catalog_name,
            template_name=temp_name)
        self.assertIsNotNone(VmTest._test_vapp_href)

        VmTest._sys_admin_client = Environment.get_sys_admin_client()
        resource = VmTest._sys_admin_client.get_extension()
        result = VmTest._sys_admin_client.get_linked_resource(
            resource, RelationType.DOWN,
            EntityType.DATASTORE_REFERENCES.value)
        if hasattr(result, '{' + NSMAP['vcloud'] + '}Reference'):
            for reference in result['{' + NSMAP['vcloud'] + '}Reference']:
                datastore_id = reference.get('id')
                VmTest._datastore_id = datastore_id.split(':')[3]
                break
        self.assertIsNotNone(VmTest._datastore_id)

    def test_0430_set_metadata(self):
        # Set metadata
        result = VmTest._runner.invoke(
            vm, args=['set-metadata',
                      VAppConstants.name, VAppConstants.vm1_name,
                      '--domain', 'GENERAL', '--visibility', 'READ_WRITE',
                      '--key', 'key1', '--value',
                      'value1'])
        self.assertEqual(0, result.exit_code)

    def test_0440_update_metadata(self):
        # update metadata
        result = VmTest._runner.invoke(
            vm, args=['update-metadata',
                      VAppConstants.name, VAppConstants.vm1_name,
                      '--domain', 'GENERAL', '--visibility', 'READ_WRITE',
                      '--key', 'key1', '--value',
                      'value2'])
        self.assertEqual(0, result.exit_code)

    def test_0450_list_metadata(self):
        # list metadata
        result = VmTest._runner.invoke(
            vm, args=['list-metadata',
                      VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0460_remove_metadata(self):
        # remove metadata
        result = VmTest._runner.invoke(
            vm, args=['remove-metadata',
                      VAppConstants.name, VAppConstants.vm1_name,
                      '--domain', 'GENERAL', '--key', 'key1'])
        self.assertEqual(0, result.exit_code)

    def test_9998_tearDown(self):
        """Delete the vApp created during setup.

        This test passes if the task for deleting the vApp succeed.
        """
        vapps_to_delete = []

        if VmTest._empty_vapp_href is not None:
            vapps_to_delete.append(VmTest._empty_vapp_name)
        vapp = VApp(VmTest._client, href=VmTest._test_old_vapp_href)
        self._power_off_and_undeploy(vapp = vapp)
        vapp = VApp(VmTest._client, href=VmTest._test_vapp_vmtools_href)
        self._power_off_and_undeploy(vapp = vapp)
        vapp = VApp(VmTest._client, href=VmTest._test_vapp_href)
        self._power_off_and_undeploy(vapp = vapp)
        vapps_to_delete.append(VmTest._vapp_name)
        vapps_to_delete.append(VmTest._test_vapp_vmtools_name)
        vapps_to_delete.append(VAppConstants.name)
        self._sys_login()
        vdc = Environment.get_test_vdc(VmTest._client)
        vdc.delete_disk(name=self._idisk_name)
        self._logout()

        self._login()

        for vapp_name in vapps_to_delete:
            task = vdc.delete_vapp(name=vapp_name, force=True)
            result = VmTest._client.get_task_monitor().wait_for_success(task)
            self.assertEqual(result.get('status'), TaskStatus.SUCCESS.value)


    def _login(self):
        org = VmTest._config['vcd']['default_org_name']
        user = Environment.get_username_for_role_in_test_org(
            CommonRoles.ORGANIZATION_ADMINISTRATOR)
        password = VmTest._config['vcd']['default_org_user_password']
        login_args = [
            VmTest._config['vcd']['host'], org, user, "-i", "-w",
            "--password={0}".format(password)
        ]
        result = VmTest._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _sys_login(self):
        """Logs in using admin credentials"""
        host = self._config['vcd']['host']
        org = self._config['vcd']['sys_org_name']
        admin_user = self._config['vcd']['sys_admin_username']
        admin_pass = self._config['vcd']['sys_admin_pass']
        login_args = [
            host, org, admin_user, "-i", "-w",
            "--password={0}".format(admin_pass)
        ]
        result = VmTest._runner.invoke(login, args=login_args)
        self.assertEqual(0, result.exit_code)
        self.assertTrue("logged in" in result.output)

    def _logout(self):
        """Logs out current session, ignoring errors"""
        VmTest._runner.invoke(logout)
