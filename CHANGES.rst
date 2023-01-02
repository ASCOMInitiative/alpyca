Version 2.0.4 (2023-01-01)
==============================

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
