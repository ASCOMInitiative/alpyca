# PyTest Unit tests for FilterWheelV2
import pytest
import conftest
import time

from alpaca.filterwheel import FilterWheel
dev_name = "FilterWheel"

def test_props(device, settings, disconn):
    d = device
    s = settings
    print("Test FilterWheel properties: Names and Offsets must be enabled")
    assert settings["ImplementsNames"]
    assert settings["ImplementsOffsets"]
    for i in range(0, settings['Slots']):
        assert d.Names[i] == settings[f'FilterNames {i}']
        assert d.FocusOffsets[i] == settings[f'FocusOffsets {i}']

def test_motion(device, settings, disconn):
    d = device
    s = settings
    assert settings['Slots'] > 4, "This test requires at least 4 filters"
    print("Test FilterWheel motion:")
    if d.Position != 0:
        print(f"  Return from slot {d.Position} to 0")
        d.Position = 0
        while(d.Position ==  -1):
            time.sleep(0.5)
            print('.', end = '')
        print('.')
        assert d.Position == 0
    newpos = settings['Slots'] - 2
    print(f"  Move from slot {d.Position} to {newpos}")
    d.Position = newpos
    while(d.Position ==  -1):
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    assert d.Position == newpos