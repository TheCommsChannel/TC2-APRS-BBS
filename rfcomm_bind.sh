#!/bin/bash

# Read the MAC address and group from bt_device_info.txt
info_file="bt_device_info.txt"

if [[ ! -f "$info_file" ]]; then
  echo "Error: $info_file not found. Ensure the bt_pair.exp script has been run successfully."
  exit 1
fi

# Extract the MAC address and group
read -r mac_address device_group < "$info_file"

if [[ -z "$mac_address" || -z "$device_group" ]]; then
  echo "Error: Missing MAC address or group information in $info_file."
  exit 1
fi

# Determine the rfcomm bind command based on the group
case "$device_group" in
  GROUP_ONE)
    group_id=1
    ;;
  GROUP_TWO)
    group_id=2
    ;;
  *)
    echo "Error: Unknown device group: $device_group"
    exit 1
    ;;
esac

# Bind to serial port
sudo rfcomm bind /dev/rfcomm0 "$mac_address" "$group_id"

if [[ $? -eq 0 ]]; then
  echo "Successfully bound /dev/rfcomm0 to $mac_address with group ID $group_id."
else
  echo "Failed to bind rfcomm device."
fi
