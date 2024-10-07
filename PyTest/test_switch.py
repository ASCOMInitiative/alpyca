# PyTest Unit tests for ISwitchV2
import time
import conftest

from alpaca.switch import Switch
dev_name = "Switch"

#
# Grab the camera settings for the pytest.mark.skipif() decisions
#
c_sets = conftest.get_settings('Switch')

def test_switch(device, settings, disconn):
    d = device
    s = settings
    assert d.InterfaceVersion >= 3, 'OmniSim must implement ISwitchV3 or later'
    assert (s['CanAsync Switch0'] and s['Duration Switch0'] == 3), 'OmniSim Switch 0 must be set for async 3 seconds'
    assert d.MaxSwitch == s['NumSwitches']
    print(f"  Switch 0 is {d.GetSwitchName(0)}, test name change")
    assert d.CanWrite(0)
    orig = d.GetSwitchName(0)
    d.SetSwitchName(0, "UnitTest0")
    assert d.GetSwitchName(0) == "UnitTest0"
    d.SetSwitchName(0, orig)
    assert d.GetSwitchName(0) == orig
    print(f"  Test simple on/off for switch 0 {d.GetSwitchName(0)} '{d.GetSwitchDescription(0)}'")
    assert d.MinSwitchValue(0) == 0
    assert d.MaxSwitchValue(0) == 1
    assert d.SwitchStep(0) == 1
    print(f"  Looks like on/off {d.MinSwitchValue(0)}-{d.MaxSwitchValue(0)} step {d.SwitchStep(0)}")

    print(f"  Synchronous toggle on/off and check")
    d.SetSwitch(0, False)
    assert not d.GetSwitch(0)
    d.SetSwitch(0, True)
    assert d.GetSwitch(0)
    d.SetSwitch(0, False)
    assert not d.GetSwitch(0)

    print(f"  Asynchronous toggle on/off and check")
    assert (s['CanAsync Switch0'] and s['Duration Switch0'] == 3), 'OmniSim Switch 0 must be set for async 3 seconds'
    assert d.CanAsync(0)
    print('  Turn switch 0 OFF')
    d.SetAsync(0, False)
    while not d.StateChangeComplete(0):
        print('.', end = '')
        time.sleep(0.5)
    print('  done')
    assert not d.GetSwitch(0)
    print('  Turn switch 0 ON')
    d.SetAsync(0, True)
    while not d.StateChangeComplete(0):
        print('.', end = '')
        time.sleep(0.5)
    print('  done')
    assert d.GetSwitch(0)
    print('  Turn switch 0 OFF')
    d.SetAsync(0, False)
    while not d.StateChangeComplete(0):
        print('.', end = '')
        time.sleep(0.5)
    print('  done')
    time.sleep(0.5)
    assert not d.GetSwitch(0)

    print(f"  Test variable for switch 3 {d.GetSwitchName(3)} '{d.GetSwitchDescription(3)}'")
    assert d.MinSwitchValue(3) == 0
    assert d.MaxSwitchValue(3) == 255
    assert d.SwitchStep(0) == 1
    print(f"  Looks like variable {d.MinSwitchValue(3)}-{d.MaxSwitchValue(3)} step {d.SwitchStep(3)}")

    print(f"  Synchronous switch between 0 and 157 and check")
    d.SetSwitchValue(3, 0)
    assert d.GetSwitchValue(3) == 0
    d.SetSwitchValue(3, 157)
    assert d.GetSwitchValue(3) == 157
    d.SetSwitchValue(3, 0)
    assert d.GetSwitchValue(3) == 0

    print(f"  Asynchronous switch between 0 and 157 and check")
    assert (s['CanAsync Switch3'] and s['Duration Switch3'] == 3), 'OmniSim Switch 3 must be set for async 3 seconds'
    assert d.CanAsync(3)
    d.SetAsyncValue(3, 0)
    while not d.StateChangeComplete(3):
        print('.', end = '')
        time.sleep(0.5)
    print('  done')
    assert d.GetSwitchValue(3) == 0
    d.SetAsyncValue(3, 157)
    while not d.StateChangeComplete(3):
        print('.', end = '')
        time.sleep(0.5)
    print('  done')
    assert d.GetSwitchValue(3) == 157
    d.SetAsyncValue(3, 0)
    while not d.StateChangeComplete(3):
        print('.', end = '')
        time.sleep(0.5)
    print('  done')
    assert d.GetSwitchValue(3) == 0
