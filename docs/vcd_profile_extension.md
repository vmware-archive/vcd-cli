```
Usage: vcd profile extension [OPTIONS] COMMAND [ARGS]...

  Manage vcd-cli extensions.

      Description
          Manages commands added to vcd-cli.
  
          New commands can be added to vcd-cli as Python modules. The module
          containing the commands implementation needs to be present in the
          Python path.
  
      Examples
          vcd profile extension list
              List the extension modules currently registered with vcd-cli.
  
          vcd profile extension add container_service_extension.client.cse
              Add to vcd-cli the commands to work with CSE, located in the
              specified Python module.
  
          vcd profile extension delete container_service_extension.client.cse
              Removes the CSE commands from vcd-cli.
  
      Files
          ~/.vcd-cli/profiles.yaml (macOS and Linux)
          %userprofile%/.vcd-cli/profiles.yaml (Windows)
              The extension modules are registered in the profiles file.



Options:
  -h, --help  Show this message and exit.

Commands:
  add     add a vcd-cli extension
  delete  delete a vcd-cli extension
  list    list vcd-cli extensions

```
