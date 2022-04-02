# PyTest Unit tests for IFocuserV3
import pytest
import conftest
import time

from alpaca.focuser import Focuser
dev_name = "Focuser"

def test_props(device, settings, disconn):
    d = device
    s = settings
    print("Test Focuser properties")
    assert d.Absolute == s["Absolute"]
    assert d.MaxIncrement == s["MaxIncrement"]
    assert d.MaxStep == s["MaxStep"]
    assert d.StepSize == s["StepSize"]
    assert d.TempCompAvailable == s["TempCompAvailable"]
    assert d.TempComp == s["TempComp"]
    print(f"Temp is variable currently {d.Temperature}")

def test_motion(device, disconn):
    d = device
    print("Test Focuser motion and Halt")
    assert d.Absolute               # Test is for Absolute mode
    newpos = int(d.MaxStep / 2)
    print(f"Test: Absolute mode - Start Move from {d.Position} to {newpos}")
    d.Move(newpos)
    while(d.IsMoving):
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    assert d.Position == newpos
    newpos = d.Position + 2500      # 5 sec for OmniSim (typ.)
    print(f"Test: Start Move from {d.Position} to {newpos}")
    d.Move(newpos)
    time.sleep(2)
    d.Halt()
    print(f"Test: Halted at {d.Position}")



