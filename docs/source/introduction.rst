..
    The rinohtype PDF builder I use chokes on right-justified images
    failing to wrap them with the text. It also chokes on the |xxx|
    format hyperlinks to externals that I use for opening in a separate
    tab. Therefore I have html and rinoh conditionals in these docs (typ)

.. only:: html

    .. image:: alpaca128.png
        :height: 92px
        :width: 128px
        :align: right

Introduction and Quick Start
============================

.. only:: html

    This package provides access to ASCOM compatible astronomy devices via the Alpaca network protocol.
    For more information see the |ascsite|, specifically the |devhelp| section, the |alpacaapi|,
    and |master2|.

.. only:: rinoh or rst

    This package provides access to ASCOM compatible astronomy devices via the Alpaca network protocol.
    For more information see the
    `ASCOM Initiative web site <https://ascom-standards.org/index.htm>`_,
    specifically the
    `Alpaca Developers Info <https://ascom-standards.org/AlpacaDeveloper/Index.htm>`_
    section, the
    `Alpaca API Reference <https://ascom-standards.org/AlpacaDeveloper/ASCOMAlpacaAPIReference.html>`_,
    and the
    `ASCOM Master Interfaces (Alpaca and COM) <https://ascom-standards.org/newdocs/>`_.

.. _intro-stat:

Status of This Document
-----------------------
The descriptions of the ASCOM Standard interfaces implemented in Alpyca are
our best efforts as of February 2025, including the results of over a year of
discussion and decisions, ultimately resulting in the new interface revisions
in the ASCOM Platform 7. None of these changes are breaking. They are additions
needed to support asynchronous operations for Alpaca, and clarifications of existing
documentation to specificallly describe already asynchronous interface members.
For details see the Release notes in the Master Interfaces document liked above.

.. note::
    Changes to the interfaces are *not* breaking. Your code using this
    library is safe from being broken by such changes in the future, as
    we never make breaking changes to interface members.

Installation
------------
Requires Python 3.9 or later. The package installs from PyPi as::

    pip install alpyca

or if you have the source code in a tar file, extract it and run::

    python3 setup.py install

General Usage Pattern
---------------------
To connect and control a device, the basic steps are:

1. Import the device class and Alpaca exceptions you plan to catch
2. Create an instance of the device class, giving the IP:port and device
   index on the Alpaca server for the device(s)
3. Connect to the Alpaca server/device
4. Call methods and read/write properties as desired, catching exceptions(!)
5. Assure that you disconnect from the device.

You will be controlling *physical devices* with your function calls here.
Devices are more susceptible to problems than software. There are some
very important things to be aware of:

- Some of the methods (initiator functions) are non-blocking (asynchronous)
  and will return right away if the operation was *started* successfully.
  These are clearly marked in the docs. You must validate that the operation
  completes *successfully* (later) by reading a *completion property* which
  is documented with each non-blocking function.
- You will receive an exception wherever anything fails to complete
  *successfully*. Not only might an initiator raise an exception, but the
  completion property will raise one as well if the operation failed
  *while in progress*. Use a ``finally`` clause to assure that you disconnect
  from the device no matter what. Please see |princ|.
- Asking the device to do something by calling an (asynchronous) method requires
  you to wait until the device indicates it has completed your request. Please
  see |async|.

Simple Example
--------------

.. only:: html

    Run the self-contained cross-platform |omnisim| on your local system

.. only:: rinoh or rst

    Run the self-contained cross-platform
    `Alpaca Omni Simulator <https://github.com/ASCOMInitiative/ASCOM.Alpaca.Simulators#readme>`_
    on your local system

Then execute this little program::

    import time
    from alpaca.telescope import *              # Multiple Classes including Enumerations
    from alpaca.exceptions import *             # Or just the exceptions you want to catch

    T = Telescope('localhost:32323', 0)         # Local Omni Simulator
    try:
        T.Connect()                             # Asynchronous in Platform 7
        while t.Connecting:
            time.sleep(0.5)
        print(f'Connected to {T.Name}')
        print(T.Description)
        T.Tracking = True                       # Needed for slewing (see below)
        print('Starting slew...')
        T.SlewToCoordinatesAsync(T.SiderealTime + 2, 50)    # 2 hrs east of meridian
        while(T.Slewing):
            time.sleep(5)                       # What do a few seconds matter?
        print('... slew completed successfully.')
        print(f'RA={T.RightAscension} DE={T.Declination}')
        print('Turning off tracking then attempting to slew...')
        T.Tracking = False
        T.SlewToCoordinatesAsync(T.SiderealTime + 2, 55)  # 5 deg slew N
        # This will fail for tracking being off
        print("... you won't get here!")
    except Exception as e:                      # Should catch specific InvalidOperationException
        print(f'Caught {type(e).__name__}')
        print(f'  Slew failed: {e.message}')    # Using exception named properties
    finally:                                    # Assure that you disconnect
        print("Disconnecting...")
        T.Connected = False

Results::

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

Enhancement: Emulation of Platform 7 Async Connection API
---------------------------------------------------------
If you connect to a device whose ``InterfaceVersion`` indicates that it is older
and does not support the new asynchronous API of Platform 7 as described in the
Release Notes of the Master Interfaces Document linked above, this library will
provide emulation of those calls internally. If ``Connect()`` or
``Disconnect()`` fail after the call returns, the exception will be delivered on
the next read of ``Connecting``.

.. warning::
    If you don't read ``Connecting`` at least once after calling ``Connect()``
    or ``Disconnect()`` you may miss an exception indicating that the operation
    failed.

.. note::
    This emulation feature is provided to help beginners who aren't yet aware of the
    additional asynchronous features added to devices for Alpaca in Platform 7.
    Older drivers will still not support the other features as described in
    the Release Notes of the Master Interfaces Document linked above. It is up to
    you to check the ``InterfaceVersion`` to make sure your device supports
    the new Platform 7 features.

Member Capitalization
---------------------
This help file provides detailed descriptions of the ASCOM Interfaces
for all supported device types. Note that, rather than follow :pep:`8`,
the method and property names, as well as enumerations and exceptions,
all follow the capitalization that has historically been assigned to ASCOM
interface members. The Class and member descriptions, notes, and exceptions
raised all follow the universal ASCOM standards established long ago.

Numeric Datatypes
-----------------
The Alpyca library takes care of numeric conversions so you always work in
native Python numbers. When comparing numeric datatypes here in Python 3,
keep the following in mind:

* Python 3's ``float`` is equivalent to a double-precision floating point
  in other languages
  (e.g. ``double`` in C#, 64-bit)
* Python 3's ``int`` is not restricted by the number of bits, and can
  expand to the limit of available memory.

Example::

    # A Python 3 program to demonstrate that we can store
    # large numbers in Python 3
    x = 10000000000000000000000000000000000000000000
    x = x + 1
    print (x)

Output::

    10000000000000000000000000000000000000000001

Common Misconceptions and Confusions
------------------------------------

.. only:: html

    Throughout the evolution of ASCOM, and particularly recently with Alpaca, our goal has been to
    provide a strong framework for reliability and integrity. We see newcomers to programming
    looking for help on the |supforum|. There are a few subject areas within which misconceptions
    and confusion are common. Before starting an application development project with Alpyca,
    you may benefit from reviewing the following design principles that are *foundational*:

    * |princ|
    * |async|
    * |excep|

.. only:: rinoh or rst

    Throughout the evolution of ASCOM, and particularly recently with Alpaca, our goal has been to
    provide a strong framework for reliability and integrity. We see newcomers to programming
    looking for help on the
    `ASCOM Driver and Application Development Support Forum <https://ascomtalk.groups.io/g/Developer>`_.
    There are a few subject areas within which misconceptions
    and confusion are common. Before starting an application development project with Alpyca,
    you may benefit from reviewing the following design principles that are *foundational*:

    * `The General Principles <https://ascom-standards.org/AlpacaDeveloper/Principles.htm>`_
    * `Asynchronous APIs <https://ascom-standards.org/AlpacaDeveloper/Async.htm>`_
    * `Exceptions in ASCOM <https://ascom-standards.org/AlpacaDeveloper/Exceptions.htm>`_


.. |ascsite| raw:: html

    <a href="https://ascom-standards.org/index.htm" target="_blank">
    ASCOM Initiative web site</a> (external)

.. |devhelp| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Index.htm" target="_blank">
    Alpaca Developers Info</a> (external)

.. |master2| raw:: html

    <a href="https://ascom-standards.org/newdocs"
    target="_blank">ASCOM Master Interfaces (Alpaca and COM)</a> (external)

.. |alpacaapi| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/ASCOMAlpacaAPIReference.html" target="_blank">
    Alpaca API Reference (external)

.. |supforum| raw:: html

    <a href="https://ascomtalk.groups.io/g/Developer" target="_blank">
    ASCOM Driver and Application Development Support Forum</a> (external)

.. |princ| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Principles.htm" target="_blank">
    The General Principles</a> (external)

.. |async| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Async.htm" target="_blank">
    Asynchronous APIs</a> (external)

.. |excep| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Exceptions.htm" target="_blank">
    Exceptions in ASCOM</a> (external)

.. |omnisim| raw:: html

    <a href="https://github.com/ASCOMInitiative/ASCOM.Alpaca.Simulators#readme" target="_blank">
    Alpaca Omni Simulator</a> (external)




