# PyTest Unit tests for SafetyMonitor
import pytest
import simconf

from alpaca.safetymonitor import SafetyMonitor

def test_Safe():

    s = SafetyMonitor(f"{simconf.addr()}", 0)
    s.Connected = True
    settings = simconf.settings("SafetyMonitor")
    assert f"{s.IsSafe}" == settings['SafetyMonitor']   # Comparing strings, bool("False") == True!
    s.Connected = False