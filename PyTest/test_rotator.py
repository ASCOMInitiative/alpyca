import conftest
import random
import time

from alpaca.rotator import *                # Sorry Python purists (typ.)
from alpaca.exceptions import *

dev_name = "Rotator"

#
# Grab the covercalibrator settings for the pytest.mark.skipif() decisions 
#
c_sets = conftest.get_settings('Rotator')


