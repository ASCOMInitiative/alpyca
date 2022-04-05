import conftest
import time

from alpaca.covercalibrator import *             # Sorry Python purists (typ.)
from alpaca.exceptions import *

dev_name = "CoverCalibrator"

def test_cover(device, settings, disconn):
    d = device
    s = settings
    print("Test Cover:")
    assert d.CoverState != CoverStatus.NotPresent
    
