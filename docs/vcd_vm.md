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
                  --media-href https://10.11.200.00/api/media/76e53c34-1845-43ca-bd5a-759c0d537433
              Insert CD from catalog to the VM.

          vcd vm eject-cd vapp1 vm1
                  --media-href https://10.11.200.00/api/media/76e53c34-1845-43ca-bd5a-759c0d537433
              Eject CD from the VM.

          vcd vm consolidate vapp1 vm1
              Consolidate the VM.

          vcd vm create-snapshot vapp1 vm1
              Create snapshot of the VM.

          vcd vm revert-to-snapshot vapp1 vm1
              Revert VM to current snapshot.

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

          vcd vm customize-on-next-poweron vapp1 vm1
              Customize on next power on of VM.

          vcd vm update-compute-policies vapp1 vm1
                 --sizing 'System Default'
                 --placement 'ESXi in Rack1'
              Update compute policies of VM.


Options:
  -h, --help  Show this message and exit.

Commands:
  add-nic                    Add a nic to the VM
  attach-disk                attach independent disk to VM
  check-compliance           check compliance of VM
  consolidate                consolidate VM
  copy                       copy vm from one vapp to another vapp
  create-snapshot            create snapshot of a VM
  customize-on-next-poweron  customize on next power on of VM
  delete                     delete VM
  delete-nic                 Delete the nic with the index
  deploy                     deploy a VM
  detach-disk                detach independent disk from VM
  discard-suspend            discard suspend state of a VM
  eject-cd                   eject CD from VM
  general-setting            general setting detail of VM
  info                       show VM details
  insert-cd                  insert CD from catalog
  install-vmware-tools       instal vmware tools
  list                       list VMs
  list-nics                  List all the nics of the VM
  list-storage-profile       list all storage profiles of VM
  move                       move VM from one vapp to another vapp
  power-off                  power off a VM
  power-on                   power on a VM
  reboot                     reboot a VM
  reload-from-vc             reload VM from VC
  reset                      reset a VM
  revert-to-snapshot         revert VM to current snapshot
  shutdown                   shutdown a VM
  suspend                    suspend a VM
  undeploy                   undeploy a VM
  update                     Update the VM properties and configurations
  update-compute-policies        Update the VM placement and sizing policy
  upgrade-virtual-hardware   upgrade virtual hardware of VM

```
