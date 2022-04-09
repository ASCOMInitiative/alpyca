import conftest
import random
import time

from alpaca.rotator import Rotator
from alpaca.exceptions import *         # Sorry Python purists
dev_name = "Rotator"

#
# Grab the rotator settings for the pytest.mark.skipif() decisions 
#
c_sets = conftest.get_settings('Rotator')

def test_reversal(device, settings, disconn):
    d = device
    s = settings
    print("Test Rotator reversal properties")
    assert d.CanReverse == s['CanReverse']
    assert d.CanReverse, "CanReverse must be enabled in OmniSim"
    d.Reverse = s['Reverse']
    assert d.Reverse == s['Reverse']
    print(f'Reverse is {d.Reverse}, changing to {not d.Reverse}')
    old = d.Reverse
    d.Reverse = not d.Reverse
    assert d.Reverse !=  old
    assert d.StepSize == 1.0   # Fixed value in OmniSim (BUG Shows 0.8)

def test_offset(device, settings, disconn):
    d = device
    s = settings
    print("Test Rotator offset and sync features")
    d.Sync(d.MechanicalPosition + 10.123)
    x = abs(d.MechanicalPosition + 10.123 - d.Position)
    assert x < 0.01 or x > 359.8
    d.Sync(d.MechanicalPosition - 8.321)
    x = abs(d.MechanicalPosition - 8.321 - d.Position)
    assert x < 0.01 or x > 359.8

def test_motion(device, settings, disconn):
    d = device
    s = settings
    print("Test Rotator motion")
    print("  Move to mechanical 90")
    d.MoveMechanical(90.0)
    while d.IsMoving:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    print("  Sync to 90 (0.0 offset) for simplicity")
    d.Sync(90.0)
    assert d.MechanicalPosition == d.Position
    print("  Move relative +45, 90 to 135 ")
    d.Move(45.0)
    print("  Immediately check TargetPosition")
    assert d.TargetPosition == 135.0
    while d.IsMoving:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    print("  Move absolute to 45")
    print("  Immediately check TargetPosition")
    d.MoveAbsolute(45.0)
    assert d.TargetPosition == 45.0
    while d.IsMoving:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    print("  Move absolute to 135, halt after 2 sec.")
    d.MoveAbsolute(135)
    time.sleep(2)
    d.Halt()
    print(f"  Halted at {d.Position}")
