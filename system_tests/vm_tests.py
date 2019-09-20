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
        VmTest._test_old_vapp_href = VmTest._test_vapp.get_resource().get(
            'href')
        self.assertIsNotNone(VmTest._test_old_vapp_href)
        logger.debug("Old vapp href is : " + VmTest._test_old_vapp_href)

        VmTest._test_vm = VM(
            VmTest._client,
            href=VmTest._test_vapp.get_vm(VAppConstants.vm1_name).get('href'))
        self.assertIsNotNone(
            VmTest._test_vapp.get_vm(VAppConstants.vm1_name).get('href'))
        logger.debug("Old vapp VM href is : " +
                     VmTest._test_vapp.get_vm(VAppConstants.vm1_name).get(
                         'href'))

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

        logger.debug("Independent disk id is: " + VmTest._idisk_id)

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

    def test_0010_info(self):
        """Get info of the VM."""
        result = VmTest._runner.invoke(
            vm, args=['info', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        # verify output
        vm_name_regex = r"name\s*%s" % VAppConstants.vm1_name
        vapp_regex = r"vapp\s*%s" % VAppConstants.name
        # finall returns a list. checking that list is not empty.
        self.assertTrue(re.findall(vm_name_regex, result.output))
        self.assertTrue(re.findall(vapp_regex, result.output))

    def test_0020_consolidate(self):
        """Consolidate the VM."""
        default_org = self._config['vcd']['default_org_name']
        self._sys_login()
        VmTest._runner.invoke(org, ['use', default_org])
        VmTest._runner.invoke(vdc, ['use', VmTest._default_ovdc])
        result = VmTest._runner.invoke(
            vm,
            args=['consolidate', VAppConstants.name,
                  VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        # logging out sys_client
        self._logout()
        # logging with org admin user
        self._login()
        VmTest._runner.invoke(vdc, ['use', VmTest._default_ovdc])

    def test_0025_copy_to(self):
        """Copy VM from one vApp to another."""
        result = VmTest._runner.invoke(
            vm, args=['copy', VAppConstants.name, VAppConstants.vm1_name,
                      '--target-vapp-name', VmTest._empty_vapp_name,
                      '--target-vm-name', VmTest._target_vm_name])
        self.assertEqual(0, result.exit_code)

    def test_0026_move_to(self):
        """Move VM from one vApp to another."""
        test_vapp = VmTest._test_vapp
        test_vapp_resource = test_vapp.get_resource()
        VmTest._test_vapp_name = test_vapp_resource.get('name')
        result = VmTest._runner.invoke(
            vm,
            args=['move', VmTest._empty_vapp_name, VmTest._target_vm_name,
                  '--target-vapp-name', VmTest._test_vapp_name,
                  '--target-vm-name', VmTest._target_vm_name])
        self.assertEqual(0, result.exit_code)

    def test_0028_delete(self):
        """Delete VM from vApp"""
        result = VmTest._runner.invoke(
            vm, args=['delete', VmTest._test_vapp_name,
                      VmTest._target_vm_name])
        self.assertEqual(0, result.exit_code)

    def test_0030_power_on(self):
        """Power on the VM."""
        result = VmTest._runner.invoke(
            vm,
            args=['power-on', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0032_reboot(self):
        """Reboot the VM."""
        result = VmTest._runner.invoke(
            vm, args=['reboot', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0034_shutdown(self):
        """Shutdown the VM."""
        result = VmTest._runner.invoke(
            vm,
            args=['shutdown', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        # Again power on VM for further test cases.
        result = VmTest._runner.invoke(
            vm,
            args=['power-on', VAppConstants.name, VAppConstants.vm1_name])

    def test_0040_power_off(self):
        """Power off the VM."""
        result = VmTest._runner.invoke(
            vm,
            args=['power-off', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        # Again power on VM for further test cases.
        result = VmTest._runner.invoke(
            vm,
            args=['power-on', VAppConstants.name, VAppConstants.vm1_name])

    def test_0050_reset(self):
        """Reset the VM."""
        result = VmTest._runner.invoke(
            vm, args=['reset', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    # def test_0060_suspend(self):
    #     """Suspend the VM."""
    #     result = VmTest._runner.invoke(
    #         vm,
    #         args=['suspend', VAppConstants.name, VAppConstants.vm1_name])
    #     self.assertEqual(0, result.exit_code)
    #
    # def test_0070_discard_suspended_state(self):
    #     """Discard suspended state of the VM."""
    #     result = VmTest._runner.invoke(
    #         vm, args=['discard-suspend', VAppConstants.name,
    #                   VAppConstants.vm1_name])
    #     self.assertEqual(0, result.exit_code)

    def test_0080_install_vmware_tools(self):
        """Install vmware tools in the VM."""
        # result = VmTest._runner.invoke(
        #     vm,
        #     args=['power-on', VAppConstants.name, VAppConstants.vm1_name])
        # self.assertEqual(0, result.exit_code)
        result = VmTest._runner.invoke(
            vm, args=['install-vmware-tools', VAppConstants.name,
                      VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0090_insert_cd(self):
        """Insert CD in the VM."""
        media_id = VmTest._media_resource.Entity.get('id')
        media_id = media_id.split(':')[3]
        result = VmTest._runner.invoke(
            vm,
            args=['insert-cd', VAppConstants.name, VAppConstants.vm1_name,
                  '--media-id', media_id])
        self.assertEqual(0, result.exit_code)

    def test_0100_eject_cd(self):
        """Eject CD from the VM."""
        media_id = VmTest._media_resource.Entity.get('id')
        media_id = media_id.split(':')[3]
        result = VmTest._runner.invoke(
            vm,
            args=['eject-cd', VAppConstants.name, VAppConstants.vm1_name,
                  '--media-id', media_id])
        self.assertEqual(0, result.exit_code)

    def test_0110_add_nic(self):
        """Add a nic to the VM."""
        result = VmTest._runner.invoke(
            vm,
            args=[
                'add-nic', VAppConstants.name, VAppConstants.vm1_name,
                '--adapter-type', VmTest.DEFAULT_ADAPTER_TYPE, '--connect',
                '--primary', '--network', VAppConstants.network1_name,
                '--ip-address-mode', VmTest.DEFAULT_IP_MODE
            ])
        self.assertEqual(0, result.exit_code)

    def test_0115_update_nic(self):
        """update nic of the VM."""
        result = VmTest._runner.invoke(
            vm,
            args=[
                'update-nic', VAppConstants.name, VAppConstants.vm1_name,
                '--network', VAppConstants.network1_name
            ])
        self.assertEqual(0, result.exit_code)

    def test_0120_list_nics(self):
        """List all nics of the VM."""
        result = VmTest._runner.invoke(
            vm,
            args=['list-nics', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0130_delete_nic(self):
        """Delete a nic of the VM."""
        result = VmTest._runner.invoke(
            vm,
            args=[
                'delete-nic', VAppConstants.name, VAppConstants.vm1_name,
                '--index', 0
            ])
        self.assertEqual(0, result.exit_code)

    def test_0140_create_snapshot(self):
        """Create snapshot of VM"""
        result = VmTest._runner.invoke(
            vm, args=['create-snapshot', VAppConstants.name,
                      VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0150_revert_to_snapshot(self):
        """Revert VM to current snapshot."""
        result = VmTest._runner.invoke(
            vm, args=['revert-to-snapshot', VAppConstants.name,
                      VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0155_remove_snapshot(self):
        """Remove VM snapshot."""
        result = VmTest._runner.invoke(
            vm, args=['remove-snapshot', VAppConstants.name,
                      VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0160_attach_disk_to_vm(self):
        """Attach independent disk to VM."""
        result = VmTest._runner.invoke(
            vm,
            args=[
                'attach-disk', VAppConstants.name, VAppConstants.vm1_name,
                '--idisk-id',
                VmTest._idisk_id
            ])
        self.assertEqual(0, result.exit_code)

    def test_0170_detach_disk_from_vm(self):
        """Detach independent disk from VM."""
        vdc = Environment.get_test_vdc(VmTest._client)
        result = VmTest._runner.invoke(
            vm,
            args=[
                'detach-disk', VAppConstants.name, VAppConstants.vm1_name,
                '--idisk-id',
                VmTest._idisk_id
            ])
        self.assertEqual(0, result.exit_code)

    def test_0180_deploy_undeploy_vm(self):
        # Undeploy VM
        result = VmTest._runner.invoke(
            vm,
            args=['undeploy', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        result = VmTest._runner.invoke(
            vm, args=['deploy', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0190_upgrade_virtual_hardware(self):
        # Undeploy VM
        result = VmTest._runner.invoke(
            vm,
            args=['undeploy', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        # Upgrade virtual hardware of VM.
        result = VmTest._runner.invoke(
            vm,
            args=[
                'upgrade-virtual-hardware', VAppConstants.name,
                VAppConstants.vm1_name
            ])
        self.assertEqual(0, result.exit_code)
        # Again deploy VM for further test cases.
        result = VmTest._runner.invoke(
            vm, args=['deploy', VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0200_general_setting_detail(self):
        # general setting details
        result = VmTest._runner.invoke(
            vm,
            args=[
                'general-setting', VAppConstants.name,
                VAppConstants.vm1_name
            ])
        self.assertEqual(0, result.exit_code)

    def test_0210_list_storage_profile(self):
        result = VmTest._runner.invoke(
            vm,
            args=[
                'list-storage-profile', VAppConstants.name,
                VAppConstants.vm1_name
            ])
        self.assertEqual(0, result.exit_code)

    def test_0220_reload_from_vc(self):
        # Reload VM from VC
        default_org = self._config['vcd']['default_org_name']
        self._sys_login()
        VmTest._runner.invoke(org, ['use', default_org])
        VmTest._runner.invoke(vdc, ['use', VmTest._default_ovdc])
        result = VmTest._runner.invoke(
            vm, args=['reload-from-vc',
                      VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0230_check_compliance(self):
        # Check compliance of VM
        result = VmTest._runner.invoke(
            vm, args=['check-compliance',
                      VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        self._logout()
        self._login()
        VmTest._runner.invoke(vdc, ['use', VmTest._default_ovdc])

    def test_0240_customize_on_next_power_on(self):
        # Customize on next power on
        result = VmTest._runner.invoke(
            vm, args=['customize-on-next-poweron',
                      VAppConstants.name, VAppConstants.vm1_name])

    def test_0250_gc_enable(self):
        # Enable guest customization
        result = VmTest._runner.invoke(
            vm, args=['gc-enable',
                      VmTest._test_vapp_vmtools_name,
                      VmTest._test_vapp_vmtools_vm_name, '--enable'])
        self.assertEqual(0, result.exit_code)

    def test_0260_get_gc_status(self):
        # Get guest customization status
        result = VmTest._runner.invoke(
            vm, args=['gc-status',
                      VmTest._test_vapp_vmtools_name,
                      VmTest._test_vapp_vmtools_vm_name])
        self.assertEqual(0, result.exit_code)

    def test_0270_poweron_and_force_recustomizations(self):
        # Power off VM.
        result = VmTest._runner.invoke(
            vm, args=['undeploy', VmTest._test_vapp_vmtools_name,
                      VmTest._test_vapp_vmtools_vm_name])
        self.assertEqual(0, result.exit_code)
        # Power on and force recustomize VM.
        result = VmTest._runner.invoke(
            vm, args=['poweron-force-recustomize',
                      VmTest._test_vapp_vmtools_name,
                      VmTest._test_vapp_vmtools_vm_name])
        self.assertEqual(0, result.exit_code)

    def test_0280_list_virtual_hardware_section(self):
        # list virtual hardware section
        result = VmTest._runner.invoke(
            vm, args=['list-virtual-hardware-section',
                      VmTest._test_vapp_vmtools_name,
                      VmTest._test_vapp_vmtools_vm_name])
        self.assertEqual(0, result.exit_code)

    def test_0290_get_compliance_result(self):
        # Get compliance result
        default_org = self._config['vcd']['default_org_name']
        self._sys_login()
        VmTest._runner.invoke(org, ['use', default_org])
        VmTest._runner.invoke(vdc, ['use', VmTest._default_ovdc])
        result = VmTest._runner.invoke(
            vm, args=['get-compliance-result',
                      VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)
        self._logout()
        self._login()
        VmTest._runner.invoke(vdc, ['use', VmTest._default_ovdc])

    def test_0300_list_current_metrics(self):
        # list current metrics
        result = VmTest._runner.invoke(
            vm, args=['list-current-metrics',
                      VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0310_list_subset_current_metrics(self):
        # list subset of current metrics based on metric pattern
        result = VmTest._runner.invoke(
            vm, args=['list-subset-current-metrics',
                      VAppConstants.name, VAppConstants.vm1_name,
                      '--metric-pattern', VmTest._metric_pattern])
        self.assertEqual(0, result.exit_code)

    def test_0320_update_general_setting(self):
        # System admin login
        default_org = self._config['vcd']['default_org_name']
        self._sys_login()
        VmTest._runner.invoke(org, ['use', default_org])
        VmTest._runner.invoke(vdc, ['use', VmTest._default_ovdc])
        # update general setting
        result = VmTest._runner.invoke(
            vm,
            args=[
                'update-general-setting', VmTest._vapp_name,
                VmTest._vm_name,
                '--name', VmTest._vm_name_update, '--d',
                VmTest._description_update, '--cn',
                VmTest._computer_name_update, '--bd',
                VmTest._boot_delay_update, '--ebs',
                VmTest._enter_bios_setup_update
            ])
        self.assertEqual(0, result.exit_code)
        # logging out sys_client
        self._logout()
        # logging with org admin user
        self._login()

    def test_0330_relocate(self):
        # relocate VM to given datastore
        default_org = self._config['vcd']['default_org_name']
        self._sys_login()
        VmTest._runner.invoke(org, ['use', default_org])
        VmTest._runner.invoke(vdc, ['use', VmTest._default_ovdc])
        result = VmTest._runner.invoke(
            vm, args=['relocate',
                      VAppConstants.name, VAppConstants.vm1_name,
                      '--datastore-id', VmTest._datastore_id])
        self.assertEqual(0, result.exit_code)

    def _power_off_and_undeploy(self, vapp):
        if vapp.is_powered_on():
            task = vapp.power_off()
            VmTest._client.get_task_monitor().wait_for_success(task)
            task = vapp.undeploy()
            VmTest._client.get_task_monitor().wait_for_success(task)

    def test_0340_list_os_section(self):
        # list os section properties
        result = VmTest._runner.invoke(
            vm, args=['list-os-section',
                      VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0340_update_os_section(self):
        # update os section properties
        result = VmTest._runner.invoke(
            vm, args=['update-os-section',
                      VAppConstants.name, VAppConstants.vm1_name,
                      '--ovf-info', VmTest._new_ovf_info])
        self.assertEqual(0, result.exit_code)

    def test_0350_list_gc_section(self):
        # list gc section properties
        result = VmTest._runner.invoke(
            vm, args=['list-gc-section',
                      VmTest._test_vapp_vmtools_name,
                      VmTest._test_vapp_vmtools_vm_name])
        self.assertEqual(0, result.exit_code)

    def test_0360_update_gc_section(self):
        # update os section properties
        result = VmTest._runner.invoke(
            vm, args=['update-gc-section',
                      VmTest._test_vapp_vmtools_name,
                      VmTest._test_vapp_vmtools_vm_name,
                      '--disable'])
        self.assertEqual(0, result.exit_code)

    def test_0370_check_post_gc_script_status(self):
        # check post gc script status
        result = VmTest._runner.invoke(
            vm, args=['check-post-gc-script',
                      VmTest._test_vapp_vmtools_name,
                      VmTest._test_vapp_vmtools_vm_name])
        self.assertEqual(0, result.exit_code)

    def test_0380_list_vm_capabilities(self):
        # list vm capabilities section properties
        result = VmTest._runner.invoke(
            vm, args=['list-vm-capabilities',
                      VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0390_update_vm_capabilities(self):
        # update vm capabilities section properties
        result = VmTest._runner.invoke(
            vm, args=['update-vm-capabilities',
                      VAppConstants.name, VAppConstants.vm1_name,
                      '--disable-memory-hot-add'])
        self.assertEqual(0, result.exit_code)

    def test_0400_list_runtime_info(self):
        # list runtime info properties
        result = VmTest._runner.invoke(
            vm, args=['list-runtime-info',
                      VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0410_list_boot_options(self):
        # list boot options properties
        result = VmTest._runner.invoke(
            vm, args=['list-boot-options',
                      VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0420_update_boot_options(self):
        # update boot options properties
        result = VmTest._runner.invoke(
            vm, args=['update-boot-options',
                      VAppConstants.name, VAppConstants.vm1_name,
                      '--disable-enter-bios-setup'])
        self.assertEqual(0, result.exit_code)

    def test_0430_set_metadata(self):
        # Set metadata
        result = VmTest._runner.invoke(
            vm, args=['set-metadata',
                      VAppConstants.name, VAppConstants.vm1_name,
                      '--domain', 'GENERAL', '--visibility', 'READWRITE',
                      '--key', 'key1', '--value',
                      'value1', '--value-type', 'MetadataStringValue'])
        self.assertEqual(0, result.exit_code)

    def test_0440_update_metadata(self):
        # update metadata
        result = VmTest._runner.invoke(
            vm, args=['update-metadata',
                      VAppConstants.name, VAppConstants.vm1_name,
                      '--domain', 'GENERAL', '--visibility', 'READWRITE',
                      '--key', 'key1', '--value',
                      'value2', '--value-type', 'MetadataStringValue'])
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

    def test_0470_list_screen_ticket(self):
        # list screen ticket
        result = VmTest._runner.invoke(
            vm, args=['list-screen-ticket',
                      VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0480_mks_ticket(self):
        # list mks ticket
        result = VmTest._runner.invoke(
            vm, args=['list-screen-ticket',
                      VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0490_list_product_sections(self):
        # list product sections
        result = VmTest._runner.invoke(
            vm, args=['list-product-sections',
                      VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_0500_update_vhs_disk(self):
        # update virtual hardware section disk
        vm1 = VM(VmTest._sys_admin_client,
                href=VmTest._test_vapp.get_vm(VAppConstants.vm1_name).get(
                    'href'))
        disk_list = vm1.list_virtual_hardware_section(is_cpu=False,
                                                     is_memory=False,
                                                     is_disk=True)
        for disk in disk_list:
            element_name = disk['diskElementName']
            virtual_quantity = disk['diskVirtualQuantityInBytes']
            break
        result = VmTest._runner.invoke(
            vm, args=['update-vhs-disk',
                      VAppConstants.name, VAppConstants.vm1_name,
                      '--e-name', element_name, '--v-quantity',
                      virtual_quantity])
        self.assertEqual(0, result.exit_code)

    def test_0510_enable_nested_hypervisor(self):
        vapp = VApp(VmTest._client, href=VmTest._test_old_vapp_href)
        self._power_off_and_undeploy(vapp=vapp)
        result = VmTest._runner.invoke(
            vm, args=['enable-nested-hypervisor',
                      VAppConstants.name, VAppConstants.vm1_name])
        self.assertEqual(0, result.exit_code)

    def test_9998_tearDown(self):
        """Delete the vApp created during setup.

        This test passes if the task for deleting the vApp succeed.
        """
        vapps_to_delete = []

        if VmTest._empty_vapp_href is not None:
            vapps_to_delete.append(VmTest._empty_vapp_name)
        vapp = VApp(VmTest._client, href=VmTest._test_old_vapp_href)
        self._power_off_and_undeploy(vapp=vapp)
        vapp = VApp(VmTest._client, href=VmTest._test_vapp_vmtools_href)
        self._power_off_and_undeploy(vapp=vapp)
        vapp = VApp(VmTest._client, href=VmTest._test_vapp_href)
        self._power_off_and_undeploy(vapp=vapp)
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
