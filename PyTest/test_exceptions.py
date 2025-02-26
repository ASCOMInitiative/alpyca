import pytest
import random, string

from alpaca.exceptions import *

#
# This tests not only that the error codes are per the spec, but also
# that the Exception subclasses have the correct Pythonic number
# (args[0]) and message (args[1]) attributes, but also our special
# convenience number and message properties.
#
# 25-Feb-25 (rbd) For Alpyca 3.1.0
#

def test_exceptions():
    # https://stackoverflow.com/questions/2030053/how-to-generate-random-strings-in-python
    letters = string.ascii_lowercase

    def t(x, n: int, sn: bool):
        m = ''.join(random.choice(letters) for i in range(12))  # 12 random characters
        with pytest.raises(x) as exinfo:
            if(sn):
                raise x(message=m, number=n)
            else:
                raise x(message=m)
        assert str(exinfo.typename) == x.__name__
        assert exinfo.value.number == n                 # Test user-friendly named properties
        assert str(exinfo.value.message) == m
        assert exinfo.value.args[0] == n                # Test Pythonic exception arguments
        assert str(exinfo.value.args[1]) == m
        assert str(exinfo.value) == f'{m} (Error Code: {format(n, "#x")})'  # Test str() function

    # These have a hardwired number per the Alpaca API
    t(ActionNotImplementedException, 0x40C, False)
    t(InvalidOperationException, 0x40B, False)
    t(InvalidValueException, 0x401, False)
    t(NotConnectedException, 0x407, False)
    t(NotImplementedException, 0x400, False)
    t(OperationCancelledException, 0x40E, False)
    t(ParkedException, 0x408, False)
    t(SlavedException, 0x409, False)
    t(ValueNotSetException, 0x402, False)
    # These take a supplied number
    t(AlpacaRequestException, 0x4F0, True)              # HTTP Result Code
    t(DriverException, 0x54F, True)                     # Driver Error Code 0x500-0x5FF

