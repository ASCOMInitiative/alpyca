Version 3.1.1
=============

- Force 'localhost' to use IPv4.
- Update ``device`` unit test to work with Onmi Simulator V0.5

Version 3.1.0
=============

- Add logic to emulate asynchronous ``Connect()``, ``Disconnect()``, and ``Connecting`` API for older pre-Platform 7
  devices.
- Enhance Exception Classes with error code attribute, named properties ``number`` and ``message`` and add support
  for printing exception instances via ``str(exception)``. See the Exception Classes documentation for details.
- New Unit Test for Exceptions to assure attributes, properties, and codes.
- Several links in documentation updated, other clarifications in docs.
- Require Python 3.9 or later, no more Python 3.7, Windows 7, ancient Linux, etc.
- Change discovery to use ``ifaddr`` instead of ``netifaces``.

Version 3.0.0
=============

This production release includes the interface additions and documentation clarifications for asynchronous
behavior which are part of ASCOM Platform 7.

Changes since 2.0.4
-------------------

- Added interface members as described in `Release Notes for Interfaces as of ASCOM Platform 7 <https://ascom-standards.org/newdocs/relnotes.html#release-notes-for-interfaces-as-of-ascom-platform-7>`_
  and `published in November 2023 <https://ascomtalk.groups.io/g/Developer/message/7066>`_ on the ASCOM Developer Forum.
  These have been included in the package unit tests and validated to the best of our abilities.
- Documentation of each interface member now contains a link to the corresponding member in the
  `ASCOM Master Interfaces (Alpaca and COM) <https://ascom-standards.org/newdocs/#ascom-master-interfaces-alpaca-and-com>`_
  which serves as the definitive source of documentation (though it is generic and not Python specific).

Changes since 2.0.2 (2.0.3 unpublished)
---------------------------------------

- Switch interface now uses ``Id`` instead of ``ID`` for switch parameters. (`GitHub Issue #8 <https://github.com/ASCOMInitiative/alpyca/issues/8>`_)
- ``Focuser.StepSize`` value type corrected to float (from int) (`GitHub Issue #7 <https://github.com/ASCOMInitiative/alpyca/issues/7>`_)
- Documentation updated for changes in links to the Omni Simulator and other additions and corrections.

Changes since 2.0.1-rc1
-----------------------

- Fix discovery for multiple devices on localhost (`GitHub Issue #6 <https://github.com/ASCOMInitiative/alpyca/issues/6>`_)
- Fix ``driveRates`` enum (`GitHub Issue #3 <https://github.com/ASCOMInitiative/alpyca/issues/3>`_)
- Fix descriptive text for ``pierWest`` and ``pierUnknown`` (`GitHub Issue #5 <https://github.com/ASCOMInitiative/alpyca/issues/5>`_)
- Fix DriverVersion to return the string (`GitHub Issue #4 <https://github.com/ASCOMInitiative/alpyca/issues/4>`_)
- ``Camera.SensorTypes`` was corrected to ``Camera.SensorType`` in the interface
- Documentation corrections and clarifications

Changes since 2.0.0-dev2
------------------------

- Improve speed via re-use of sockets (``Connection: keep-alive``) for device HTTP.
- ``ObservingConditions.SensorDescription()`` has been fixed to accept the sensor name (`GitHub Issue #2 <https://github.com/ASCOMInitiative/alpyca/issues/2>`_)
- Parameters for ``ObservingConditions.TimeSinceLastUpdate()`` and
  ``ObservingConditions.SensorDescription()`` have been corrected to ``SensorName``.
- Correct ``ObservingConditions.AveragePeriod`` to remove capital P from URI
