# PyTest Unit tests for ISwitchV2
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
    print("Test Switch interface. OmniSim settings must be Reset.")
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
    print(f"  Toggle on/off and check")
    d.SetSwitchValue(0, 0)
    assert d.GetSwitchValue(0) == 0
    d.SetSwitchValue(0, 1)
    assert d.GetSwitchValue(0) == 1
    d.SetSwitchValue(0, 0)
    assert d.GetSwitchValue(0) == 0
    print(f"  Test variable for switch 3 {d.GetSwitchName(3)} '{d.GetSwitchDescription(3)}'")
    assert d.MinSwitchValue(3) == 0
    assert d.MaxSwitchValue(3) == 255
    assert d.SwitchStep(0) == 1
    print(f"  Looks like variable {d.MinSwitchValue(3)}-{d.MaxSwitchValue(3)} step {d.SwitchStep(3)}")
    print(f"  Switch between 0 and 157 and check")
    d.SetSwitchValue(3, 0)
    assert d.GetSwitchValue(3) == 0
    d.SetSwitchValue(3, 157)
    assert d.GetSwitchValue(3) == 157
    d.SetSwitchValue(3, 0)
    assert d.GetSwitchValue(3) == 0

