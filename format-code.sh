#!/usr/bin/env bash

yapf -i vcd_cli/*.py
flake8 vcd_cli/*.py
