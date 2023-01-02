#
# PyTest Unit tests for Device superclass
# For simplicity this uses the SafetyMonitor device. 
# The strings are static and not accessible via the 
# OmniSim XML settings file. 
import pytest
import conftest

from alpaca.safetymonitor import SafetyMonitor
dev_name = "SafetyMonitor"   # Use this Alpaca device as the source (not in XML config)

def test_device(device, disconn):
    print("Checking Device superclass common static properties (using SafetyMonitor):")
    print(f"  Connected:        {device.Connected}")
    assert device.Connected
    print(f"  Description:      {device.Description}")
    assert device.Description == "ASCOM SafetyMonitor Simulator Driver"
    print(f"  DriverInfo:       {device.DriverInfo}")
    assert device.DriverInfo == ['SafetyMonitor Simulator Drivers']
    print(f"  DriverVersion:    {device.DriverVersion}")
    assert device.DriverVersion == '0.3'  # Some day not hardwired. New 0.3 OmniSim.
    print(f"  InterfaceVersion: {device.InterfaceVersion}")
    assert device.InterfaceVersion == 2
    print(f"  Name:             {device.Name}")
    assert device.Name == "Alpaca SafetyMonitor Sim"
    print(f"  SupportedActions: {device.SupportedActions}")
    assert device.SupportedActions == []

