# PyTest Unit tests for ISafetyMonitor
import pytest
import conftest

from alpaca.safetymonitor import SafetyMonitor
dev_name = "SafetyMonitor"  # Read by fixtures

def test_Safe(device, settings, disconn):
    assert device.IsSafe == settings['SafetyMonitor']   # This is the setting not the class (same name, typ)
