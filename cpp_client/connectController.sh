#!/bin/bash
set -x


# grep searches for the line containing "Controller-MAC"
# grep -v "^#" excludes lines that start with '#'
# cut splits the line at the '=' character and outputs the second field

MAC=$(grep "Controller-MAC" ../config.txt | grep -v "^#" | cut -d '=' -f 2)
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


