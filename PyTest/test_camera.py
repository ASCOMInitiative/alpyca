# PyTest Unit tests for ICameraV3
import pytest
import conftest
import time

from alpaca.camera import Camera
from alpaca.camera import CameraStates
from alpaca.camera import SensorTypes
from alpaca.exceptions import *

dev_name = "Camera"

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
    assert d.SensorType == s['SensorType']

def test_notimpl(device, settings, disconn):
    d = device
    s = settings
    print("Test unimplemented by looping through sim:")

    with pytest.raises(NotImplementedException, match='.*BayerOffsetX.*'):
        v = d.BayerOffsetX
    with pytest.raises(NotImplementedException, match='.*BayerOffsetY.*'):
        v = d.BayerOffsetY
    with pytest.raises(NotImplementedException, match='.*GainMax.*'):
        v = d.GainMax
    with pytest.raises(NotImplementedException, match='.*GainMax.*'):       # Sim 0.1.1) returns error for GainMax
        v = d.GainMin
    with pytest.raises(NotImplementedException, match='.*Gains.*'):
        v = d.Gains
    with pytest.raises(NotImplementedException, match='.*Gain[^s].*'):      # Assure exactly "Gain"
        v = d.Gain
    with pytest.raises(NotImplementedException, match='.*OffsetMax.*'):
        v = d.OffsetMax
    with pytest.raises(NotImplementedException, match='.*OffsetMax.*'):     # Sim 0.1.1) returns error for OffsetMax
        v = d.OffsetMin
    with pytest.raises(NotImplementedException, match='.*Offsets.*'):
        v = d.Offsets
    with pytest.raises(NotImplementedException, match='.*Offset[^s].*'):    # Assure exactly "Offset"
        v = d.Offset

def test_image_capture(device, settings, disconn):
    d = device
    s = settings
    print("Test: Camera image settings read/write:")
    assert d.MaxBinX >= 4, "Camera must support X binning >= 2"
    assert d.MaxBinY >= 4, "Camera must support Y binning >= 2"
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
    d.StartExposure(10.0, True)
    while not d.ImageReady:
        time.sleep(0.5)
        print(f'  {d.PercentCompleted}% complete')
    print('  finished')
