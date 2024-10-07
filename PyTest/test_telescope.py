# PyTest Unit tests for ITelescopeV3
import pytest
import conftest
import random
import time

from alpaca.telescope import *          # Sorry Python purists (typ.)
from alpaca.exceptions import *

dev_name = "Telescope"                  # Device-independent fixtures use this via introspection

#
# Grab the camera settings for the pytest.mark.skipif() decisions
#
c_sets = conftest.get_settings('Telescope')

def test_props(device, settings, disconn):
    d = device
    s = settings
    print("Test properties:")
    assert d.AlignmentMode.value == s['AlignMode']
    assert d.ApertureArea == s['ApertureArea']
    assert d.ApertureDiameter == s['Aperture']
    assert d.CanFindHome == s['CanFindHome']
    assert d.CanPark == s['CanPark']
    assert d.CanPulseGuide == s['CanPulseGuide']
    assert d.CanSetDeclinationRate == s['CanSetEquRates']
    assert d.CanSetGuideRates == s['CanSetGuideRates']
    assert d.CanSetPark == s['CanSetPark']
#    assert d.CanSetPierSide == s['CanSetPointingState']    #BUGBUG d.CanSetPierSide stuck on False
    assert d.CanSetRightAscensionRate == s['CanSetEquRates']
    assert d.CanSetTracking == s['CanSetTracking']
    assert d.CanSlew == s['CanSlew']
    assert d.CanSlewAltAz == s['CanSlewAltAz']
    assert d.CanSlewAltAzAsync == s['CanSlewAltAzAsync']
    assert d.CanSlewAsync == s['CanSlewAsync']
    assert d.CanSync == s['CanSync']
    assert d.CanSyncAltAz == s['CanSyncAltAz']
    assert d.CanUnpark == s['CanUnpark']
    assert d.DoesRefraction == s['Refraction']
    assert d.EquatorialSystem.value == s['EquatorialSystem']
    assert d.SiteElevation == s['Elevation']
    assert d.SiteLatitude == s['Latitude']
    assert d.SiteLongitude == s['Longitude']
    d.SlewSettleTime = 5
    # assert d.SlewSettleTime == 5      # BUGBUG 0.1.2 OmniSim stuck at settle time 0
    d.SlewSettleTime = 0
    assert d.SlewSettleTime == 0
    print("  Tracking rates from OmniSim are simple Python Dict [0, 3, 1, 2]")
    assert d.TrackingRates == [0, 3, 1, 2]
    print(f'  Testing UTC Date: {d.UTCDate}')

def test_eq_slewing(device, settings, disconn):
    d = device
    s = settings
    assert d.AlignmentMode == AlignmentModes.algGermanPolar, "OmniSim must be set for German Polar AlignmentMode"
    assert d.CanSlew, "OmniSim must be anabled for Equatorial Slewing"
    assert d.CanSlewAsync, "OmniSim must be enabled for Equatorial Asynchronous"
    print("Test equatorial slewing (both flavors):")
    lst = d.SiderealTime
    print(f"  LST={d.SiderealTime:.3f}")
    tgtRA = lst + 2    # Two hours east
    if tgtRA >= 24.0:
        tgtRA -= 24
    d.TargetRightAscension = tgtRA
    if d.SiteLatitude > 0:
        tgtDec = 45
    else:
        tgtDec = -45
    d.TargetDeclination = tgtDec
    if d.AtPark:
        d.Unpark()
    d.Tracking = True
    print(f"  SlewToTargetAsync() RA={d.TargetRightAscension:.3f} DE={d.TargetDeclination:.3f}")
    d.SlewToTargetAsync()
    assert d.Slewing
    while d.Slewing:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    print(f"  New pos RA={d.RightAscension:.3f} DE={d.Declination:.3f}, check PierSide West")
    assert d.SideOfPier == PierSide.pierWest
    tgtRA = lst - 2
    if tgtRA < 0:
        tgtRA += 24
    if d.SiteLatitude > 0:
        tgtDec = 40
    else:
        tgtDec = -40
    print(f"  SlewToCoordinatesAsync({tgtRA:.3f} DE={tgtDec:.3f})")
    d.SlewToCoordinatesAsync(tgtRA, tgtDec)
    assert d.Slewing
    assert d.TargetRightAscension == tgtRA
    assert d.TargetDeclination == tgtDec
    while d.Slewing:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    print(f"  New pos RA={d.RightAscension:.3f} DE={d.Declination:.3f}, check PierSide East")
    assert d.SideOfPier == PierSide.pierEast
    print(f"  Assure synchronous slews are not supported")
    with pytest.raises(NotImplementedException):
        d.SlewToTarget()
    with pytest.raises(NotImplementedException):
        d.SlewToCoordinates(0, 0)


def test_aa_slewing(device, settings, disconn):
    d = device
    s = settings
    print("Test alt/Az slewing:")
    assert d.CanSlewAltAz, "OmniSim must be anabled for Alt/Az Slewing"
    assert d.CanSlewAltAzAsync, "OmniSim must be enabled for Alt/Az Asynchronous"
    d.Tracking = False
    print(f"  Tracking off, SlewToAltAzAsync(120, 60)")
    d.SlewToAltAzAsync(120, 60)
    while d.Slewing:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    print(f"  New pos Alt={d.Altitude:.3f} Azm={d.Azimuth:.3f}")
    print(f"  SlewToAltAzAsync(45, 20)")
    d.SlewToAltAzAsync(45, 20)
    while d.Slewing:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    print(f"  New pos Alt={d.Altitude:.3f} Azm={d.Azimuth:.3f}")

def test_park_home(device, settings, disconn):
    d = device
    s = settings
    print("Test parking and homing:")
    assert d.CanPark, "OmniSim must have CanPark enabled"
    assert d.CanUnpark, "OmniSim must have CanUnpark enabled"
    d.Unpark()
    d.Tracking = False
    tgtAz = random.uniform(10, 240)
    tgtAlt = random.uniform(0, 10)
    d.SlewToAltAzAsync(tgtAz, tgtAlt)
    print("  Slew to random alt-az")
    while d.Slewing:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    print(f"  SetPark() at pos Alt={d.Altitude:.3f} Azm={d.Azimuth:.3f}")
    d.SetPark()
    assert d.AtPark == False
    tg2Az = random.uniform(240, 300)
    tg2Alt = random.uniform(20, 40)
    d.SlewToAltAzAsync(tg2Az, tg2Alt)
    print("  Slew to random alt-az")
    while d.Slewing:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    print(f"  Now away from park at pos Alt={d.Altitude:.3f} Azm={d.Azimuth:.3f}")
    print("  Park now")
    d.Park()
    while not d.AtPark:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    print(f"  Parking complete at Alt={d.Altitude:.3f} Azm={d.Azimuth:.3f}")
    ea = abs(d.Azimuth - tgtAz)
    if ea > 180:
        ea = 360 - ea
    assert ea < 0.1
    assert abs(d.Altitude - tgtAlt) < 0.1
    print("  Unpark then find home")
    d.Unpark()
    tgtAz = s['HomeAzimuth']
    tgtAlt = s['HomeAltitude']
    print(f"  Home position is Alt={tgtAlt:.3f} Azm={tgtAz:.3f}, FindHome()")
    d.FindHome()
    while not d.AtHome:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    print(f"  FindHome complete at Alt={d.Altitude:.3f} Azm={d.Azimuth:.3f}")
    ea = abs(d.Azimuth - tgtAz)
    if ea > 180:
        ea = 360 - ea
    assert ea < 0.1
    assert abs(d.Altitude - tgtAlt) < 0.1

def test_moveaxis(device, settings, disconn):
    d = device
    s = settings
    print("Test MoveAxis:")
    assert d.CanMoveAxis(TelescopeAxes.axisPrimary), "OmniSim must have Axes for move set to > 0"
    r = d.AxisRates(TelescopeAxes.axisPrimary)[1]   # Hardwired in OmniSim
    assert r.Maximum == 20
    assert r.Minimum == 10
    print("  Got valid AxisRates info")
    ra1 = d.RightAscension
    d.Tracking = False
    print(f"  Move for 0.5 sec at the minimum rate in the second pair of rates ({r.Minimum})")
    d.MoveAxis(TelescopeAxes.axisPrimary, r.Minimum)
    time.sleep(0.5)
    d.MoveAxis(TelescopeAxes.axisPrimary, 0)
    print("  Check to see that it moved in RA")
    assert ra1 != d.RightAscension

def test_tracking_offsets(device, settings, disconn):
    d = device
    s = settings
    print("Test Tracking offsets (just set and clear them):")
    assert d.CanSetRightAscensionRate, "OmniSim RA / Dec rates must be enabled"
    assert d.CanSetDeclinationRate
    d.Tracking = True
    d.RightAscensionRate = 0.01
    d.DeclinationRate = 0.02
    assert d.RightAscensionRate == 0.01
    assert d.DeclinationRate == 0.02
    d.RightAscensionRate = 0
    d.DeclinationRate = 0
    assert d.RightAscensionRate == 0
    assert d.DeclinationRate == 0

def test_pulse_guiding(device, settings, disconn):
    d = device
    s = settings
    print("Test Tracking offsets (just set and clear them):")
    assert d.CanPulseGuide, "OmniSim must have Pulse Guide enabled"
    assert d.CanSetGuideRates, "OmniSim must have Guide Rates enabled"
    print("  Set and check some guide rates")
    d.GuideRateRightAscension = 0.001
    #assert d.GuideRateRightAscension == 0.001  #BUGBUG? Stuck
    d.GuideRateDeclnation = 0.002
    #assert d.GuideRateDeclination == 0.002     #BUGBUG? Stuck
    print("  Do a PulseGuide North and check that it ends in prescribed time")
    d.PulseGuide(GuideDirections.guideNorth, 500)
    assert d.IsPulseGuiding
    time.sleep(2.5)
    assert d.IsPulseGuiding == False

