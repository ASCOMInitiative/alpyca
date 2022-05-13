# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# observingconditions - Implements ASCOM Alpaca ObservingConditions device class
#
# Part of the Alpyca application interface package
#
# Author:   Robert B. Denny <rdenny@dc3.com> (rbd)
#
# Python Compatibility: Requires Python 3.7 or later
# Doc Environment: Sphinx v4.5.0 with autodoc, autosummary, napoleon, and autoenum
# GitHub: https://github.com/BobDenny/alpyca-client
#
# -----------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2022 Ethan Chappel and Bob Denny
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------
# Edit History:
# 02-May-22 (rbd) Initial Edit
# 13-May-22 (rbd) 2.0.0-dev1 Project now called "Alpyca" - no logic changes
# -----------------------------------------------------------------------------

from alpaca.device import Device

class ObservingConditions(Device):
    """ASCOM Standard IObservingConditions Interface
    
    Provides measurements of meterological conditions as apply
    to astronomy. Determination of safe/unsafe is made by a separate
    :py:class:`~alpaca.safetymonitor.SafetyMonitor` device. 
    
    """

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize the ObservingConditions object.
              
        Args:
            address (str): IP address and port of the device (x.x.x.x:pppp)
            device_number (int): The index of the device (usually 0)
            protocol (str, optional): Only if device needs https. Defaults to "http".

        """
        super().__init__(address, "observingconditions", device_number, protocol)

    @property
    def AveragePeriod(self) -> float:
        """(read/write) Gets And sets the time period (hours) over which observations will be averaged
        
        Raises:
            InvalidValueException: If the value set is out of bounds for this device. 
                All devices must accept 0.0 to specify that an instantaneous value 
                is to be made available.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.
        
        Notes:
            * AveragePeriod returns the time period (hours) over which sensor readings will be 
              averaged. If the device is delivering instantaneous sensor readings this property 
              will return a value of 0.0.
            * Though discouraged in the specification, possible you will receive an exception 
              if you read a sensor property when insufficient time has passed to get a true 
              average reading. 
        
        """
        return self._get("averagePeriod")

    @property
    def CloudCover(self) -> float:
        """Amount of sky obscured by cloud (0.0-1.0)
        
        Raises:
            NotImplementedException: This property is not available.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        return self._get("cloudcover")

    @property
    def DewPoint(self) -> float:
        """Atmospheric dew point temperature (deg C) at the observatory
                
        Raises:
            NotImplementedException: This property is not available.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        return self._get("dewpoint")

    @property
    def Humidity(self) -> float:
        """Atmospheric relative humidity (0-100%) at the observatory
                
        Raises:
            NotImplementedException: This property is not available.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        
        """
        return self._get("humidity")

    @property
    def Pressure(self) -> float:
        """Atmospheric pressure (hPa) at the observatory altitude
        
        Raises:
            NotImplementedException: This property is not available.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            Not "corrected to sea level" as often encountered in weather reports.
            The ConvertPressure() method may be used to get "sea level" pressure
        
        """
        return self._get("pressure")

    @property
    def RainRate(self) -> float:
        """Rain rate (mm/hr) at the observatory
                
        Raises:
            NotImplementedException: This property is not available.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        return self._get("rainrate")

    @property
    def SkyBrightness(self) -> float:
        """Sky brightness (Lux) at the observatory
                
        Raises:
            NotImplementedException: This property is not available.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        return self._get("skybrightness")

    @property
    def SkyQuality(self) -> float:
        """Sky quality (mag per sq-arcsec) at the observatory
                
        Raises:
            NotImplementedException: This property is not available.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        return self._get("skyquality")

    @property
    def SkyTemperature(self) -> float:
        """Sky temperature (deg C) at the observatory
                
        Raises:
            NotImplementedException: This property is not available.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        return self._get("skytemperature")

    @property
    def StarFWHM(self) -> float:
        """Seeing (FWHM in arc-sec) at the observatory
                
        Raises:
            NotImplementedException: This property is not available.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        return self._get("starfwhm")

    @property
    def Temperature(self) -> float:
        """Atmospheric temperature (deg C) at the observatory
                
        Raises:
            NotImplementedException: This property is not available.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        return self._get("temperature")

    @property
    def WindDirection(self) -> float:
        """Direction (deg) from which the wind is blowing at the observatory
                
        Raises:
            NotImplementedException: This property is not available.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        Notes:
            * **Meterological standards** Wind direction is that from which the wind 
              is blowing, measured in degrees clockwise from *true* North=0.0, 
              East=90.0, South=180.0, West=270.0 If the wind velocity is 0 then 
              direction is reported as 0.
            
        """
        return self._get("winddirection")

    @property
    def WindGust(self) -> float:
        """Peak 3 second wind gust (m/s) at the observatory over the last 2 minutes

        Raises:
            NotImplementedException: This property is not available.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        return self._get("windgust")

    @property
    def WindSpeed(self) -> float:
        """Wind speed (m/s) at the observatory
        
        Raises:
            NotImplementedException: This property is not available.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        return self._get("windspeed")

    def Refresh(self) -> None:
        """Forces the device to immediately query its attached hardware to refresh sensor values
        
        Raises:
            NotImplementedException: This method is not supported.
            NotConnectedException: If the device is not connected
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        self._put("refresh")

    @property
    def SensorDescription(self, PropertyName: str) -> str:
        """Description of the sensor providing the requested property
        
        Args:
            PropertyName: A string containing the name of the ObservingConditions
                meterological property for which the sensor description is desired.
                For example "WindSpeed" (for :py:attr:`WindSpeed`) would retrieve 
                a description of the sensor used to measure the wind speed.
        
        Raises:
            NotImplementedException: This method is not supported.
            NotConnectedException: If the device is not connected.
            InvalidValueException: The supplied PropertyName is not valid.
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        return self._get("sensordescription", PropertyName=PropertyName)

    def TimeSinceLastUpdate(self, PropertyName: str) -> str:
        """Elapsed time (sec) since last update of the sensor providing the requested property
        
        Args:
            PropertyName: A string containing the name of the ObservingConditions
                meterological property for which the time since last update is 
                desired. For example "WindSpeed" (for :py:attr:`WindSpeed`) would 
                retrieve the time since the wind speed was last updated by its sensor.
        
        Raises:
            NotImplementedException: This method is not supported.
            NotConnectedException: If the device is not connected.
            InvalidValueException: The supplied PropertyName is not valid.
            DriverException: An error occurred that is not described by
                one of the more specific ASCOM exceptions.
                The device did not *successfully* complete the request.

        """
        return self._get("timesincelastupdate", PropertyName=PropertyName)
