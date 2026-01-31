# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# conftest - Implements PyTest module for testing SafetyMonitor
#
# # Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
# -----------------------------------------------------------------------------
# Edit History:
# 30-Jan-2026   rbd     Setting name changed to IsSafeSetting
#                       Change to using the OmniSim JSON API for settings
# -----------------------------------------------------------------------------
import pytest
import conftest

from alpaca.safetymonitor import SafetyMonitor
dev_name = "SafetyMonitor"  # Read by fixtures
def test_Safe(device, disconn):
    assert device.IsSafe == conftest.get_setting(dev_name.lower(), 'issafesetting')
