# AlpycaClient
Python client interface for [ASCOM Alpaca](https://ascom-standards.org/Developer/Alpaca.htm)

Derived and modernized from [Ethan/Chappel/Alpyca](https://github.com/EthanChappel/Alpyca). Interfaces and member casing corrected, and more. 

## Install
#### Using Pip
If downloading from the Python Package Index, run
```
python3 -m pip install Alpyca
```

#### From source
If you have the source code in a tar file, extract it and run
```
python3 setup.py install
```

## Documentation
All methods have docstrings accessible with Python's built-in [```help()```](https://docs.python.org/3/library/functions.html#help) function.

Alpyca's classes, methods, and parameters use the same names as ASCOM Alpaca's RESTful API. The documentation for Alpaca can be found at [https://ascom-standards.org/api/](https://ascom-standards.org/api/).

### Example
The address to move a telescope accessible at ```http://127.0.0.1:11111/api/v1/telescope/0/moveaxis``` with the request body ```{"Axis": 0, "Rate": 1.5}``` translates into this Python code:
```
# Import the Telescope class.
from alpaca import Telescope

# Initialize a Telescope object with 0 as the device number.
t = Telescope('127.0.0.1:11111', 0)

# Move the primary axis 1.5 degrees per second.
t.moveaxis(Axis=0, Rate=1.5)
```
