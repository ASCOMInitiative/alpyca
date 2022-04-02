import sys
import pytest
import simconf

def setname(name):
    global n
    n = name

@pytest.fixture(scope="module")
def device():
    global d
    global n
    c = getattr(sys.modules[f"alpaca.{n.lower()}"], n)  # Creates a device class by string name :-)
    d =  c(simconf.addr(), 0)                           # Created an instance of the class
    d.Connected = True
    print(f"Setup: Connected to {n} OK")
    return d
#
# Grabs the settings for the device from the OmniSim settings data *once*.
#
@pytest.fixture(scope="module")
def settings():
    s = simconf.settings(n)
    print(f"Setup: {n} Settings retrieved")
    return s

@pytest.fixture(scope="module")
def disconn():
    global d
    yield
    d.Connected = False
    print(f"Teardown: {n} Disconnected")

