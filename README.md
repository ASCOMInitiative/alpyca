# alpyca 3.1.0 (Discovery update)

## Python 3.9+ API library for all [ASCOM Alpaca](https://ascom-standards.org/Developer/Alpaca.htm) universal interfaces

<img align="right" width="210" height="166" hspace="20" vspace="20" src="https://ascom-standards.org/alpyca/readme-assets/AlpacaLogo210.png">

Produced by the [ASCOM Initiative](https://ascom-standards.org/), and derived from Ethan Chappel's
Alpyca 1.0.0. Ethan kindly released the name **Alpyca** to the ASCOM Initiative, hence this expanded
package started life as Version 2.0. With 3.0.0 it has been expanded to support the additions in
ASCOM Platform 7. **NOTE** This package runs on Linux, MacOS, and Windows. It has no depencence on the
Windows ASCOM PLatform. Alpaca does not depend on Windows.

## Requirements

This package runs under Python 3.9 or later. It is compatible with most Linux distros, Windows , and MacOS.
Dependencies are minimal: [requests](https://pypi.org/project/requests/),
[netifaces](https://pypi.org/project/netifaces/),
[typing-extensions](https://pypi.org/project/typing-extensions/),
[python-dateutil](https://pypi.org/project/python-dateutil/), and
[enum-tools](https://pypi.org/project/enum-tools/).

## Installation

The package installs from [PyPi](https://pypi.org/) as

```sh
pip install alpyca
```

## Current Status & Documentation

This version 3.1.0. This release changes discovey to use ``ifaddr`` instead
of netifaces.

The documentation is extensive and available online as **[Alpyca: API Library
for Alpaca](https://ascom-standards.org/alpyca/)** as well as a **[PDF Document
here](https://ascom-standards.org/alpyca/alpyca.pdf)**. Each element of the
package references the relevant documentation in the **[ASCOM Master Interfaces
Document](https://ascom-standards.org/newdocs/)** See
**[CHANGES.rst](https://github.com/ASCOMInitiative/alpyca/blob/master/CHANGES.rst)**
(on GitHub) for change log.

## Feedback and Discussion

Feedback can be given on the
[ASCOM Driver and Application Development Support Forum](https://ascomtalk.groups.io/g/Developer).
Please note that the protocols are universal and strictly curated. This library is an
_implementation_ of the protocols, not the protocols themselves. For background please visit
[About Alpaca and ASCOM](https://ascom-standards.org/About/Index.htm), as well as the
[ASCOM Interface Principle](https://ascom-standards.org/Standards/InterfacePrinciple.htm),
[The Standards Process](https://ascom-standards.org/Standards/StandardsProcess.htm), and
the [General Requirements](https://ascom-standards.org/Standards/Requirements.htm).

## Example

This requires the _cross-platform_ ASCOM Omni Simulators which will give you
fully functional simulators for _all_ Alpaca devices, as well as a _live_
OpenAPI/Swagger interface to the Alpaca RESTful endpoints (_see the details
below_). If you are on a Windows system, the Omni Simulators are included with
the [ASCOM Platform 7](https://ascom-standards.org/). If you are on Linux or
MacOS, you can get the _cross-platform_ OmniSimulators from GitHub at the
**[Omni Simulators
Repo](https://github.com/ASCOMInitiative/ASCOM.Alpaca.Simulators/releases)**.

This example will
use the Telescope simulator. Assuming you are running the Omni Simulator on your local host
at its default port of 32323, its address is then <code>localhost:32323</code>. Here is a sample
program using Alpaca:

**REQUIRES [LATEST OMNI SIM](https://github.com/ASCOMInitiative/ASCOM.Alpaca.Simulators/releases) WITH PLATFORM 7 CONNECTION SEMANTICS**:

```python
    import time
    from alpaca.telescope import *      # Multiple Classes including Enumerations
    from alpaca.exceptions import *     # Or just the exceptions you want to catch

    T = Telescope('localhost:32323', 0) # Local Omni Simulator
    T.Connect()                         # New async connect
    while T.Connecting
        time.sleep(1)
    print(f'Connected to {T.Name}')
    print(T.Description)
    T.Tracking = True               # Needed for slewing (see below)
    try:
        print('Starting slew...')
        T.SlewToCoordinatesAsync(T.SiderealTime + 2, 50)    # 2 hrs east of meridian
        while(T.Slewing):
            time.sleep(5)               # What do a few seconds matter?
        print('... slew completed successfully.')
        print(f'RA={T.RightAscension} DE={T.Declination}')
        print('Turning off tracking then attempting to slew...')
        T.Tracking = False
        T.SlewToCoordinatesAsync(T.SiderealTime + 2, 55)    # 5 deg slew N
        # This will fail for tracking being off
        print("... you won't get here!")
    except Exception as e:                      # Should catch specific InvalidOperationException
        print(f'Caught {type(e).__name__}')
        print(f'  Slew failed: {e.message}')    # Using exception named properties
    finally:                            # Assure that you disconnect
        print("Disconnecting...")
        T.Disconnect()
```

### Results

```tt
    Connected to Alpaca Telescope Sim
    Software Telescope Simulator for ASCOM
    Starting slew...
    ... slew completed successfully.
    RA=10.939969572854931 DE=50
    Turning off tracking then attempting to slew...
    Caught InvalidOperationException
      Slew failed: SlewToCoordinatesAsync is not allowed when tracking is False
    Disconnecting...
    done
```

See how easliy  exceptions are handled? The error message came from the OmniSim.

## Alpaca Omni Simulators

The ASCOM Alpaca Simulators are included in [ASCOM Platform
7](https://ascom-standards.org/) or if you are on Linux or MacOS, they are
[available via GitHub
here](https://github.com/ASCOMInitiative/ASCOM.Alpaca.Simulators). Scroll down
to the Assets section and pick the package for your OS and CPU type.

```sh
./ascom-alpaca.simulators
```

(or the equivalent on Windows or MacOS). You may need to open a web browser to
`http://localhost:32323` if that option is off in the server settings. This is
the primary user interface to the simulator server and simulated devices. Once
you get this running you are ready to try the sample above.

![Initial OmniSim Display](https://ascom-standards.org/alpyca/readme-assets/InitialBrowserAnnotated.png)

## ASCOM Remote

Any current ASCOM COM device that is hosted on a Windows system can have an Alpaca interface added via the
**[ASCOM Remote Windows app](https://github.com/ASCOMInitiative/ASCOMRemote/releases/latest)**. This app allows you to
expose any of your Windows-hosted astronomy devices to the Alpaca world, making them reachable from programs
using alpyca.

## Wireshark

If you are interested in monitoring the HTTP/REST traffic that alpyca creates and exchanges with the
Alpaca devices, you can install the [Wireshark network protocol analyzer](https://www.wireshark.org/).
One thing that trips people up is making the installation so that Wireshark has access to all of the
network insterfaces without needing root privs (linux) or running "As Administrator" on Windows. Pay close
attention the installation steps on this. On WIndows the capture driver installation will require elevation,
as it is a privileged module. For example installing on Linux (e.g Debian/Raspberry Pi) you'll see this,
and **be sure to answer Yes**.

![Wireshark Privileges](https://ascom-standards.org/alpyca/readme-assets/WireSharkPrivs.png)

To watch Alpaca traffic, set this simple display filter <code>http and tcp.port == 32323</code>
(with <code>32323</code> being the port of the OmniSim, see above). You'll get a nice analysis
of the Alpaca traffic like this

![Wireshark Privileges](https://ascom-standards.org/alpyca/readme-assets/Wireshark1.png)
