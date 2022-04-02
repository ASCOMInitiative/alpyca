#
# PyTest Unit tests for Device superclass
# For simplicity this uses the SafetyMonitor device. 
# Connected is tested, then the common properties are read,
# Rather than test for exact strings, this test just makes
# certain that no errors occur when reading them.
#
import pytest
import simconf

from alpaca.device import Device

def test_device():
    d = Device(f"{simconf.addr()}", "SafetyMonitor", 0, "http")
    d.Connected = True
    print("Checking common static properties:")
    print(f"  Description:      {d.Description}")
    print(f"  DriverInfo:       {d.DriverInfo}")
    print(f"  DriverVersion:    {d.DriverVersion}")
    print(f"  InterfaceVersion: {d.InterfaceVersion}")
    print(f"  Name:             {d.Name}")
    print(f"  SupportedActions: {d.SupportedActions}")
    d.Connected = False

