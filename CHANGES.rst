Version 2.0.1 (2022-07-26)
==============================

- First production release

Changes since 2.0.1-rc1
-----------------------

- Camera.SensorTypes was corrected to Camera.SensorType in the interface
- Documentation corrections and clarifications

Changes since 2.0.0-dev2
------------------------

- Improve speed via re-use of sockets (``Connection: keep-alive``) for device HTTP.
- ``ObservingConditions.SensorDescription)`` has been fixed to accept the sensor name
- Parameters for ``ObservingConditions.TimeSinceLastUpdate()`` and
  ``ObservingConditions.SensorDescription()`` have been corrected to ``SensorName``.
- Correct ``ObservingConditions.AveragePeriod`` to remove capital P from URI
