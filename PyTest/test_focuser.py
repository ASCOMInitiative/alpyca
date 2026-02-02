# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# test_focuser.py - Implements PyTest module for testing Focuser
#
# # Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
# -----------------------------------------------------------------------------
# Edit History:
# 02-Feb-2026   rbd     Change to using the OmniSim JSON API for settings
#                       Use JSON API to assure correct Dome configuration
# -----------------------------------------------------------------------------
import pytest
import conftest
import time

from alpaca.focuser import Focuser
dev_name = "Focuser"

def test_props(device, disconn):
    conftest.reset_dev(dev_name)
    d = device
    print('Test Focuser properties, Enable temp probe')
    conftest.set_setting(dev_name, 'TempProbe', True)
    print(f"Temp is variable currently {d.Temperature}")
    assert d.Absolute == conftest.get_setting(dev_name,'Absolute')
    assert d.MaxIncrement == conftest.get_setting(dev_name,'MaxIncrement')
    assert d.MaxStep == conftest.get_setting(dev_name,'MaxStep')
    assert d.StepSize == conftest.get_setting(dev_name,'StepSize')
    assert d.TempCompAvailable == conftest.get_setting(dev_name,'TempCompAvailable')
    assert d.TempComp == conftest.get_setting(dev_name,'TempComp')

def test_motion(device, disconn):
    conftest.reset_dev(dev_name)
    d = device
    print("Test Focuser motion and Halt. Set Absolute and disable Synchronous")
    conftest.set_setting(dev_name, 'Absolute', True)
    conftest.set_setting(dev_name, 'Synchronous', False)
    conftest.set_setting(dev_name, 'CanHalt', True)
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



