#!/usr/bin/env python3
"""Script to list ADB devices with explicit ADB path."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Set ADB path explicitly
os.environ["ADB_PATH"] = r"C:\AND\platform-tools\adb.exe"

from ntt_adb_mcp.tools.devices import list_devices, get_device_info
import json

def main():
    print("=== Listing ADB Devices ===")
    print(f"Using ADB at: {os.environ['ADB_PATH']}\n")
    
    # List all devices
    result = list_devices()
    
    if result["success"]:
        print(f"✓ Found {result['count']} device(s)\n")
        
        if result["devices"]:
            for i, device in enumerate(result["devices"], 1):
                print(f"Device {i}:")
                for key, value in device.items():
                    print(f"  {key}: {value}")
                print()
                
                # Get detailed info for each device
                print(f"  Detailed Info:")
                info_result = get_device_info(device["id"])
                if info_result["success"]:
                    for key, value in info_result["info"].items():
                        if key != "device_id":
                            print(f"    {key}: {value}")
                print()
        else:
            print("No devices found. Make sure:")
            print("  1. USB debugging is enabled on your device")
            print("  2. Device is connected via USB or network")
            print("  3. Device is authorized (check device for prompt)")
    else:
        print("✗ Error listing devices:")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
