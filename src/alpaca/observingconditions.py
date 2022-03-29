from alpaca.device import Device

class ObservingConditions(Device):

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize FilterWheel object."""
        super().__init__(address, "observingconditions", device_number, protocol)

    @property
    def AveragePeriod(self) -> float:
        """Gets And sets the time period over which observations will be averaged"""
        self._get("averagePeriod")

    @property
    def CloudCover(self) -> float:
        """Amount of sky obscured by cloud (0.0-1.0)"""
        self._get("cloudcover")

    @property
    def DewPoint(self) -> float:
        """Atmospheric dew point temperature (deg C) at the observatory"""
        self._get("dewpoint")

    @property
    def Humidity(self) -> float:
        """Atmospheric relative humidity (0-100%) at the observatory"""
        self._get("humidity")

    @property
    def Pressure(self) -> float:
        """Atmospheric pressure (hPa) at the observatory altitude

        Notes:
            Not "corrected to sea level" as often encountered in weather reports.
            The ConvertPressure() method may be used to get "sea level" pressure
        
        """
        self._get("pressure")

    @property
    def RainRate(self) -> float:
        """Rain rate (mm/hr) at the observatory"""
        self._get("rainrate")

    @property
    def SkyBrightness(self) -> float:
        """Sky brightness (Lux) at the observatory"""
        self._get("skybrightness")

    @property
    def SkyQuality(self) -> float:
        """Sky quality (mag per sq-arcsec) at the observatory"""
        self._get("skyquality")

    @property
    def SkyTemperature(self) -> float:
        """Sky temperature (deg C) at the observatory"""
        self._get("skytemperature")

    @property
    def StarFWHM(self) -> float:
        """Seeing (FWHM in arc-sec) at the observatory"""
        self._get("starfwhm")

    @property
    def Temperature(self) -> float:
        """Atmospheric temperature (deg C) at the observatory"""
        self._get("temperature")

    @property
    def WindDirection(self) -> float:
        """Direction (deg) from which the wind is blowing at the observatory
        
        Meterological standards:
            Wind direction is that from which the wind is blowing, measured in degrees
            clockwise from true North=0.0, East=90.0, South=180.0, West=270.0 If the 
            wind velocity is 0 then direction is reported as 0.
            
            """
        self._get("winddirection")

    @property
    def WindGust(self) -> float:
        """Peak 3 second wind gust (m/s) at the observatory over the last 2 minutes"""
        self._get("windgust")

    @property
    def WindSpeed(self) -> float:
        """Wind speed (m/s) at the observatory"""
        self._get("windgust")

    def Refresh(self) -> None:
        """Forces the device to immediately query its attached hardware to refresh sensor values"""
        self._put("refresh")

    def SensorDescription(self, PropertyName: str) -> str:
        """Description of the sensor providing the requested property"""
        self._get("sensordescription", PropertyName=PropertyName)

    def TimeSinceLastpdate(self, PropertyName: str) -> str:
        """Elapsed time (sec) since last update of the sensor providing the requested property"""
        self._get("timesincelastupdate", PropertyName=PropertyName)
