# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# test_filterwheel.py - Implements PyTest module for testing FilterWheel
#
# # Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
# -----------------------------------------------------------------------------
# Edit History:
# 02-Feb-2026   rbd     Change to using the OmniSim JSON API for settings
#                       Use JSON API to assure correct configuration
# -----------------------------------------------------------------------------
import pytest
import conftest
import time

from alpaca.filterwheel import FilterWheel
dev_name = "FilterWheel"

#
# OmniSim Default is 6 filters with
#
# NOTE: As of OmniSim 0.5, the FilterNames and FocusOffsets settings
#       are not accessible through the JSON API, so this test still uses
#       the XML API access.
#
def test_props(device, settings, disconn):
    conftest.reset_dev(dev_name)
    print("Test FilterWheel properties: Enable Names and Offsets")
    conftest.set_setting(dev_name, 'ImplementsNames', True)
    conftest.set_setting(dev_name, 'ImplementsOffsets', True)
    d = device
    nslots = conftest.get_setting(dev_name, "Slots")
    for i in range(0, nslots):
        assert d.Names[i] == settings[f'FilterNames {i}']
        assert d.FocusOffsets[i] == settings[f'FocusOffsets {i}']

def test_motion(device, disconn):
    conftest.reset_dev(dev_name)
    d = device
    nslots = conftest.get_setting(dev_name, "Slots")
    assert nslots > 4, "This test requires at least 4 filters"

    print("Test FilterWheel motion:")
    if d.Position != 0:
        print(f"  Return from slot {d.Position} to 0")
        d.Position = 0
        while(d.Position ==  -1):
            time.sleep(0.5)
            print('.', end = '')
        print('.')
        assert d.Position == 0
    newpos = nslots - 2
    print(f"  Move from slot {d.Position} to {newpos}")
    d.Position = newpos
    while(d.Position ==  -1):
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    assert d.Position == newpos