#!/bin/bash

# List the devices
devices=$(ls /dev/serial/by-id/)

# Use grep and sed to extract the device ID from each line, then sort and remove duplicates
echo "$devices" | grep -o 'usb-Silicon_Labs_CP2105_Dual_USB_to_UART_Bridge_Controller_[^-]*' | sed 's/.*_Controller_//g' | sort | uniq
