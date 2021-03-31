```
Usage: vcd vm [OPTIONS] COMMAND [ARGS]...

  Manage VMs in vCloud Director.

      Examples
          vcd vm list
              Get list of VMs in current virtual datacenter.

          vcd vm info vapp1 vm1
              Get details of the VM 'vm1' in vApp 'vapp1'.

          vcd vm update vapp1 vm1 --cpu 2 --core 2
              Modifies the VM 'vm1' in vApp 'vapp1' to be configured
              with 2 cpu and 2 cores .

          vcd vm update vapp1 vm1 --memory 512
              Modifies the VM 'vm1' in vApp 'vapp1' to be configured
              with the specified memory .

          vcd vm update vapp1 vm1 --cpu 2 --memory 512
              Modifies the VM 'vm1' in vApp 'vapp1' to be configured
              with 2 cpu and the specified memory .

          vcd vm add-nic vapp1 vm1
                  --adapter-type VMXNET3
                  --primary
                  --connect
                  --network network_name
                  --ip-address-mode MANUAL
                  --ip-address 192.168.1.10
              Adds a nic to the VM.

          vcd vm update-nic vapp1 vm1
                  --adapter-type VMXNET3
                  --primary
                  --connect
                  --network network_name
                  --ip-address-mode MANUAL
                  --ip-address 192.168.1.10
              Update a nic of the VM.

          vcd vm list-nics vapp1 vm1
              Lists the nics of the VM.

          vcd vm delete-nic vapp1 vm1
                  --index 1
              Deletes the nic at given index.

          vcd vm power-on vapp1 vm1
              Power on the VM.

          vcd vm power-off vapp1 vm1
              Power off the VM.

          vcd vm reboot vapp1 vm1
              Reboot the VM.

          vcd vm shutdown vapp1 vm1
              Shutdown the VM.

          vcd vm suspend vapp1 vm1
              Suspend the VM.

          vcd vm discard-suspend vapp1 vm1
              Discard suspended state of the VM.

          vcd vm reset vapp1 vm1
              Reset the VM.

          vcd vm install-vmware-tools vapp1 vm1
              Install vmware tools in the VM.

          vcd vm insert-cd vapp1 vm1
                  --media-id 76e53c34-1845-43ca-bd5a-759c0d537433
              Insert CD from catalog to the VM.

          vcd vm eject-cd vapp1 vm1
                  --media-id 76e53c34-1845-43ca-bd5a-759c0d537433
              Eject CD from the VM.

          vcd vm consolidate vapp1 vm1
              Consolidate the VM.

          vcd vm create-snapshot vapp1 vm1
              Create snapshot of the VM.

          vcd vm revert-to-snapshot vapp1 vm1
              Revert VM to current snapshot.

          vcd vm remove-snapshot vapp1 vm1
              Remove VM snapshot.

          vcd vm copy vapp1 vm1 vapp2 vm2
              Copy VM from one vapp to another vapp.

          vcd vm move vapp1 vm1 vapp2 vm2
              Move VM from one vapp to another vapp.

          vcd vm delete vapp1 vm1
              Delete VM.

          vcd vm attach-disk vapp1 vm1
                 --idisk-id 76e53c34-1845-43ca-bd5a-759c0d537433
              Attach independent disk to VM.

          vcd vm detach-disk vapp1 vm1
                 --idisk-id 76e53c34-1845-43ca-bd5a-759c0d537433
              Detach independent disk from VM.

          vcd vm deploy vapp1 vm1
              Deploy a VM.

          vcd vm undeploy vapp1 vm1
              Undeploy a VM.

          vcd vm upgrade-virtual-hardware vapp1 vm1
              Upgrade virtual hardware of VM.

          vcd vm general-setting vapp1 vm1
              Show general setting details of VM.

          vcd vm list-storage-profile vapp1 vm1
              List all storage profiles of VM.

          vcd vm reload-from-vc vapp1 vm1
              Reload VM from VC.

          vcd vm check-compliance vapp1 vm1
              Check compliance of VM.

          vcd vm gc-enable vapp1 vm1
                  --enable
              Enable guest customization of VM.

          vcd vm gc-status vapp1 vm1
              Returns guest customization status of VM.

          vcd vm customize-on-next-poweron vapp1 vm1
              Customize on next power on of VM.

          vcd vm poweron-force-recustomize vapp1 vm1
              Power on and force re-customize VM.

          vcd vm list-virtual-hardware-section vapp1 vm1
              List virtual hadware section of VM.

          vcd vm get-compliance-result vapp1 vm1
              Get compliance result of VM.

          vcd vm list-current-metrics vapp1 vm1
              List current metrics of VM.

          vcd vm list-subset-current-metrics vapp1 vm1
                  --metric-pattern *.average
              List subset of current metrics of VM based on metric pattern.

          vcd vm list-historic-metrics vapp1 vm1
              List historic metrics of VM.

          vcd vm list-sample-historic-data vapp1 vm1
                  --metric-name disk.read.average
              List historic sample data of given metric of VM.

          vcd vm update-general-setting vapp1 vm1 --name vm_new_name
              --d vm_new_description --cn new_computer_name --bd 60
              --ebs True
              Update general setting details of VM.

          vcd vm relocate vapp1 vm1
                  --datastore-id 0d8c7358-3e8d-4862-9364-68155069d252
              Relocate VM to given datastore.

          vcd vm list-os-section vapp1 vm1
              List OS section properties of VM.

          vcd vm update-os-section vapp1 vm1
                  --ovf-info newInfo
                  --description newDescription
              Update OS section properties of VM.

          vcd vm list-gc-section vapp1 vm1
              List guest customization section properties of VM.

          vcd vm update-gc-section
                  --disable
              Update guest customization section properties of VM.

          vcd vm check-post-gc-script vapp1 vm1
              Check post guest customization script status of VM.

          vcd vm list-vm-capabilities vapp1 vm1
              List VM capabilities section properties of VM.

          vcd vm update-vm-capabilities
                  --enable-memory-hot-add
              Update VM capabilities section properties of VM.

          vcd vm list-runtime-info vapp1 vm1
              List runtime info properties of VM.

          vcd vm list-boot-options vapp1 vm1
              List boot options properties of VM.

          vcd vm update-boot-options vapp1 vm1
                  --enable-enter-bios-setup
              Update boot options properties of VM.

          vcd vm set-metadata vapp1 vm1
                  --domain GENERAL
                  --visibility READWRITE
                  --key key1
                  --value value1
                  --value-type MetadataStringValue
              Set metadata of VM.

          vcd vm update-metadata vapp1 vm1
                  --domain GENERAL
                  --visibility READWRITE
                  --key key1
                  --value value2
                  --value-type MetadataStringValue
              Update metadata of VM.

          vcd vm list-metadata vapp1 vm1
              List metadata of VM.

          vcd vm remove-metadata vapp1 vm1
                  --domain GENERAL
                  --key key1
              Remove metadata of VM.

          vcd vm list-screen-ticket vapp1 vm1
              List screen ticket of VM.

          vcd vm list-mks-ticket vapp1 vm1
              List mks ticket of VM.

          vcd vm list-product-sections vapp1 vm1
              List product sections of VM.

          vcd vm update-vhs-disk vapp1 vm1
                  --e-name 'Hard Disk 1'
                  --v-quantity 694487
              Update virtual hardware section disk of VM.

          vcd vm update-vhs-media  vapp1 vm1
                  --e-name 'CD DVD DRive'
                  --host-resource pb1.iso
              Update virtual hardware section media of VM.

          vcd vm enable-nested-hypervisor vapp1 vm1
              Enable nested hypervisor of VM.
      

Options:
  -h, --help  Show this message and exit.

Commands:
  add-nic                        Add a nic to the VM
  attach-disk                    attach independent disk to VM
  check-compliance               check compliance of VM
  check-post-gc-script           check post guest customizationscript of VM
  consolidate                    consolidate VM
  copy                           copy vm from one vapp to another vapp
  create-snapshot                create snapshot of a VM
  customize-on-next-poweron      customize on next power on of VM
  delete                         delete VM
  delete-nic                     Delete the nic with the index
  deploy                         deploy a VM
  detach-disk                    detach independent disk from VM
  discard-suspend                discard suspend state of a VM
  eject-cd                       eject CD from VM
  enable-nested-hypervisor       enable nested hypervisor of VM
  gc-enable                      enable/disable the guest customization
  gc-status                      get guest customization status
  general-setting                general setting detail of VM
  get-compliance-result          get compliance result of VM
  info                           show VM details
  insert-cd                      insert CD from catalog
  install-vmware-tools           instal vmware tools
  list                           list VMs
  list-boot-options              list boot options properties of VM
  list-current-metrics           list current metrics of VM
  list-gc-section                list guest customization section properties
                                 of VM

  list-historic-metrics          list historic metrics of VM
  list-metadata                  list metadata of VM
  list-mks-ticket                list mks ticket of VM
  list-nics                      List all the nics of the VM
  list-os-section                list operating system section properties of
                                 VM

  list-product-sections          list product sections of VM
  list-runtime-info              list runtime info properties of VM
  list-sample-historic-data      list sample historic data of given metric of
                                 VM

  list-screen-ticket             list screen ticket of VM
  list-storage-profile           list all storage profiles of VM
  list-subset-current-metrics    list subset of current metrics of VM
  list-virtual-hardware-section  list virtual hardware section of VM
  list-vm-capabilities           list VM capabilities section properties
  move                           move VM from one vapp to another vapp
  power-off                      power off a VM
  power-on                       power on a VM
  poweron-force-recustomize      power on and force recustomize VM
  reboot                         reboot a VM
  reload-from-vc                 reload VM from VC
  relocate                       relocate VM to given datastore
  remove-metadata                remove metadata of VM
  remove-snapshot                remove VM snaphot
  reset                          reset a VM
  revert-to-snapshot             revert VM to current snapshot
  set-metadata                   set an entity as metadata of VM
  shutdown                       shutdown a VM
  suspend                        suspend a VM
  undeploy                       undeploy a VM
  update                         Update the VM properties and configurations
  update-boot-options            update boot options properties
  update-gc-section              update guest customization section properties
                                 of VM

  update-general-setting         update general setting of VM
  update-metadata                update metadata of VM
  update-nic                     Update a nic to the VM
  update-os-section              update os section properties of VM
  update-vhs-disk                update virtual hardware section disk of VM
  update-vhs-media               update virtual hardware section media of VM
  update-vm-capabilities         update VM capabilities properties
  upgrade-virtual-hardware       upgrade virtual hardware of VM

```
