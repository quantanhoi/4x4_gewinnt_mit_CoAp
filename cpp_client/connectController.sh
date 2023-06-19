#!/bin/bash
set -x

# Set MAC address
MAC="E8:47:3A:02:3F:27" #Simon Controller black
#MAC="E8:47:3A:01:EE:E3"  #white
#MAC="E8:47:3A:02:A3:F0" #black

{
  #Check if Controller is already connected
  echo "info $MAC"
  sleep 2  # Allow some time for fetching info
} | bluetoothctl > /tmp/bt_info

if grep -q "Connected: yes" /tmp/bt_info; then
    echo "Device is already connected."
else
    {
      echo "remove $MAC"
      echo "agent on"
      sleep 5  # Give Bluetooth some time to register the agent and scan devices
      echo "scan on"
      sleep 15 # sicher is sicher
      echo "connect $MAC"
      sleep 5   # Allow some time for connection
      echo "quit"
    } | bluetoothctl
fi

# Clean up temp file
rm /tmp/bt_info


