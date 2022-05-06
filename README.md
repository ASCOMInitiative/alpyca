# alpyca-client (0.1.0 Alpha)

## Python 3.7+ client interface for all [ASCOM Alpaca](https://ascom-standards.org/Developer/Alpaca.htm) universal interfaces

<img align="right" width="210" height="166" hspace="20" vspace="20" src="https://ascom-standards.org/alpyca/readme-assets/AlpacaLogo210.png">Produced by the [ASCOM Initiative](https://ascom-standards.org), and inspired by [Ethan Chappel's Alpyca](https://github.com/EthanChappel/Alpyca).
When this releases to production as **alpyca-client**, Ethan's original alpyca package on PyPi will redirect to this official ASCOM Alpaca package. It's intended that there will be a companion **alpyca-server** library for astronomy devices.

## Requirements

This package runs under Python 3.7 or later. It is compatible with most Linux distros, Windows , and MacOS. Dependencies are minimal: [requests](https://pypi.org/project/requests/),
[netifaces](https://pypi.org/project/netifaces/),
[typing-extensions](https://pypi.org/project/typing-extensions/),
[python-dateutil](https://pypi.org/project/python-dateutil/), and
[enum-tools](https://pypi.org/project/enum-tools/).

## Installation

The library installs from PyPi as

```sh
pip install alpyca-client
```

or if you have the source code in a tar file, extract it and run

```sh
python3 setup.py install
```

The dependencies listed above are automatically installed with alpyca-client.

## Current Status & Documentation

The library is in a developmental/alpha stage. The documentation is extensive and available
online as **[Alpaca Client Library](https://ascom-standards.org/alpyca/)** as well as a
**[PDF Document here](https://ascom-standards.org/alpyca/alpyca-client.pdf)**.

## Feedback and Discussion

Feedback can be given on the [ASCOM Driver and Application Development Support Forum](https://ascomtalk.groups.io/g/Developer).
Please note that the protocols are universal and strictly curated. This library is an
_implementation_ of the protocols, not the protocols themselves. For background please visit
[About Alpaca and ASCOM](https://ascom-standards.org/About/Index.htm), as well as the
[ASCOM Interface Principle](https://ascom-standards.org/Standards/InterfacePrinciple.htm),
[The Standards Process](https://ascom-standards.org/Standards/StandardsProcess.htm), and
the [General Requirements](https://ascom-standards.org/Standards/Requirements.htm).

## Example

First download, install and run the _cross-platform_
**[Alpaca Omni Simulator](https://github.com/DanielVanNoord/ASCOM.Alpaca.Simulators#readme)**
which will give you fully functional simulators for _all_ Alpaca devices, as well as a _live_
OpenAPI/Swagger interface to the Alpaca RESTful endpoints (_see the details below_). This example will
use the Telescope simulator. Assuming you are running the Omni Simulator on your local host
at its default port of 32323, its address is then <code>localhost:32323</code>. Here is a sample
program using alpaca-client:

```python
    import time
    from alpaca.telescope import *      # Multiple Classes including Enumerations
    from alpaca.exceptions import *     # Or just the exceptions you want to catch

    T = Telescope('localhost:32323', 0) # Local Omni Simulator
    try:
        T.Connected = True
        print(f'Connected to {T.Name}')
        print(T.Description)
        T.Tracking = True               # Needed for slewing (see below)
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
    except Exception as e:              # Should catch specific InvalidOperationException
        print(f'Slew failed: {str(e)}')
    finally:                            # Assure that you disconnect
        print("Disconnecting...")
        T.Connected = False
```

### Results

```tt
    Connected to Alpaca Telescope Sim
    Software Telescope Simulator for ASCOM
    Starting slew...
    ... slew completed successfully.
    RA=10.939969572854931 DE=50
    Turning off tracking then attempting to slew...
    Slew failed: SlewToCoordinatesAsync is not allowed when tracking is False
    Disconnecting...
    done
```

## Alpaca Omni Simulators

The ASCOM Alpaca Simulators are [available via GitHub here](https://github.com/DanielVanNoord/ASCOM.Alpaca.Simulators).
Using the \[[Latest](https://github.com/DanielVanNoord/ASCOM.Alpaca.Simulators/releases/tag/v0.1.2)\] link, scroll down the
Assets section and pick the package for your OS and CPU type. Extract all files to a directory and start via

```sh
./ascom-alpaca.simulators
```

(or the equivalent on Windows or MacOS). A web browser should appear. This is the primary user interface to the simulator
server and simulated devices. Once you get this running you are ready to try the sample above.

![Initial OmniSim Display](https://ascom-standards.org/alpyca/readme-assets/InitialBrowserAnnotated.png)

## ASCOM Remote

Any current ASCOM COM device that is hosted on a Windows system can have an Alpaca interface added via the
[ASCOM Remote](https://github.com/ASCOMInitiative/ASCOMRemote/releases/latest) app. This app allows you to
expose any of your Windows-hosted astronomy devices to the Alpaca world, making them reachable from programs
using alpyca-client.

## Wireshark

If you are interested in monitoring the HTTP/REST traffic that alpyca-client creates and exchanges with the
Alpaca devices, you can install the [Wireshark network protocol analyzer](https://www.wireshark.org/).
One thing that trips people up is making the installation so that Wireshark has access to all of the
network insterfaces without needing root provs (linux) or running "As Administrator" on Windows. Pay close
attention the installation steps on this. On WIndows the capture driver installation will require elevation,
as it is a privileged module. For example installinn on Linux (e.g Debian/Raspberry Pi) you'll see this,
and **be sure to answer Yes**.

![Wireshark Privileges](https://ascom-standards.org/alpyca/readme-assets/WireSharkPrivs.png)

To watch Alpaca traffic, set this simple display filter <code>http and tcp.port == 32323</code>
(with <code>32323</code> being the port of the OmniSim, see above). You'll get a nice analysis
of the Alpaca traffic like this

![Wireshark Privileges](https://ascom-standards.org/alpyca/readme-assets/Wireshark1.png)
