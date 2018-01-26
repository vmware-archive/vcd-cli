```
Usage: vcd vapp [OPTIONS] COMMAND [ARGS]...

  Manage vApps in vCloud Director.

      Description
          The vapp command manages vApps.
  
          'vapp create' creates a new vApp in the current vDC. When '--catalog'
          and '--template' are not provided, it creates an empty vApp and VMs can
          be added later. When specifying a template in a catalog, it creates an
          instance of the catalog template.
  
          'vapp add-vm' adds a VM to the vApp. When '--catalog' is used, the
          <source-vapp> parameter refers to a template in the specified catalog
          and the command will instantiate the <source-vm> found in the template.
          If '--catalog' is not used, <source-vapp> refers to another vApp in the
          vDC and the command will copy the <source-vm> found in the vApp. The
          name of the VM and other options can be customized when the VM is added
          to the vApp.
  
      Examples
          vcd vapp list
              Get list of vApps in current virtual datacenter.
  
          vcd vapp list vapp1
              Get list of VMs in vApp 'vapp1'.
  
          vcd vapp info vapp1
              Get details of the vApp 'vapp1'.
  
          vcd vapp create vapp1
              Create an empty vApp with name 'vapp1'.
  
          vcd vapp create vapp1 --network net1
              Create an empty vApp connected to a network.
  
          vcd vapp create vapp1 -c catalog1 -t template1
              Instantiate a vApp from a catalog template.
  
          vcd vapp create vapp1 -c catalog1 -t template1 \
                   --cpu 4 --memory 4096 --disk-size 20000 \
                   --network net1 --ip-allocation-mode pool \
                   --hostname myhost --vm-name vm1 --accept-all-eulas \
                   --storage-profile '*'
              Instantiate a vApp with customized settings.
  
          vcd vapp delete vapp1 --yes --force
              Delete a vApp.
  
          vcd --no-wait vapp delete vapp1 --yes --force
              Delete a vApp without waiting for completion.
  
          vcd vapp update-lease vapp1 7776000
              Set vApp lease to 90 days.
  
          vcd vapp update-lease vapp1 0
              Set vApp lease to no expiration.
  
          vcd vapp shutdown vapp1 --yes
              Gracefully shutdown a vApp.
  
          vcd vapp reboot vapp1 --yes
              Reboot a vApp.
  
          vcd vapp power-off vapp1
              Power off a vApp.
  
          vcd vapp power-off vapp1 vm1 vm2
              Power off vm1 and vm2 of vapp1.
  
          vcd vapp reset vapp1 vm1 vm2
              Power reset vm1 and vm2 of vapp1.
  
          vcd vapp deploy vapp1 vm1 vm2
              Deploy vm1 and vm2 of vapp1.
  
          vcd vapp undeploy vapp1 vm1 vm2
              Undeploy vm1 and vm2 of vapp1.
  
          vcd vapp delete vapp1 vm1 vm2
              Delete vm1 and vm2 from vapp1.
  
          vcd vapp reboot vapp1 vm1 vm2 --yes
              Reboot vm1 and vm2 in vApp.
  
          vcd vapp shutdown vapp1 vm1 vm2 --yes
              Shutdown vm1 and vm2 in vApp.
  
          vcd vapp power-on vapp1
              Power on a vApp.
  
          vcd vapp reset vapp1
              Power reset vapp1.
  
          vcd vapp deploy vapp1
              Deploy vapp1.
  
          vcd vapp power-on vapp1 vm1 vm2
              Power on vm1 and vm2 of vapp1.
  
          vcd vapp capture vapp1 catalog1
              Capture a vApp as a template in a catalog.
  
          vcd vapp attach vapp1 vm1 disk1
              Attach a disk to a VM in the given vApp.
  
          vcd vapp detach vapp1 vm1 disk1
              Detach a disk from a VM in the given vApp.
  
          vcd vapp add-disk vapp1 vm1 10000
              Add a disk of 10000 MB to a VM.
  
          vcd vapp add-vm vapp1 template1.ova vm1 -c catalog1
              Add a VM to a vApp. Instantiate the source VM 'vm1' that is in
              the 'template1.ova' template in the 'catalog1' catalog and
              place the new VM inside 'vapp1' vApp.
  
          vdc vapp connect vapp1 org-vdc-network1
              Connects the network org-vdc-network1 to vapp1.

          vdc vapp disconnect vapp1 org-vdc-network1
              Disconnects the network org-vdc-network1 from vapp1.
      

Options:
  -h, --help  Show this message and exit.

Commands:
  acl           work with vapp acl
  add-disk      add disk to vm
  add-vm        add VM to vApp
  attach        attach disk to VM in vApp
  capture       save a vApp as a template
  change-owner  change vApp owner
  connect       connect an ovdc network to a vapp
  create        create a vApp
  delete        delete a vApp or VM(s)
  deploy        Deploy a vApp or VM(s)
  detach        detach disk from VM in vApp
  disconnect    disconnect an ovdc network from a vapp
  info          show vApp details
  list          list vApps
  power-off     power off a vApp
  power-on      power on a vApp or VM(s)
  reboot        Reboot a vApp or VM(s)
  reset         Reset a vApp or VM(s)
  shutdown      shutdown a vApp
  undeploy      undeploy a vApp or VM(s)
  update-lease  update vApp lease
  use           set active vApp

```
