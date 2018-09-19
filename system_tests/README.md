# vcd-cli System Tests

## Running Tests

This directory contains system tests that exercise vcd-cli API
functions on any operating system. You can run tests individually
as follows.

1. Fill in required values in `base_config.yaml`.  
2. Execute the test as a Python unit test, e.g.: 
```
python3 -m unittest org_tests.py
```

To run system tests in a build, follow the steps below.

1. Copy `vcd_connection.sample` to `vcd_connection` and fill in 
connection data.
2. Export `VCD_CONNECTION`, e.g., `export VDC_CONNECTION=$PWD/vcd_connection`
3. Execute the script as follows: `./run_system_tests.sh`

This will run a default list of tests.  You can specify different tests 
by listing the file names on the command line, e.g.,
`./run_system_tests.sh my_test.py`.

## Writing New Tests

System tests for vcd-cli follow the same conventions as 
[pyvcloud](https://github.com/vmware/pyvcloud).  Please refer to the pyvcloud 
[system_tests/README.md file](https://github.com/vmware/pyvcloud/blob/master/system_tests/README.md)
for more information. 

vcd-cli tests use the Click CliRunner() class, which issues mock calls 
against CLI command functions.  Have a look at the tests in this directory 
as well as [Testing Click Applications](http://click.pocoo.org/5/testing/) 
for a full description of how to test Click applications efficiently. 
