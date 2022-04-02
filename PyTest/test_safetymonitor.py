# PyTest Unit tests for SafetyMonitor
import sys
import pytest
import simconf
import conftest

from alpaca.safetymonitor import SafetyMonitor
conftest.setname("SafetyMonitor")

def test_Safe(device, settings, disconn):
    assert device.IsSafe == settings['SafetyMonitor']   # This is the setting not the class (same name, typ)

def test_Boo(device, settings, disconn):
    assert device.IsSafe == settings['SafetyMonitor']
