```
Usage: vcd vapp [OPTIONS] COMMAND [ARGS]...

  Manage vApps in vCloud Director.

      Description
          The vapp command manages vApps.

          'vapp create' creates a new vApp in the current vDC. When '--catalog'
          and '--template' are not provided, it creates an empty vApp and VMs can
          be added later. When specifying a template in a catalog, it creates an
          instance of the catalog template.

          'vapp add-vm' adds a VM to the vApp. When '--catalog' is used, the
          <source-vapp> parameter refers to a template in the specified catalog
          and the command will instantiate the <source-vm> found in the template.
          If '--catalog' is not used, <source-vapp> refers to another vApp in the
          vDC and the command will copy the <source-vm> found in the vApp. The
          name of the VM and other options can be customized when the VM is added
          to the vApp.

      Examples
          vcd vapp list
              Get list of vApps in current virtual datacenter.

          vcd vapp list vapp1
              Get list of VMs in vApp 'vapp1'.

          vcd vapp list --filter name==vapp1
              Get list of vApp with name vapp1.

          vcd vapp list --filter ownerName==user1
              Get list of vApp with ownername 'user1'.

          vcd vapp list --filter numberOfVMs==7
              Get list of vApp with numberOfVMs 7.

          vcd vapp list --filter vdcName==ovdc1
              Get list of vApp with vdcName 'ovdc1'.

          vcd vapp info vapp1
              Get details of the vApp 'vapp1'.

          vcd vapp create vapp1
              Create an empty vApp with name 'vapp1'.

          vcd vapp create vapp1 --network net1
              Create an empty vApp connected to a network.

          vcd vapp create vapp1 -c catalog1 -t template1
              Instantiate a vApp from a catalog template.

          vcd vapp create vapp1 -c catalog1 -t template1
                   --cpu 4 --memory 4096 --disk-size 20000
                   --network net1 --ip-allocation-mode pool
                   --hostname myhost --vm-name vm1 --accept-all-eulas
                   --storage-profile '*'
              Instantiate a vApp with customized settings.

          vcd vapp update vapp1 -n vapp-new-name -d "new description"
              Updates vApp name and description.

          vcd vapp delete vapp1 --yes --force
              Delete a vApp.

          vcd --no-wait vapp delete vapp1 --yes --force
              Delete a vApp without waiting for completion.

          vcd vapp update-lease vapp1 7776000
              Set vApp lease to 90 days.

          vcd vapp update-lease vapp1 0
              Set vApp lease to no expiration.

          vcd vapp shutdown vapp1 --yes
              Gracefully shutdown a vApp.

          vcd vapp reboot vapp1 --yes
              Reboot a vApp.

          vcd vapp power-off vapp1
              Power off a vApp.

          vcd vapp power-off vapp1 vm1 vm2
              Power off vm1 and vm2 of vapp1.

          vcd vapp reset vapp1 vm1 vm2
              Power reset vm1 and vm2 of vapp1.

          vcd vapp deploy vapp1 vm1 vm2
              Deploy vm1 and vm2 of vapp1.

          vcd vapp undeploy vapp1 vm1 vm2
              Undeploy vm1 and vm2 of vapp1.

          vcd vapp stop vapp1
              stop a vApp.

          vcd vapp delete vapp1 vm1 vm2
              Delete vm1 and vm2 from vapp1.

          vcd vapp reboot vapp1 vm1 vm2 --yes
              Reboot vm1 and vm2 in vApp.

          vcd vapp shutdown vapp1 vm1 vm2 --yes
              Shutdown vm1 and vm2 in vApp.

          vcd vapp power-on vapp1
              Power on a vApp.

          vcd vapp reset vapp1
              Power reset vapp1.

          vcd vapp deploy vapp1
              Deploy vapp1.

          vcd vapp power-on vapp1 vm1 vm2
              Power on vm1 and vm2 of vapp1.

          vcd vapp capture vapp1 catalog1
              Capture a vApp as a template in a catalog.

          vcd vapp download vapp1 file.ova
              Download a vapp.

          vcd vapp attach vapp1 vm1 disk1
              Attach a disk to a VM in the given vApp.

          vcd vapp detach vapp1 vm1 disk1
              Detach a disk from a VM in the given vApp.

          vcd vapp add-disk vapp1 vm1 10000
              Add a disk of 10000 MB to a VM.

          vcd vapp add-vm vapp1 template1.ova vm1 -c catalog1
              Add a VM to a vApp. Instantiate the source VM 'vm1' that is in
              the 'template1.ova' template in the 'catalog1' catalog and
              place the new VM inside 'vapp1' vApp.

          vdc vapp connect vapp1 org-vdc-network1
              Connects the network org-vdc-network1 to vapp1.

          vdc vapp disconnect vapp1 org-vdc-network1
              Disconnects the network org-vdc-network1 from vapp1.

          vcd vapp suspend vapp1
              Suspend a vapp.

          vcd vapp discard-suspended-state vapp1
              Discard suspended state of vapp.

          vcd vapp enter-maintenance-mode vapp1
              Place a vApp in Maintenance Mode.

          vcd vapp exit-maintenance-mode vapp1
              Exit maintenance mode a vapp.

          vcd vapp upgrade-virtual-hardware vapp1
              Upgrade virtual hardware of vapp.

          vcd vapp copy vapp1 -n new_vapp_name -v target_vdc -d description
              Copy a vapp to target vdc.

          vcd vapp move vapp1 -v target_vdc
              Move a vapp to target vdc.

          vcd vapp create-snapshot vapp1
              Create snapshot of the vapp.

          vcd vapp revert-to-snapshot vapp1
              Revert to to current snapshot of the vapp.

          vcd vapp remove-snapshot vapp1
              Remove snapshot of the vapp.

          vcd vapp enable-download vapp1
              Enable download of the vapp.

          vcd vapp disable-download vapp1
              Disable download of the vapp.

          vcd vapp show-lease vapp1
              Show vApp lease details.

          vcd vapp show-metadata vapp1
              Show metadata of vapp.

          vcd vapp update-startup-section vapp1 testvm1 --o 1 --start-action
              powerOn --start-delay 4 --stop-action guestShutdown --stop-delay 3
              Update startup section of vapp

          vcd vapp show-startup-section vapp1
              Show startup section data of vapp.

          vcd vapp show-product-section vapp1
              Show product section data of vapp.

          vcd vapp update-product-section vapp1 --key testkey --value testvalue
              --class_name testclassname --instance_name testinstancename --label
              labledata --is_password true --user_configurable false
              Update product section of vapp.

          vcd vapp add-vm-scratch vapp1 -vm vm1 -cn computer_name -d description
                  -os windows7_64Guest -cpu 2 -cps 2 -crm 2 -m 1024 -media
                  pb1.iso -aae -deploy -power-on
              Add a VM from scratch to a vApp.
      

Options:
  -h, --help  Show this message and exit.

Commands:
  acl                       work with vapp acl
  add-disk                  add disk to vm
  add-vm                    add VM to vApp
  add-vm-scratch            add VM from scratch to vApp
  attach                    attach disk to VM in vApp
  capture                   Capture a vApp as template
  change-owner              change vApp owner
  connect                   connect an ovdc network to a vapp
  copy                      copy a vapp
  create                    create a vApp
  create-snapshot           create snapshot of a vapp
  delete                    delete a vApp or VM(s)
  deploy                    Deploy a vApp or VM(s)
  detach                    detach disk from VM in vApp
  disable-download          disbale a vapp for download
  discard-suspended-state   discard suspended state of vApp
  disconnect                disconnect an ovdc network from a vapp
  download                  Download a vApp
  enable-download           enable a vapp for download
  enter-maintenance-mode    Place a vApp in Maintenance Mode
  exit-maintenance-mode     exit maintenance mode a vApp
  info                      show vApp details
  list                      list vApps
  move                      move a vapp
  network                   work with vapp network
  power-off                 power off a vApp
  power-on                  power on a vApp or VM(s)
  reboot                    Reboot a vApp or VM(s)
  remove-snapshot           rmove snapshot of vapp
  reset                     Reset a vApp or VM(s)
  revert-to-snapshot        revert vapp to current snapshot
  show-lease                show a vapp lease details
  show-metadata             show metadata of vapp
  show-product-section      show product sections of vapp
  show-startup-section      show startup section of vapp
  shutdown                  shutdown a vApp
  stop                      stop a vApp
  suspend                   suspend a vApp
  undeploy                  undeploy a vApp or VM(s)
  update                    update vapp's name and description
  update-lease              update vApp lease
  update-product-section    update product section of vapp
  update-startup-section    update startup section of vapp for vm
  upgrade-virtual-hardware  upgrade virtual hardware of a vApp
  use                       set active vApp

```
