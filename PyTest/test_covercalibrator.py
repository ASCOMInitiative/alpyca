import conftest
import random
import time

from alpaca.covercalibrator import *            # Sorry Python purists (typ.)

dev_name = "CoverCalibrator"

#
# Grab the covercalibrator settings for the pytest.mark.skipif() decisions 
#
c_sets = conftest.get_settings('Camera')

# Does not seem to be a way to detect "Not Present: in the settings
# Should be a pytest.mark.skipif() condition. 
def test_cover(device, settings, disconn):
    d = device
    s = settings
    print("Test Cover:")
    assert d.CoverState != CoverStatus.NotPresent       # Never
    if d.CoverState != CoverStatus.Closed:
        print("  Closing the cover")
        d.CloseCover()
        while d.CoverState != CoverStatus.Closed:
            time.sleep(0.5)
            print('.', end = '')
        print('.')
        assert d.CoverState == CoverStatus.Closed
    print("  Opening the cover")
    d.OpenCover()
    while d.CoverState != CoverStatus.Open:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    assert d.CoverState == CoverStatus.Open
    print("  Closing the Cover")
    d.CloseCover()
    while d.CoverState != CoverStatus.Closed:
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

def test_calibrator(device, settings, disconn):
    d = device
    s = settings
    print("Test Calibrator:")
    assert d.MaxBrightness == s["Maximum Brightness"]
    if d.Brightness > 0:
        print("  Turning calibrator off")
        d.CalibratorOff()
        while d.Brightness > 0:
            time.sleep(0.5)
            print('.', end = '')
        print('.')
    b = random.randint(0, d.MaxBrightness)
    print(f"Turning calibrator on brightness {b}")
    d.CalibratorOn(b)
    while d.Brightness < b:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    assert d.Brightness == b
    print(" Turning calibrator off")
    d.CalibratorOff()
    while d.Brightness > 0:
        time.sleep(0.5)
        print('.', end = '')
    print('.')
    assert d.Brightness == 0
   
