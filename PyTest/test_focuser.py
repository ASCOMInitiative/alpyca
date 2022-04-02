# PyTest Unit tests for Focuser
import pytest
import simconf
from alpaca.focuser import Focuser

def test_focuser():
    f = Focuser(f"{simconf.addr()}", 0)
    f.Connected = True
    print(f.Description)
    f.Connected = False