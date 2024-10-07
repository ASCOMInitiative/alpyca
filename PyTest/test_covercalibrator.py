import pytest
import conftest
import random
import time

from alpaca.covercalibrator import *            # Sorry Python purists (typ.)

dev_name = "CoverCalibrator"

#
# Grab the covercalibrator settings for the pytest.mark.skipif() decisions
#
c_sets = conftest.get_settings('CoverCalibrator')

@pytest.mark.skipif((c_sets['Cover Initialisation State'] == 'NotPresent'), reason='Requires OmniSim Cover to be enabled')
def test_cover(device, settings, disconn):
    d = device
    s = settings
    print("Test Cover:")
    assert d.CoverState != CoverStatus.NotPresent       # Never
    if d.CoverState != CoverStatus.Closed:
        print("  Closing the cover")
        d.CloseCover()
        #while d.CoverState != CoverStatus.Closed:
        while d.CoverMoving:
            time.sleep(0.5)
            print('.', end = '')
        print('.')
        assert d.CoverState == CoverStatus.Closed
    print("  Opening the cover")
    d.OpenCover()
    #while d.CoverState != CoverStatus.Open:
    while d.CoverMoving:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    assert d.CoverState == CoverStatus.Open
    print("  Closing the Cover")
    d.CloseCover()
    #while d.CoverState != CoverStatus.Closed:
    while d.CoverMoving:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    assert d.CoverState == CoverStatus.Closed
    print("  Opening to be halted")
    d.OpenCover()
    time.sleep(1.5)
    print("  Halting")
    d.HaltCover()
    print(" CoverState should be Unknown")
    assert d.CoverState == CoverStatus.Unknown

@pytest.mark.skipif((c_sets['Calibrator Initialisation State'] == 'NotPresent'), reason='Requires OmniSim Calibrator to be enabled')
def test_calibrator(device, settings, disconn):
    d = device
    s = settings
    print("Test Calibrator:")
    assert d.MaxBrightness == s["Maximum Brightness"]
    if d.Brightness > 0:
        print("  Turning calibrator off")
        d.CalibratorOff()
        #while d.Brightness > 0:
        while d.CalibratorChanging:
            time.sleep(0.5)
            print('.', end = '')
        print('.')
        assert d.Brightness == 0
    b = random.randint(0, d.MaxBrightness)
    print(f"Turning calibrator on brightness {b}")
    d.CalibratorOn(b)
    #while d.Brightness < b:
    while d.CalibratorChanging:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    assert d.Brightness == b
    print(" Turning calibrator off")
    d.CalibratorOff()
    #while d.Brightness > 0:
    while d.CalibratorChanging:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    assert d.Brightness == 0

