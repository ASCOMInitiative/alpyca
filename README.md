# alpaca-client

## Python 3.6+ client interface for all [ASCOM Alpaca](https://ascom-standards.org/Developer/Alpaca.htm) universal interfaces

Inspired by [EthanChappel/Alpyca](https://github.com/EthanChappel/Alpyca). When this releases as **alpyca-client** Ethan's original **alpyca** package on PyPi will redirect to this client package.

**Progress:** Interfaces and member casing corrected, refactored to class per module, return of native types, and more. All remaining ASCOM device classes added and implemented, management interface and discovery added and implemented.

_[10-April-2022]_ Just wrapping up the PyTest unit tests. Still remining is a total review of the docstrings for input to Sphinx as well as Intellisense popup help, production of documentation, and Poetry-created PyPi package.

_[03-May-2022]_ Discovery for IPv6 on systems with multiple net interfaces and multiple addresses on interfaces. Complete review and update of the docstring/Sphinx docs and intellisense throughout. Added the module headers, now just about ready to be packaged and tested.

Much work left to be completed, and this yet to be written!
