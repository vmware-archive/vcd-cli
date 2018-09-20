#!/usr/bin/env bash

set -e

VCD="C:\Users\nvladimirovi\AppData\Roaming\Python\Python36\Scripts\vcd.exe"
VCD_UI_EXT_ABS_PATH=D:/test-py-cli/ui_plugin
VCD_HOST=bos1-vcd-sp-static-198-58.eng.vmware.com
VCD_ORG=System
VCD_USER=administrator
VCD_PASSWORD='********'

# $VCD login $VCD_HOST $VCD_ORG $VCD_USER --password $VCD_PASSWORD

$VCD version

echo 'This should deploy ui extension'
$VCD uiext deploy --path $VCD_UI_EXT_ABS_PATH  -p -pr
echo 'This should list all ui extensions'
$VCD uiext list
echo 'This should delete ui extension by user choice'
$VCD uiext delete
