from alpaca.device import Device
from alpaca.telescope import GuideDirections
from alpaca.exceptions import *
from alpaca.docenum import DocIntEnum
from typing import List, Any
import requests
from requests import Response
import array

class CameraStates(DocIntEnum):
    """Current condition of the Camera"""
    cameraIdle      = 0, 'Inactive'
    cameraWaiting   = 1, 'Waiting for ??'
    cameraExposing  = 2, 'Acquiring photons'
    cameraReading   = 3, 'Reading from the sensor'
    cameraDownload  = 4, 'Downloading the image data'
    cameraError     = 5, 'An error condition exists'

class SensorTypes(DocIntEnum):    # **TODO** This is singular in the ASCOM spec
    """Type of sensor in the Camera. Names should be self-explanatory."""
    Monochrome      = 0
    Color           = 1
    RGGB            = 2
    CMYG            = 3
    CMYG2           = 4
    LRGB            = 5

class ImageArrayElementTypes(DocIntEnum):
    """The native data type of ImageArray pixels"""
    Unknown = 0
    Int16 = 1
    Int32 = 2
    Double = 3
    Single = 4, 'Unused in Alpaca 2022'
    UInt64 = 5, 'Unused in Alpaca 2022'
    Byte = 6, 'Unused in Alpaca 2022'
    Int64 = 7, 'Unused in Alpaca 2022'
    UInt16 = 8, 'Unused in Alpaca 2022'

class ImageMetadata(object):
    """Metadata describing the returned ImageArray data

        See https://ascom-standards.org/Developer/AlpacaImageBytes.pdf

    """
    def __init__(
        self,
        metadata_version: int,
        image_element_type: ImageArrayElementTypes,
        transmission_element_type: ImageArrayElementTypes,
        rank: int,
        num_x: int,
        num_y: int,
        num_z: int
    ):
        """Initialize the Camera object
        
        Args:
            metadata_version (int): Currently this is 1
            image_element_type (ImageArrayElementTypes): 
                The native data type of the original image data
            transmission_element_type (ImageArrayElementTypes): 
                The data type used when transmitting the image data
            rank (int): The matrix rank of the iamge data (either 2 or 3)
            num_x (int): Number of pixels in the X direction
            num_y (int): Number of pixels in the Y direction
            num_z (int): The index of the color plane
        
        Raises:      
            DriverException: Thrown if the driver cannot successfully complete the request.
                This exception may be encountered on any call to the device.
        
        Notes:
            * See the description of the ImageArray property for info on image element ordering in the received data. 

        """
        self.metavers = metadata_version
        self.imgtype = image_element_type
        self.xmtype = transmission_element_type
        self.rank = rank
        self.x_size = num_x
        self.y_size = num_y
        self.z_size = num_z

    @property
    def MetadataVersion(self):
        """The version of metadata, currently 1"""
        return self.metavers

    @property
    def ImageElementType(self) -> ImageArrayElementTypes: 
        """The data type of the pixels in originally acquired image
        
        Notes:
            Within Python, the returned nested list(s) image pixels themselves 
            will be either int or float. 
        """
        return self.imgtype

    @property
    def TransmissionElementType(self) -> ImageArrayElementTypes: 
        """The ddta type of the pixels in the transmitted image bytes stream

        Notes:
            Within Python, the returned image pixels themselves will be either int or float.

            To save transmission time camera may choose to use a smaller data 
            type than the original image if the pixel values would all be 
            representative in that data type without a loss of precision.

        """
        return self.xmtype

    @property
    def Rank(self):
        """The matrix rank of the image data (either 2 or 3)"""
        return self.rank

    @property
    def Dimension1(self):
        """The first (X) dimension of the image array"""
        return self.x_size

    @property
    def Dimension2(self):
        """The second (Y) dimension of the image array"""
        return self.y_size

    @property
    def Dimension3(self):
        """The third (Z) dimension of the image array (None or 3)"""
        return self.z_size

class Camera(Device):
    """ASCOM Standard iCamera V3 Interface."""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http",
    ):
        """Initialize the Camera object
        
        Args:
            address (str): IP address and port of the device (x.x.x.x:pppp)
            device_number (int): The index of the device (usually 0)
            protocol (str, optional): Only if device needs https. Defaults to "http".
        
        Raises:
            DriverException: Thrown if the driver cannot successfully complete the request. 
                This exception may be encountered on any call to the device.

        """
        super().__init__(address, "camera", device_number, protocol)
        self.img_desc = None

    @property
    def BayerOffsetX(self) -> int:
        """Return the X offset of the Bayer matrix, as defined in SensorType."""
        return self._get("bayeroffsetx")

    @property
    def BayerOffsetY(self) -> int:
        """Return the Y offset of the Bayer matrix, as defined in SensorType."""
        return self._get("bayeroffsety")

    @property
    def BinX(self) -> int:
        """**(Read/Write)** Set or return the binning factor for the X axis."""
        return self._get("binx")
    @BinX.setter
    def BinX(self, BinVal: int):
        self._put("binx", BinX=BinVal)

    @property
    def BinY(self) -> int:
        """**(Read/Write)** Set or return the binning factor for the Y axis."""
        return self._get("biny")
    @BinY.setter
    def BinY(self, BinVal: int):
        self._put("biny", BinY=BinVal)

    @property
    def CameraState(self) -> CameraStates:
        """Return the camera operational state"""
        return CameraStates(self._get("camerastate"))

    @property
    def CameraXSize(self) -> int:
        """Return the width of the camera sensor."""
        return self._get("cameraxsize")

    @property
    def CameraYSize(self) -> int:
        """Return the height of the camera sensor."""
        return self._get("cameraysize")

    @property
    def CanAbortExposure(self) -> bool:
        """Indicate whether the camera can abort exposures."""
        return self._get("canabortexposure")

    @property
    def CanAsymmetricBin(self) -> bool:
        """Indicate whether the camera supports asymmetric binning."""
        return self._get("canasymmetricbin")

    @property
    def CanFastReadout(self) -> bool:
        """Indicate whether the camera has a fast readout mode."""
        return self._get("canfastreadout")

    @property
    def CanGetCoolerPower(self) -> bool:
        """Indicate whether the camera's cooler power setting can be read."""
        return self._get("cangetcoolerpower")

    @property
    def CanPulseGuide(self) -> bool:
        """Indicate whether this camera supports pulse guiding."""
        return self._get("canpulseguide")

    @property
    def CanSetCCDTemperature(self) -> bool:
        """Indicate whether this camera supports setting the CCD temperature."""
        return self._get("cansetccdtemperature")

    @property
    def CanStopExposure(self) -> bool:
        """Indicate whether this camera can stop an exposure that is in progress."""
        return self._get("canstopexposure")

    @property
    def CCDTemperature(self) -> float:
        """Return the current CCD temperature in degrees Celsius."""
        return self._get("ccdtemperature")

    @property
    def CoolerOn(self) -> bool:
        """**(Read/Write)** Turn the camera cooler on and off or return the current cooler on/off state."""
        return self._get("cooleron")
    @CoolerOn.setter
    def CoolerOn(self, CoolerState: bool):
        self._put("cooleron", CoolerOn=CoolerState)

    @property
    def CoolerPower(self) -> float:
        """Return the present cooler power level, in percent."""
        return self._get("coolerpower")

    @property
    def ElectronsPerADU(self) -> float:
        """Return the gain of the camera (float) in photoelectrons per A/D unit."""
        return self._get("electronsperadu")

    @property
    def ExposureMax(self) -> float:
        """Return the maximum exposure time (float) supported by StartExposure."""
        return self._get("exposuremax")

    @property
    def ExposureMin(self) -> float:
        """Return the minimum exposure time (float) supported by StartExposure."""
        return self._get("exposuremin")

    @property
    def ExposureResolution(self) -> float:
        """Return the smallest increment in exposure time (float) supported by StartExposure."""
        return self._get("exposureresolution")

    @property
    def FastReadout(self) -> bool:
        """Set or return whether Fast Readout Mode is enabled.

        Args:
            FastReadout (bool): True to enable fast readout mode.
        
        Returns:
            Whether Fast Readout Mode is enabled.

        """
        return self._get("fastreadout")
    @FastReadout.setter
    def FastReadout(self, FastReadout: bool):
        self._put("fastreadout", FastReadout=FastReadout)

    @property
    def FullWellCapacity(self) -> float:
        """Report the full well capacity of the camera.

        Report the full well capacity of the camera in electrons, at the current
        camera settings (binning, SetupDialog settings, etc.).

        Returns:
            Full well capacity of the camera.

        """
        return self._get("fullwellcapacity")

    @property
    def Gain(self) -> int:
        """Set or return an index into the Gains array.

        Args:
            Gain (int): Index of the current camera gain in the Gains array.
        
        Returns:
            Index into the Gains array for the selected camera gain.
        
        """
        return self._get("gain")
    @Gain.setter
    def Gain(self, Gain: int):
        self._put("gain", Gain=Gain)

    @property
    def GainMax(self) -> int:
        """Maximum value of Gain."""
        return self._get("gainmax")

    @property
    def GainMin(self) -> int:
        """Minimum value of Gain."""
        return self._get("gainmin")

    @property
    def Gains(self) -> List[int]:
        """Gains supported by the camera."""
        return self._get("gains")

    @property
    def HasShutter(self) -> bool:
        """Indicate whether the camera has a mechanical shutter."""
        return self._get("hasshutter")

    @property
    def HeatSinkTemperature(self) -> float:
        """Return the current heat sink temperature.

        Returns:
            Current heat sink temperature (called "ambient temperature" by some
            manufacturers) in degrees Celsius.

        """
        return self._get("heatsinktemperature")

    @property
    def ImageArray(self) -> List[int]:      # TODO This could be Float
        """Return a multidimensional list containing the exposure pixel values.

        Notes:
            Automatically adapts to servers returning either JSON image data or the much
            faster ImageBytes format. In either case the returned nested list array 
            contains standard Python int or float pixel values. See
            https://ascom-standards.org/Developer/AlpacaImageBytes.pdf
            See self.ImageArrayInfo for metadata covering the returned image data.

        Returns:
            list of lists (of lists) forming a two (or three) dimensional array of integers.

        """
        return self._get_imagedata("imagearray")

    @property
    def ImageArrayVariant(self) -> List[int]:
        """Return a multidimensional list containing the exposure pixel values.

        Notes:
            Automatically adapts to servers returning either JSON image data or the much
            faster ImageBytes format. In either case the returned nested list array 
            contains standard Python int or float pixel values. See
            https://ascom-standards.org/Developer/AlpacaImageBytes.pdf
            See self.ImageArrayInfo for metadata covering the returned image data.
            Synonym of ImageArray in Alpaca

        Returns:
            list of lists (of lists) forming a two (or three) dimensional array of integers.

        """
        return self._get_imagedata("imagearray")

    @property
    def ImageArrayInfo(self) -> ImageMetadata:
        """Get image metadata sucn as dimensions, data type, rank.

        Notes:
            If no image or if the image was not transmitted via ImageBytesis,
            this returns None. 
           
        Returns:
            ImageMetadata object containing ImageBytes info about the image

        """
        return self.img_desc

    @property
    def ImageReady(self) -> bool:
        """Indicates that an image is ready to be downloaded."""
        return self._get("imageready")

    @property
    def IsPulseGuiding(self) -> bool:
        """Indicatee that the camera is pulse guideing."""
        return self._get("ispulseguiding")

    @property
    def LastExposureDuration(self) -> float:
        """Report the actual exposure duration in seconds (i.e. shutter open time)."""
        return self._get("lastexposureduration")

    @property
    def LastExposureStartTime(self) -> str:
        """Start time of the last exposure in FITS standard format.
        
        Reports the actual exposure start in the FITS-standard / ISO-8601
        CCYY-MM-DDThh:mm:ss[.sss...] format.

        Returns:
            Start time of the last exposure in FITS / ISO-8601 standard format.

        """
        return self._get("lastexposurestarttime")

    @property
    def MaxADU(self) -> int:
        """Camera's maximum ADU value."""
        return self._get("maxadu")

    @property
    def MaxBinX(self) -> int:
        """Maximum binning for the camera X axis."""
        return self._get("maxbinx")

    @property
    def MaxBinY(self) -> int:
        """Maximum binning for the camera Y axis."""
        return self._get("maxbiny")

    @property
    def NumX(self) -> int:
        """Set or return the current subframe width.
        
        Args:
            NumX (int): Subframe width, if binning is active, value is in binned
                pixels.
        
        Returns:
            Current subframe width.
        
        """
        return self._get("numx")
    @NumX.setter
    def NumX(self, NumX: int):
        self._put("numx", NumX=NumX)

    @property
    def NumY(self) -> int:
        """Set or return the current subframe height.
        
        Args:
            NumX (int): Subframe height, if binning is active, value is in binned
                pixels.
        
        Returns:
            Current subframe height.
        
        """
        return self._get("numy")
    @NumY.setter
    def NumY(self, NumY: int):
        self._put("numy", NumY=NumY)

    @property
    def Offset(self) -> int:
        """Set or return an index into the Offsets array.

        Args:
            Offset (int): Index of the current camera offset in the Offsets array.
        
        Returns:
            Index into the Offsets array for the selected camera offset.
        
        """
        return self._get("offset")
    @Offset.setter
    def Offset(self, Offset: int):
        self._put("offset", Offset=Offset)

    @property
    def OffsetMax(self) -> int:
        """Maximum value of Offset."""
        return self._get("offsetmax")

    @property
    def OffsetMin(self) -> int:
        """Minimum value of Offset."""
        return self._get("offsetmin")

    @property
    def Offsets(self) -> List[int]:
        """Offsets supported by the camera."""
        return self._get("offsets")

    @property
    def PercentCompleted(self) -> int:
        """Indicate percentage completeness of the current operation.

        Returns:
            An integer between 0 and 100% indicating the completeness of 
            this operation.

        """
        return self._get("percentcompleted")

    @property
    def PixelSizeX(self):
        """Width of CCD chip pixels (microns)."""
        return self._get("pixelsizex")

    @property
    def PixelSizeY(self):
        """Height of CCD chip pixels (microns)."""
        return self._get("pixelsizey")

    @property
    def ReadoutMode(self) -> int:
        """Set or get the canera's readout mode as an index into the array ReadoutModes."""
        return self._get("readoutmode")
    @ReadoutMode.setter
    def ReadoutMode(self, ReadoutMode: int):
        self._put("readoutmode", ReadoutMode=ReadoutMode)

    @property
    def ReadoutModes(self) -> List[str]:
        """List of available readout mode names.
        
        Notes:
            The names are indexed, and the index of the name is used to
            set and get the current readout mode.

        """
        return self._get("readoutmodes")

    @property
    def SensorName(self) -> str:
        """Name of the sensor used within the camera."""
        return self._get("sensorname")

    @property
    def SensorType(self) -> SensorTypes:
        """Type of information returned by the the camera sensor (monochrome or colour).
        
        Returns: Enum SensorTypes: 
            0 = Monochrome 
            1 = Colour (not requiring Bayer decoding)
            2 = RGGB   (Bayer encoding)
            3 = CMYG   (Bayer encoding)
            4 = CMYG2  (Bayer encoding)
            5 = LRGB   TRUESENSE Bayer encoding
       
        """
        return SensorTypes(self._get("sensortype"))
    
    @property
    def SetCCDTemperature(self) -> float:
        """Set or return the camera's cooler setpoint (degrees Celsius).

        Args:
            SetCCDTemperature (float): 	Temperature set point (degrees Celsius).
        
        Returns:
            Camera's cooler setpoint (degrees Celsius).
        
        """
        return self._get("setccdtemperature")
    @SetCCDTemperature.setter
    def SetCCDTemperature(self, SetCCDTemperature: float):
        self._put("setccdtemperature", SetCCDTemperature=SetCCDTemperature)

    @property
    def StartX(self) -> int:
        """Set or return the current subframe X axis start position.

        Args:
            StartX (int): The subframe X axis start position in binned pixels.
        
        Returns:
            Sets the subframe start position for the X axis (0 based) and returns the
            current value. If binning is active, value is in binned pixels.
        
        """
        return self._get("startx")
    @StartX.setter
    def StartX(self, StartX: int):
        self._put("startx", StartX=StartX)

    @property
    def StartY(self) -> int:
        """Set or return the current subframe Y axis start position.

        Args:
            StartY (int): The subframe Y axis start position in binned pixels.
        
        Returns:
            Sets the subframe start position for the Y axis (0 based) and returns the
            current value. If binning is active, value is in binned pixels.
        
        """
        return self._get("starty")
    @StartY.setter
    def StartY(self, StartY):
        self._put("starty", StartY=StartY)

    @property
    def SubExposureDuration(self) -> float:
        """Camera's sub-exposure interval (float)

        The Camera's sub exposure duration (float) in seconds. Only available in Camera 
        Interface Version 3 and later.

        """
        return self._get("subexposureduration")
    @SubExposureDuration.setter
    def SubExposureDuration(self, SubexposureDuration: float):
        self._put("subexposureduration", SubexposureDuration=SubexposureDuration)

    def AbortExposure(self) -> None:
        """Abort the current exposure, if any, and returns the camera to Idle state."""
        self._put("abortexposure")

    def PulseGuide(self, Direction: GuideDirections, Duration: int) -> None:
        """Pulse guide in the specified direction for the specified time (ms).
        
        Args:
            Direction (enum GuideDirections): Direction of movement 
                (0 = North, 1 = South, 2 = East, 3 = West).
            Duration (int): Duration of movement in milli-seconds.
        **TODO** Check this once the Telescope PulseGuide is working
        """
        self._put("pulseguide", Direction=Direction, Duration=Duration)

    def StartExposure(self, Duration: float, Light: bool) -> None:
        """Start an exposure. Returns if exposure has successfully been started.
        
        Notes:
            Asynchronous Use ImageReady to check when the exposure has been
            successfully completed.
        
        Args:
            Duration (float): Duration of exposure in seconds.
            Light (bool): True if light frame, false if dark frame.

        """
        self._put("startexposure", Duration=Duration, Light=Light)

    def StopExposure(self) -> None:
        """Stop the current exposure, if any.
        
        Notes:
            If an exposure is in progress, the readout process is initiated. Ignored if
            readout is already in process.
        
        """
        self._put("stopexposure")

# === LOW LEVEL ROUTINES TO GET IMAGE DATA WITH OPTIONAL IMAGEBYTES ===
#     https://www.w3resource.com/python/python-bytes.php#byte-string

    def _get_imagedata(self, attribute: str, **data) -> str:
        """TBD

        Args:
            attribute (str): Attribute to get from server.
            **data: Data to send with request.
        
        """
        url = f"{self.base_url}/{attribute}"
        hdrs = {'accept' : 'application/imagebytes'}
        pdata = {
                "ClientTransactionID": f"{Device._client_trans_id}",
                "ClientID": f"{Device._client_id}" 
                }
        pdata.update(data)
        try:
            Device._ctid_lock.acquire()
            response = requests.get("%s/%s" % (self.base_url, attribute), params = pdata, headers = hdrs)
            Device._client_trans_id += 1
        finally:
            Device._ctid_lock.release()

        if response.status_code not in range(200, 204):                 # HTTP level errors 
            raise AlpacaRequestException(response.status_code, 
                    f"{response.reason}: {response.text} (URL {response.url})")

        ct = response.headers.get('content-type')   # case insensitive
        m = 'little'
        #
        # IMAGEBYTES
        #
        if ct == 'application/imagebytes':
            b = response.content
            n = int.from_bytes(b[4:8], m)
            if n != 0:
                m = response.text[44:].decode(encoding='UTF-8')
                raise_alpaca_if(n, m)               # Will raise here
            self.img_desc = ImageMetadata(
                int.from_bytes(b[0:4], m),          # Meta version
                int.from_bytes(b[20:24], m),        # Image element type
                int.from_bytes(b[24:28], m),        # Xmsn element type
                int.from_bytes(b[28:32], m),        # Rank
                int.from_bytes(b[32:36], m),        # Dimension 1
                int.from_bytes(b[36:40], m),        # Dimension 2
                int.from_bytes(b[40:44], m)         # Dimension 3
                )
            #
            # Bless you Kelly Bundy and Mark Ransom
            # https://stackoverflow.com/questions/71774719/native-array-frombytes-not-numpy-mysterious-behavior/71776522#71776522
            #
            if self.img_desc.TransmissionElementType == ImageArrayElementTypes.Int16.value:
                tcode = 'h'
            elif self.img_desc.TransmissionElementType == ImageArrayElementTypes.UInt16.value:
                tcode = 'H'
            elif self.img_desc.TransmissionElementType == ImageArrayElementTypes.Int32.value:
                tcode = 'l'
            elif self.img_desc.TransmissionElementType == ImageArrayElementTypes.Double.value:
                tcode = 'd'
            # Extension types for future. 64-bit pixels are unlikely to be seen on the wire
            elif self.img_desc.TransmissionElementType == ImageArrayElementTypes.Byte.value:
                tcode = 'B'     # Unsigned
            elif self.img_desc.TransmissionElementType == ImageArrayElementTypes.UInt32.value:
                tcode = 'L'
            else:
               raise InvalidValueException("Unknown or as-yet unsupported ImageBytes Transmission Array Element Type")
            #
            # Assemble byte stream back into indexable machine data types
            #
            a = array.array(tcode)
            data_start = int.from_bytes(b[16:20],m)
            a.frombytes(b[data_start:])     # 'h', 'H', 16-bit ints 2 bytes get turned into Python 32-bit ints
            #
            # Convert to common Python nested list "array". 
            #
            l = []
            rows = self.img_desc.Dimension1
            cols = self.img_desc.Dimension2
            if self.img_desc.Rank == 3:
                for i in range(rows):
                    rowidx = i * cols * 3
                    r = []
                    for j in range(cols):
                        colidx = j * 3
                        r.append(a[colidx:colidx+3])
                    l.append(r)
            else:
                for i in range(rows):
                    rowidx = i * cols
                    l.append(a[rowidx:rowidx+cols])

            return l                                # Nested lists 
        #
        # JSON IMAGE DATA -> List of Lists (row major)
        #
        else:
            j = response.json()
            n = j["ErrorNumber"]
            m = j["ErrorMessage"]
            raise_alpaca_if(n, m)                   # Raise Alpaca Exception if non-zero Alpaca error
            l = j["Value"]                          # Nested lists
            if type(l[0][0]) == list:               # Test & pick up color plane
                r = 3
                d3 = len(l[0][0])
            else:
                r = 2
                d3 = 0
            self.img_desc = ImageMetadata(
                1,                                  # Meta version
                ImageArrayElementTypes.Int32,       # Image element type
                ImageArrayElementTypes.Int32,       # Xmsn element type
                r,                                  # Rank
                len(l),                             # Dimension 1
                len(l[0]),                          # Dimension 2
                d3                                  # Dimension 3
            )
            return l

def raise_alpaca_if(n, m):
    """If non-zero Alpaca error, raise the appropriate Alpaca exception

    Parameters:
        n: Error number from JSON response
        m: Message text for exception

    Returns:
        Nothing if n==0, raises if n != 0

    """
    if n == 0x0400:
        raise NotImplementedException(n, m)
    elif n == 0x0401:
        raise InvalidValueException(n, m)
    elif n == 0x0402:
        raise ValueNotSetException(n, m)
    elif n == 0x0407:
        raise NotConnectedException(n, m)
    elif n == 0x0408:
        raise ParkedException(n, m)
    elif n == 0x0409:
        raise SlavedException(n, m)
    elif n == 0x040B:
        raise InvalidOperationException(n, m)
    elif n == 0x040c:
        raise ActionNotImplementedException(n, m)
    elif n >= 0x500 and n <= 0xFFF:
        raise DriverException(n, m)
    else:
        pass
