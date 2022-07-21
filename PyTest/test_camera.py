# PyTest Unit tests for ICameraV3
import os
import pytest
import conftest
import time

from alpaca.camera import *             # Sorry Python purists (typ.)
from alpaca.exceptions import *

dev_name = "Camera"                     # Device-independent fixtures use this via introspection

#
# Grab the camera settings for the pytest.mark.skipif() decisions 
#
c_sets = conftest.get_settings('Camera')

def test_props(device, settings, disconn):
    d = device
    s = settings
    print("Test properties:")
    assert d.CameraXSize == s['CameraXSize']
    assert d.CameraYSize == s['CameraYSize']
    assert d.CanAbortExposure == s['CanAbortExposure']
    assert d.CanAsymmetricBin == s['CanAsymmetricBin']
    assert d.CanFastReadout == s['CanFastReadout']
    assert d.CanGetCoolerPower == s['CanGetCoolerPower']
    assert d.CanPulseGuide == s['CanPulseGuide']
    assert d.CanSetCCDTemperature == s['CanSetCCDTemperature']
    assert d.ElectronsPerADU == s['ElectronsPerADU']
    assert d.ExposureMax == s['MaxExposure']
    assert d.ExposureMin == s['MinExposure']
    assert d.ExposureResolution == s['ExposureResolution']
    #assert d.FastReadout == s['FastReadout']
    assert d.FullWellCapacity == s['FullWellCapacity']
    assert d.HasShutter == s['HasShutter']
    assert d.MaxADU == s['MaxADU']
    assert d.MaxBinX == s['MaxBinX']
    assert d.MaxBinY == s['MaxBinY']
    assert d.PixelSizeX == s['PixelSizeX']
    assert d.PixelSizeY == s['PixelSizeY']
    v = s['ReadoutModes']
    assert d.ReadoutModes == v.split(',')
    assert d.SensorName == s['SensorName']
    assert d.SensorType == SensorType(s['SensorType'])

def test_cooler(device, settings, disconn):
    d = device
    s = settings
    assert s['HasCooler'], 'OmniSim Has Cooler must be ON'
    assert d.CanSetCCDTemperature, 'OmniSim Can Set CCD Temperature must be ON'
    assert d.CanGetCoolerPower, 'OmniSim Can Get Cooler Power must be ON'

@pytest.mark.skipif((c_sets['GainMode'] != 1 or c_sets['OffsetMode'] != 1), reason='Requires OmniSim Gain and Offset modes to be "Gain Names"')
def test_named_gains_offsets(device, settings, disconn):
    d = device
    s = settings
    v = s['Gains']
    assert d.Gains == v.split(','), 'OmniSim must be set to Named Gains mode'
    d.Gain = 0
    assert d.Gain == 0
    v = s['Offsets']
    assert d.Offsets == v.split(','), 'OmniSim must be set to "Named Offsets" mode'
    d.Offset = 0
    assert d.Offset == 0

@pytest.mark.skipif((c_sets['GainMode'] != 2 or c_sets['OffsetMode'] != 2), reason='Requires OmniSim Gain and Offset modes to be "Min Max"')
def test_min_max_gains_offsets(device, settings, disconn):
    d = device
    s = settings
    assert d.GainMin == s["GainMin"], 'OmniSim must be set to Max-Min Gains mode'
    assert d.GainMax == s["GainMax"]
    tg = d.GainMin + (d.GainMax - d.GainMin) // 2
    d.Gain = tg
    assert d.Gain == tg
    assert d.OffsetMin == s["OffsetMin"], 'OmniSim must be set to Max-Min Offsets mode'
    assert d.OffsetMax == s["OffsetMax"]
    tg = d.OffsetMin + (d.OffsetMax - d.OffsetMin) // 2
    d.Offset = tg
    assert d.Offset == tg

@pytest.mark.skipif((c_sets['GainMode'] != 0 or c_sets['OffsetMode'] != 0), reason='Requires OmniSim Gain and Offset modes to be "None"')
def test_disabled_gains_offsets(device, settings, disconn):
    d = device
    s = settings
    with pytest.raises(NotImplementedException, match='.*Gain[^s].*'):      # Assure exactly "Gain"
        v = d.Gain
    with pytest.raises(NotImplementedException, match='.*Offset[^s].*'):    # Assure exactly "Offset"
        v = d.Offset
    with pytest.raises(NotImplementedException, match='.*GainMax.*'):
        v = d.GainMax
    with pytest.raises(NotImplementedException, match='.*GainMax.*'):       # Sim (0.1.2) returns error for GainMax
        v = d.GainMin
    with pytest.raises(NotImplementedException, match='.*Gains.*'):
        v = d.Gains
    with pytest.raises(NotImplementedException, match='.*OffsetMax.*'):
        v = d.OffsetMax
    with pytest.raises(NotImplementedException, match='.*OffsetMax.*'):     # Sim (0.1.2) returns error for OffsetMax
        v = d.OffsetMin
    with pytest.raises(NotImplementedException, match='.*Offsets.*'):
        v = d.Offsets


@pytest.mark.skipif((c_sets['SensorType'] == 0 ), reason='Requires OmniSim SensorType to be other than Monochrome')
def test_color_bayer(device, settings, disconn):
    d = device
    s = settings
    assert d.BayerOffsetX == s['BayerOffsetX']
    assert d.BayerOffsetY == s['BayerOffsetY']

@pytest.mark.skipif((c_sets['SensorType'] != 0 ), reason='Requires OmniSim SensorType to be Monochrome')
def test_image_capture(device, settings, disconn):
    d = device
    s = settings
    print("Test: Camera image capture:")
    assert d.CameraXSize != d.CameraYSize, "Width must not be the same as height for test validity"
    assert d.MaxBinX >= 2, "Camera must support X binning >= 2"
    assert d.MaxBinY >= 2, "Camera must support Y binning >= 2"
    d.BinX = 2
    assert d.BinX == 2
    d.BinY = 2
    assert d.BinY == 2
    d.StartX = 0
    assert d.StartX == 0
    d.StartY = 0
    assert d.StartY == 0
    d.NumX = d.CameraXSize // d.BinX
    assert d.NumX == d.CameraXSize // d.BinX
    d.NumY = d.CameraYSize // d.BinY
    assert d.NumY == d.CameraYSize // d.BinY
    print(f"Test: Acquire 10 second {d.CameraXSize}x{d.CameraYSize} image:")
    print(f"  {d.CameraState}")
    d.StartExposure(10.0, True)
    while not d.ImageReady:
        time.sleep(0.5)
        print(f'  {d.CameraState}: {d.PercentCompleted}% complete')
    print(f'  finished, Duration = {d.LastExposureDuration}, Start Time = {d.LastExposureStartTime}')
    img = d.ImageArray
    assert len(img) == d.NumX
    assert len(img[0]) == d.NumY
    print(f'    array is {len(img)} wide by {len(img[0])} high, OK for {d.BinX} by {d.BinY} binning')

def test_image_stop_abort(device, settings, disconn):
    d = device
    s = settings
    print("Test: Camera image stop and abort:")
    assert d.MaxBinX >= 2, "OmniSim Camera must support X binning >= 2"
    assert d.MaxBinY >= 2, "OmniSim OmniSim Camera must support Y binning >= 2"
    assert d.CanAbortExposure, 'OmniSim Can Abort Exposure must be ON'
    assert d.CanStopExposure, 'OmniSim Can Stop Exposure must be ON'
    print('Test: Acquire 10 sec image, stop after 4 seconds')
    d.StartExposure(10.0, True)
    time.sleep(4)
    print('  stopping')
    d.StopExposure
    while not d.ImageReady:
        time.sleep(0.5)
        print(f'  {d.CameraState}: {d.PercentCompleted}% complete')
    print(f'  finished, Duration = {d.LastExposureDuration}, Start Time = {d.LastExposureStartTime}')
    print('Test: Acquire 10 sec image, abort after 4 seconds')
    d.StartExposure(10.0, True)
    time.sleep(4)
    print('  aborting')
    d.AbortExposure
    while not d.ImageReady:
        time.sleep(0.5)
        print(f'  {d.CameraState}: {d.PercentCompleted}% complete')
    print(f'  finished, Duration = {d.LastExposureDuration}, Start Time = {d.LastExposureStartTime}')
