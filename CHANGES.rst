Version 2.0.1-rc1 (2022-07-17)
==============================

- Release candidate. 

Changes since 2.0.0-dev2
------------------------

- Improve speed via re-use of sockets (<code>Connection: keep-alive</code>) for device HTTP.
- <code>ObservingConditions.SensorDescription()</code> has been fixed to accept the sensor name
- Parameters for <code>ObservingConditions.TimeSinceLastUpdate()</code> and
  <code>ObservingConditions.SensorDescription()</code> have been corrected to <code>SensorName</code>.
- Correct <code>ObservingConditions.AveragePeriod</code> to remove capital P from URI

