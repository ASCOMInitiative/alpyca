# PyTest Unit tests for IDomeV2
import pytest
import conftest
import time

from alpaca.dome import Dome
from alpaca.dome import ShutterState
dev_name = "Dome"

def test_props(device, settings, disconn):
    d = device
    s = settings
    print("Test properties:")
    assert d.CanFindHome == settings["CanFindHome"]
    assert d.CanPark == settings["CanPark"]
    assert d.CanSetAltitude == settings["CanSetAltitude"]
    assert d.CanSetAzimuth == settings["CanSetAzimuth"]
    assert d.CanSetPark == settings["CanSetPark"]
    assert d.CanSetShutter == settings["CanSetShutter"]
    assert d.CanSlave == False      # Not in settings, this dome simulator cannot ever slave
    assert d.Slaved == False
    assert d.CanSyncAzimuth == settings["CanSyncAzimuth"]

def test_shutter(device, disconn):
    d = device
    print("Test shutter motion:")
    assert d.CanSetShutter
    assert d.ShutterStatus != ShutterState.shutterError
    if d.ShutterStatus != ShutterState.shutterClosed:
        print("  Closing the shutter")
        d.CloseShutter()
        while d.ShutterStatus != ShutterState.shutterClosed:
            time.sleep(0.5)
            print('.', end = '')
        print('.')
        assert d.ShutterStatus == ShutterState.shutterClosed
    print("  Opening the shutter")
    d.OpenShutter()
    while d.ShutterStatus != ShutterState.shutterOpen:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    assert d.ShutterStatus == ShutterState.shutterOpen
    print("  Closing the shutter")
    d.CloseShutter()
    while d.ShutterStatus != ShutterState.shutterClosed:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    assert d.ShutterStatus == ShutterState.shutterClosed

def test_altaz(device, disconn):
    d = device
    print("Test alt/az motion:")
    assert d.CanSetAzimuth
    assert d.CanSetAltitude
    print("  Start rotate to az 90")
    d.SlewToAzimuth(90)
    print("  Start slew to alt 60")
    d.SlewToAltitude(60)
    print('  ', end = '')
    while d.Slewing:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    assert d.Azimuth == 90
    assert d.Altitude == 60
    print("  Sync to az 130...")
    d.SyncToAzimuth(130)
    assert d.Azimuth == 130
    print(f"  OK, start rotate az {d.Azimuth} back to az 90")
    print('  ', end = '')
    d.SlewToAzimuth(90)
    while d.Slewing:
        time.sleep(0.5)
        print('.', end = '')
    assert d.Azimuth == 90
    print(f'. OK, azimuth is {d.Azimuth}')


def test_park(device, disconn):
    d = device
    print("Test parking (check can-flags):")
    assert d.CanPark
    assert d.CanSetPark
    assert d.CanSetAzimuth
    assert d.CanSyncAzimuth
    print("  Start slew to az 27")
    d.SlewToAzimuth(27)
    print('  ', end = '')
    while d.Slewing:
        time.sleep(0.5)
        print('.', end = '')
    print(f'. Dome az is {d.Azimuth}')
    assert d.Azimuth == 27
    print("  Set park position here at az 27")
    d.SetPark()
    print("  Start slew to az 120")
    print('  ', end = '')
    d.SlewToAzimuth(120)
    while d.Slewing:
        time.sleep(0.5)
        print('.', end = '')
    print(f'. Dome az is {d.Azimuth}')
    assert d.Azimuth == 120
    print("  Start async Park the dome")
    d.Park()
    print('  ', end = '')
    while not d.AtPark:
        time.sleep(0.5)
        print('.', end = '')
    print(f'. AtPark is True, Dome az is {d.Azimuth}')
    assert d.Azimuth == 27
    print("  Unpark, start slew to az 120")
    print('  ', end = '')
    d.SlewToAzimuth(120)
    while d.Slewing:
        time.sleep(0.5)
        print('.', end = '')
    print(f'. Dome az is {d.Azimuth}')
    assert d.Azimuth == 120

def test_home(device, disconn):
    d = device
    print("Test homing (check can-flag):")
    assert d.CanFindHome
    print("  Start slew to az 90")
    print('  ', end = '')
    d.SlewToAzimuth(90)
    while d.Slewing:
        time.sleep(0.5)
        print('.', end = '')
    print(f'. Dome az is {d.Azimuth}')
    assert d.Azimuth == 90
    print('  Start FindHome')
    print('  ', end = '')
    d.FindHome()
    while not d.AtHome:
        time.sleep(0.5)
        print('.', end = '')
    print(f'. OK, AtHome is true')

