#!/usr/bin/env bash

set -e

VCD="path/to/vcd/exe"
VCD_UI_EXT_ABS_PATH=path/to/existing/ui/plugin
VCD_HOST=host.vmware.com
VCD_ORG=Org
VCD_USER=user
VCD_PASSWORD='********'

# $VCD login $VCD_HOST $VCD_ORG $VCD_USER --password $VCD_PASSWORD

$VCD version

echo 'This should deploy ui extension'
$VCD uiext deploy --path $VCD_UI_EXT_ABS_PATH  -p -pr
echo 'This should list all ui extensions'
$VCD uiext list
echo 'This should delete all ui extension'
$VCD uiext delete --all
