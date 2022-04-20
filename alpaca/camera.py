from alpaca.device import Device
from alpaca.telescope import GuideDirections
from alpaca.exceptions import *
from alpaca.docenum import DocIntEnum
from typing import List, Any
#import requests
#from requests import Response
import httpx
import array

class CameraStates(DocIntEnum):
    """Current condition of the Camera"""
    cameraIdle      = 0, 'Inactive'
    cameraWaiting   = 1, 'Waiting for ??'
    cameraExposing  = 2, 'Acquiring photons'
    cameraReading   = 3, 'Reading from the sensor'
    cameraDownload  = 4, 'Downloading the image data'
    cameraError     = 5, 'An error condition exists'

class SensorTypes(DocIntEnum):    # TODO This is singular in the ASCOM spec
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

        Notes:
            * Constructed internally by the library during image retrieval.
            * See https://ascom-standards.org/Developer/AlpacaImageBytes.pdf

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
        
        """
        super().__init__(address, "camera", device_number, protocol)
        self.img_desc = None

    @property
    def BayerOffsetX(self) -> int:
        """The X offset of the Bayer matrix, as defined in property :py:attr:`SensorType`
        
        Raises:
        
            NotImplementedException: Monochrome cameras throw this exception, 
                colour cameras do not.
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
            InvalidValueException: If not valid.

        Notes:
            * The value returned will be in the range 0 to M-1 where M is the width of 
              the Bayer matrix. The offset is relative to the 0,0 pixel in the sensor 
              array, and does not change to reflect subframe settings.
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("bayeroffsetx")

    @property
    def BayerOffsetY(self) -> int:
        """The Y offset of the Bayer matrix, as defined in property :py:attr:`SensorType`
        
        Raises:
        
            NotImplementedException: Monochrome cameras throw this exception, 
                colour cameras do not.
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
            InvalidValueException: If not valid.

        Notes:
            * The value returned will be in the range 0 to M-1 where M is the width of 
              the Bayer matrix. The offset is relative to the 0,0 pixel in the sensor 
              array, and does not change to reflect subframe settings.
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("bayeroffsety")

    @property
    def BinX(self) -> int:
        """**(Read/Write)** Set or return the binning factor for the X axis.

        Raises:      
            InvalidValueException: If the given binning value is invalid
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * Will default to 1 when the camera connection is established. 
            * Camera does not check for compatible subframe values when this property
              is set; rather they are checked upon :py:meth:`StartExposure()`. 
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("binx")
    @BinX.setter
    def BinX(self, BinVal: int):
        self._put("binx", BinX=BinVal)

    @property
    def BinY(self) -> int:
        """**(Read/Write)** Set or return the binning factor for the Y axis.

        Raises:      
            InvalidValueException: If the given binning value is invalid
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * Will default to 1 when the camera connection is established. 
            * Camera does not check for compatible subframe values when this property
              is set; rather they are checked upon :py:meth:`StartExposure()`. 
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("biny")
    @BinY.setter
    def BinY(self, BinVal: int):
        self._put("biny", BinY=BinVal)

    @property
    def CameraState(self) -> CameraStates:
        """The camera's operational state (:py:class:`CameraStates`)
        
        Raises:
            NotConnectedException: If the camera status is unavailable
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        return CameraStates(self._get("camerastate"))

    @property
    def CameraXSize(self) -> int:
        """The width of the camera sensor in unbinned pixels
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("cameraxsize")

    @property
    def CameraYSize(self) -> int:
        """The height of the camera sensor in unbinned pixels
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("cameraysize")

    @property
    def CanAbortExposure(self) -> bool:
        """The camera can abort exposures

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * Some cameras support :py:meth:`AbortExposure()`, which allows the exposure to be 
              terminated before the exposure timer completes, *with the image being discarded*.
              Returns True if :py:meth:`AbortExposure()` is available, False if not. See also
              :py:meth:`StopExposure()`
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("canabortexposure")

    @property
    def CanAsymmetricBin(self) -> bool:
        """The camera supports asymmetric binning

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * If true, the camera can have different binning on the X and Y axes, as 
              determined by BinX and BinY. If false, the binning must be equal on the X and Y axes.
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """             
        return self._get("canasymmetricbin")

    @property
    def CanFastReadout(self) -> bool:
        """The camera supports a fast readout mode

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """             
        return self._get("canfastreadout")

    @property
    def CanGetCoolerPower(self) -> bool:
        """The camera's cooler power level is available via :py:attr:`CoolerPower`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """             
        return self._get("cangetcoolerpower")

    @property
    def CanPulseGuide(self) -> bool:
        """The camera supports pulse guiding via :py:meth:`PulseGuide()`

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """             
        return self._get("canpulseguide")

    @property
    def CanSetCCDTemperature(self) -> bool:
        """The camera cooler temperature can be controlled 

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * If True, the camera's cooler setpoint can be adjusted. If False, the 
              camera either uses open-loop cooling or does not have the ability to 
              adjust temperature from software, and setting the :py:attr:`SetCCDTemperature` 
              property has no effect.
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("cansetccdtemperature")

    @property
    def CanStopExposure(self) -> bool:
        """The camera can stop exposures

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * Some cameras support :py:meth:`StopExposure()`, which allows the exposure to be 
              terminated before the exposure timer completes, *but will still read out the image*. 
              Returns True if :py:meth:`StopExposure()` is available, False if not. See also
              :py:meth:`AbortExposure()`.
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("canstopexposure")

    @property
    def CCDTemperature(self) -> float:
        """The current CCD temperature in degrees Celsius.

        Raises:
            InvalidValueException: If data unavailable.
            NotImplementedException: If not supported (no cooler)
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        return self._get("ccdtemperature")

    @property
    def CoolerOn(self) -> bool:
        """**(Read/Write)** Turn the camera cooler on and off or return the current cooler on/off state.
        
        Raises:
            NotConnectedException: If the device is not connected
            NotImplementedException: If not supported (no cooler)
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Warning:
            Turning the cooler off when the cooler is operating at high delta-T 
            (typically >20C below ambient) may result in thermal shock. Repeated thermal 
            shock may lead to damage to the sensor or cooler stack. Please consult the 
            documentation supplied with the camera for further information. 
        
        """
        return self._get("cooleron")
    @CoolerOn.setter
    def CoolerOn(self, CoolerState: bool):
        self._put("cooleron", CoolerOn=CoolerState)

    @property
    def CoolerPower(self) -> float:
        """The current cooler power level in percent.

        Raises:
            NotImplementedException: If not supported (no cooler)
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        return self._get("coolerpower")

    @property
    def ElectronsPerADU(self) -> float:
        """The gain of the camera in photoelectrons per A/D unit.
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * TODO Some cameras have multiple gain modes, resulting in this value changing.
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("electronsperadu")

    @property
    def ExposureMax(self) -> float:
        """The maximum exposure time (sec) supported by :py:meth:`StartExposure()`.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.
        """
        return self._get("exposuremax")

    @property
    def ExposureMin(self) -> float:
        """The minimum exposure time (sec) supported by :py:meth:`StartExposure()`.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.
        """
        return self._get("exposuremin")

    @property
    def ExposureResolution(self) -> float:
        """The smallest increment in exposure time (sec) supported by :py:meth:`StartExposure()`.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * This can be used, for example, to specify the resolution of a user interface 
              "spin control" used to dial in the exposure time. 
            * The duration provided to :py:meth:`StartExposure()` does not have to be an 
              exact multiple of this number; the driver will choose the closest available 
              value. Also in some cases the resolution may not be constant over the full 
              range of exposure times; in this case the smallest increment will be chosen 
              by the driver. A value of 0.0 indicates that there is no minimum resolution 
              except that imposed by the resolution of the float data type.
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.
        """
        return self._get("exposureresolution")

    @property
    def FastReadout(self) -> bool:
        """(Read/Write) Gets or sets Fast Readout Mode.

        Raises:
            NotImplementedException: If FastReadout is not supported
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * This function may in some cases interact with :py:attr:`ReadoutModes`; for 
              example, there may be modes where the Fast/Normal switch is meaningless. 
              In this case, it may be preferable to use the :py:attr:`ReadoutModes` 
              feature to control fast/normal switching.

        """
        return self._get("fastreadout")
    @FastReadout.setter
    def FastReadout(self, FastReadout: bool):
        self._put("fastreadout", FastReadout=FastReadout)

    @property
    def FullWellCapacity(self) -> float:
        """The full well capacity of the camera (see Notes).

        Raises:
            NotConnectedException: If the device is not connected.
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Reports the full well capacity of the camera in electrons, at the current
              camera settings (binning, SetupDialog settings, etc.).
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """

        return self._get("fullwellcapacity")

    @property
    def Gain(self) -> int:
        """(Read/Write) Gets or sets the current gain value or index (**see Notes**)

        Raises:
            InvalidValueException: If the supplied valus is not valid 
            NotImplementedException: If neither **gains index** mode nor **gains value**
                mode are supported.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            The Gain property is used to adjust the gain setting of the camera and has 
            two modes of operation:

            * **Gains-Index:** The Gain property is the selected gain's index within 
              the :py:attr:`Gains` array of textual gain descriptions.

                * In this mode the Gains method returns a *0-based* array of strings, which 
                  describe available gain settings e.g. "ISO 200", "ISO 1600" 
                * :py:attr:`GainMin` and :py:attr:`GainMax` will throw a **NotImplementedException**.

            * **Gains-Value:** The Gain property is a direct numeric representation 
              of the camera's gain.

                * In this mode the :py:attr:`GainMin` and :py:attr:`GainMax` properties must 
                  return integers specifying the valid range for Gain.
                * The :py:attr:`Gains` array property will throw a **NotImplementedException**.

            A driver can support none, one or both gain modes depending on the camera's capabilities. 
            However, only one mode can be active at any one moment because both modes share the 
            Gain property to return the gain value. Your application can determine 
            which mode is operational by reading the :py:attr:`GainMin`, :py:attr:`GainMax` 
            property and this Gain property. If a property can be read then its associated mode 
            is active, if it throws a **NotImplementedException** then the mode is not active.
        
        Important:
            The :py:attr:`ReadoutMode` may in some cases affect the gain of the camera; if so, 
            the driver must ensure that the two properties do not conflict if both are used.
                  
        """
        return self._get("gain")
    @Gain.setter
    def Gain(self, Gain: int):
        self._put("gain", Gain=Gain)

    @property
    def GainMax(self) -> int:
        """Maximum gain value that this camera supports (see notes and :py:attr:`Gain`)
        
        Raises:
            NotImplementedException: If the :py:attr:`Gain` property is not 
                implemented or is operating in **gains-index** mode.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            When :py:attr:`Gain` is operating in **gain-value** mode:

            * GainMax must return the camera's highest valid :py:attr:`Gain` setting
            * The :py:attr:`Gains` property will throw **NotImplementedException**

            GainMax and :py:attr:`GainMin` act together and that either both will 
            return values, or both will throw **NotImplementedException**.

            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("gainmax")

    @property
    def GainMin(self) -> int:
        """Minimum gain value that this camera supports (see notes and :py:attr:`Gain`)
        
        Raises:
            NotImplementedException: If the :py:attr:`Gain` property is not 
                implemented or is operating in **gains-index** mode.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            When :py:attr:`Gain` is operating in **gain-value** mode:

            * GainMin must return the camera's highest valid :py:attr:`Gain` setting
            * The :py:attr:`Gains` property will throw **NotImplementedException**

            GainMin and :py:attr:`GainMax` act together and that either both will 
            return values, or both will throw **NotImplementedException**.

            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

         """     
        return self._get("gainmin")

    @property
    def Gains(self) -> List[str]:
        """List of Gain *names* supported by the camera (see notes and :py:attr:`Gain`)
        
        Raises:
            NotImplementedException: If the :py:attr:`Gain` property is not 
                implemented or is operating in **gains-value** mode.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            When :py:attr:`Gain` is operating in the **gains-index** mode:

            * The Gains property returns a list of available gain setting *names*.
            * The :py:attr:`GainMax` and :py:attr:`GainMin` properties will throw
              **NotImplementedException**.

            The returned gain names could, for example, be a list of ISO settings 
            for a DSLR camera or a list of gain names for a CMOS camera. Typically 
            the application software will display the returned gain names in a 
            drop list, from which the astronomer can select the required value. 
            The application can then configure the required gain by setting the 
            camera's Gain property to the *array index* of the selected description.

            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("gains")

    @property
    def HasShutter(self) -> bool:
        """Indicate whether the camera has a mechanical shutter.
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            If HasShutter is False, the :py:meth:`StartExposure()` method will ignore the 
            Light parameter. 

        """
        return self._get("hasshutter")

    @property
    def HeatSinkTemperature(self) -> float:
        """The current heat sink (aka "ambient") temperature (deg C).

        Raises:
            NotConnectedException: If the device is not connected
            NotImplementedException: If :py:attr:`CanSetCCDTemperature` is False
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        return self._get("heatsinktemperature")

    @property
    def ImageArray(self) -> List[int]:      # TODO This could be Float
        """Return a multidimensional list containing the exposure pixel values.

        Raises:
            InvalidOperationException: If no image data is available
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * The returned array is in row-major format, and typically must be transposed
              for use with *numpy* and *astropy* for creating FITS files. See the example
              below. 
            * Automatically adapts to devices returning either JSON image data or the much
              faster ImageBytes format. In either case the returned nested list array 
              contains standard Python int or float pixel values. See
              https://ascom-standards.org/Developer/AlpacaImageBytes.pdf
              See :py:attr:`ImageArrayInfo` for metadata covering the returned image data.

        """
        return self._get_imagedata("imagearray")

    @property
    def ImageArrayInfo(self) -> ImageMetadata:
        """Get image metadata sucn as dimensions, data type, rank.

        See Class :py:class:`ImageMetadata` for the properties available. 

        Notes:
            If no image has been retrieved via :py:attr:`ImageArray`, 
            this returns None. 
 
        """
        return self.img_desc

    @property
    def ImageReady(self) -> bool:
        """Indicates that an image is ready to be downloaded.
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the previous
                :py:meth:`Expose()` request
                (see Attention below). This exception may be encountered on any 
                call to the device.

        Notes:
            * If ImageReady returns a valid False or True value, then the *non-blocking*
              process of acquiring an image is *proceeding normally* or has been *successful*. 
            * ImageReady will be False immediately upon return from :py:meth:`StartExposure()`. 
              It will remain False until the exposure has been *successfully* completed and 
              an image is ready for download.

        Attention:
            * If the camera encounters a problem which prevents or prevented it from 
              *successfully* completing the exposure, the driver will raise an 
              exception when you attempt to read ImageReady. 

        """
        return self._get("imageready")

    @property
    def IsPulseGuiding(self) -> bool:
        """Indicates that the camera is currently in a :py:meth:`PulseGuide()` operation.
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request
                (see Attention below). This exception may be encountered on any 
                call to the device.

        Notes:
            * If IsPulseGuiding returns a valid True or False value, then the process of
              pulse-guiding is *proceeding normally* or has completed *successfully*,
              respectively. 
            * IsPulseGuiding will be True immediately upon return from :py:meth:`PulseGuide()`. 
              It will remain True until the requested pulse-guide interval has elapsed, and
              the pulse-guiding operation has been *successfully* completed. If 
              :py:meth:`PulseGuide()` returns with IsPulseGuiding = False, then you can
              assume that the operation *succeeded* with a very short pulse-guide interval.

        Attention:
            * If the camera encounters a problem which prevents it from *successfully*
              completing the the pulse-guiding operation, the driver will raise an exception 
              when you attempt to read IsPulseGuiding.

        
        
        """
        return self._get("ispulseguiding")

    @property
    def LastExposureDuration(self) -> float:
        """Report the actual exposure duration in seconds (i.e. shutter open time).

        Raises:
            NotImplementedException: If the camera doesn't support this feature
            InvalidOperationException: If no image has yet been *successfully* acquired.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request
                (see Attention below). This exception may be encountered on any 
                call to the device.

        Notes:
            * This may differ from the exposure time requested due to shutter latency, 
              camera timing precision, etc. 
        
        """
        return self._get("lastexposureduration")

    @property
    def LastExposureStartTime(self) -> str:
        """Start time of the last exposure in FITS standard format, UTC.
        
        Raises:
            NotImplementedException: If the camera doesn't support this feature
            InvalidOperationException: If no image has yet been *successfully* acquired.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request
                (see Attention below). This exception may be encountered on any 
                call to the device.

        Notes:
            Reports the actual exposure UTC start date/time in the 
            FITS-standard / ISO-8601 CCYY-MM-DDThh:mm:ss[.sss...] format. 

        """
        return self._get("lastexposurestarttime")

    @property
    def MaxADU(self) -> int:
        """The maximum ADU value of the camera.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("maxadu")

    @property
    def MaxBinX(self) -> int:
        """The maximum supported X binning value of the camera.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("maxbinx")

    @property
    def MaxBinY(self) -> int:
        """The maximum supported Y binning value of the camera.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("maxbiny")

    @property
    def NumX(self) -> int:
        """(Read/Write) Set or return the current subframe width.
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * If binning is active, value is in binned pixels. 
            * Defaults to :py:attr:`CameraXSize` with :py:attr:`StartX` = 0
              (full frame) on initial camera startup.
        
        Attention:
            * No error check is performed for incompatibilty with :py:attr:`BinX`, 
              and :py:attr:`StartX`, If these values are incompatible, you will
              receive an **InvalidValueException** from a subsequent call to 
              :py:meth:`StartExposure()`.
        
        """
        return self._get("numx")
    @NumX.setter
    def NumX(self, NumX: int):
        self._put("numx", NumX=NumX)

    @property
    def NumY(self) -> int:
        """(Read/Write) Set or return the current subframe height.
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * If binning is active, value is in binned pixels. 
            * Defaults to :py:attr:`CameraYSize` with :py:attr:`StartY` = 0
              (full frame) on initial camera startup.
        
        Attention:
            * No error check is performed for incompatibilty with :py:attr:`BinY`, 
              and :py:attr:`StartY`, If these values are incompatible, you will
              receive an **InvalidValueException** from a subsequent call to 
              :py:meth:`StartExposure()`.
        
        """
        return self._get("numy")
    @NumY.setter
    def NumY(self, NumY: int):
        self._put("numy", NumY=NumY)

    @property
    def Offset(self) -> int:
        """(Read/Write) Gets or sets the current offset value or index (**see Notes**)

        Raises:
            InvalidValueException: If the supplied value is not valid 
            NotImplementedException: If neither **offsets index** mode nor **offsets value**
                mode are supported.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            The Offset property is used to adjust the offset setting of the camera and has 
            two modes of operation:

            * **Offsets-Index:** The Offset property is the selected offset's index within 
              the :py:attr:`Offsets` array of textual offset descriptions.

                * In this mode the Offsets method returns a *0-based* array of strings, which 
                  describe available offset settings.
                * :py:attr:`OffsetMin` and :py:attr:`OffsetMax` will throw a **NotImplementedException**.

            * **Offsets-Value:** The Offset property is a direct numeric representation 
              of the camera's offset.

                * In this mode the :py:attr:`OffsetMin` and :py:attr:`OffsetMax` properties must 
                  return integers specifying the valid range for Offset.
                * The :py:attr:`Offsets` array property will throw a **NotImplementedException**.

            A driver can support none, one or both offset modes depending on the camera's capabilities. 
            However, only one mode can be active at any one moment because both modes share the 
            Offset property to return the offset value. Your application can determine 
            which mode is operational by reading the :py:attr:`OffsetMin`, :py:attr:`OffsetMax` 
            property and this Offset property. If a property can be read then its associated mode 
            is active, if it throws a **NotImplementedException** then the mode is not active.
        
        Important:
            The :py:attr:`ReadoutMode` may in some cases affect the offset of the camera; if so, 
            the driver must ensure that the two properties do not conflict if both are used.

        """          
        return self._get("offset")
    @Offset.setter
    def Offset(self, Offset: int):
        self._put("offset", Offset=Offset)

    @property
    def OffsetMax(self) -> int:
        """Maximum offset value that this camera supports (see notes and :py:attr:`Offset`)
        
        Raises:
            NotImplementedException: If the :py:attr:`Offset` property is not 
                implemented or is operating in **offsets-index** mode.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            When :py:attr:`Offset` is operating in **offsets-value** mode:

            * OffsetMax must return the camera's highest valid :py:attr:`Offset` setting
            * The :py:attr:`Offsets` property will throw **NotImplementedException**

            OffsetMax and :py:attr:`OffsetMin` act together and that either both will 
            return values, or both will throw **NotImplementedException**.

            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("offsetmax")

    @property
    def OffsetMin(self) -> int:
        """Minimum offset value that this camera supports (see notes and :py:attr:`Offset`)
        
        Raises:
            NotImplementedException: If the :py:attr:`Offset` property is not 
                implemented or is operating in **offsets-index** mode.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            When :py:attr:`Offset` is operating in **offsets-value** mode:

            * OffsetMin must return the camera's highest valid :py:attr:`Offset` setting
            * The :py:attr:`Offsets` property will throw **NotImplementedException**

            OffsetMin and :py:attr:`OffsetMax` act together and that either both will 
            return values, or both will throw **NotImplementedException**.

            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

         """     
        return self._get("offsetmin")

    @property
    def Offsets(self) -> List[str]:
        """List of Offset *names* supported by the camera (see notes and :py:attr:`Offset`)
        
        Raises:
            NotImplementedException: If the :py:attr:`Offset` property is not 
                implemented or is operating in **offsets-value** mode.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            When :py:attr:`Offset` is operating in the **offsets-index** mode:

            * The Offsets property returns a list of available offset setting *names*.
            * The :py:attr:`OffsetMax` and :py:attr:`OffsetMin` properties will throw
              **NotImplementedException**.

            The returned offset names could, for example, be a list of ISO settings 
            for a DSLR camera or a list of offset names for a CMOS camera. Typically 
            the application software will display the returned offset names in a 
            drop list, from which the astronomer can select the required value. 
            The application can then configure the required offset by setting the 
            camera's Offset property to the *array index* of the selected description.

            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("offsets")

    @property
    def PercentCompleted(self) -> int:
        """The percentage completeness of this operation
        
        Raises:
            InvalidOperationException: When it is inappropriate to ask for a 
                completion percentage.
            NotImplementedException: If this optional property is not implemented.
            NotConnectedException: If the device is not connected.
            DriverException: If the device cannot *successfully* complete the request
                (see Attention below). This exception may be encountered on any 
                call to the device.

        Notes:
            * If valid, returns an integer between 0 and 100, where 0 indicates 0% progress 
              (function just started) and 100 indicates 100% progress (i.e. completion). 
            * At the discretion of the device, PercentCompleted may optionally be valid 
              when :py:attr:`CameraState` is in any or all of the following states: 
              
                * cameraExposing
                * cameraWaiting
                * cameraReading
                * cameraDownload
            
            In all other states an **InvalidOperationException** will be raised.

        Attention:
            * If the camera encounters a problem which prevents or prevented it from 
              *successfully* completing the operation, the driver will raise an 
              exception when you attempt to read PercentComplete. 

        """
        return self._get("percentcompleted")

    @property
    def PixelSizeX(self) -> float:
        """The width (microns) of the camera sensor elements.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("pixelsizex")

    @property
    def PixelSizeY(self) -> float:
        """The height (microns) of the camera sensor elements.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("pixelsizey")

    @property
    def ReadoutMode(self) -> int:
        """(Read/Write) Gets or sets the current camera readout mode (**see Notes**)

        Raises:
            InvalidValueException: If the supplied value is not valid (index out of range)
            NotImplementedException: If :py:attr:`CanFastReadout` is True.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * ReadoutMode is an index into the array :py:attr:`ReadoutModes`, and 
              selects the desired readout mode for the camera. Defaults to 0 if not set. 
            * It is strongly recommended, but not required, that cameras make the 0-index 
              mode suitable for standard imaging operations, since it is the default.

        Important:
            The :py:attr:`ReadoutMode` may in some cases affect the :py:attr:`Gain`
            and/or :py:attr:`Offset` of the camera; if so, the camera must ensure 
            that the two properties do not conflict if both are used.

        """          
        return self._get("readoutmode")
    @ReadoutMode.setter
    def ReadoutMode(self, ReadoutMode: int):
        self._put("readoutmode", ReadoutMode=ReadoutMode)

    @property
    def ReadoutModes(self) -> List[str]:
        """List of ReadoutMode *names* supported by the camera (see notes and :py:attr:`ReadoutMode`)
        
        Raises:
            NotImplementedException: If the :py:attr:`ReadoutMode` property is not 
                implemented.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * Readout modes may be available from the camera, and if so then 
              :py:attr:`CanFastReadout` will be False. The two camera mode selection
              schemes are mutually exclusive.
            * This property provides an array of strings, each of which describes an 
              available readout mode of the camera. At least one string will be present 
              in the list. Your application may use this list to present to the user a 
              drop-list of modes. The choice of available modes made available is 
              entirely at the discretion of the camera. Please note that if the camera 
              has many different modes of operation, then the most commonly adjusted 
              settings will probably be in ReadoutModes; additional settings may be 
              provided using :py:meth:`SetupDialog()`. 
            * To select a mode, set ReadoutMode to the index of the desired mode. 
              The index is zero-based.
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("readoutmodes")

    @property
    def SensorName(self) -> str:
        """The name of the sensor used within the camera.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Returns the name (data sheet part number) of the sensor, e.g. ICX285AL. 
              The format is to be exactly as shown on manufacturer data sheet, 
              subject to the following rules: 

                * All letters will be upper-case.
                * Spaces will not be included.
                * Any extra suffixes that define region codes, package types, temperature range, 
                  coatings, grading, colour/monochrome, etc. will not be included.
                * For colour sensors, if a suffix differentiates different Bayer matrix encodings, 
                  it will be included.
                * The property will return an empty string if the sensor name is not known
            * Examples:
                * ICX285AL-F shall be reported as ICX285
                * KAF-8300-AXC-CD-AA shall be reported as KAF-8300
            * The most common usage of this property is to select approximate colour balance 
              parameters to be applied to the Bayer matrix of one-shot colour sensors. 
              Application authors should assume that an appropriate IR cut-off filter is 
              in place for colour sensors.
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return self._get("sensorname")

    @property
    def SensorType(self) -> SensorTypes:
        """The type of sensor within the camera.

        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * It is recommended that this property be retrieved only after a connection is 
              established with the camera hardware, to ensure that the driver is
              aware of the capabilities of the specific camera model.

        """
        return SensorTypes(self._get("sensortype"))
    
    @property
    def SetCCDTemperature(self) -> float:
        """(Read/Write) Get or set the camera's cooler setpoint (degrees Celsius).

        Raises:
            InvalidValueException: If set to a value outside the camera's valid
                temperature setpoint range.
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        return self._get("setccdtemperature")
    @SetCCDTemperature.setter
    def SetCCDTemperature(self, SetCCDTemperature: float):
        self._put("setccdtemperature", SetCCDTemperature=SetCCDTemperature)

    @property
    def StartX(self) -> int:
        """(Read/Write) Set or return the current X-axis subframe start position.
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * If binning is active, value is in binned pixels. 
            * Defaults to 0 with :py:attr:`NumX` = :py:attr:`CameraXSize`
              (full frame) on initial camera startup.
        
        Attention:
            * No error check is performed for incompatibilty with :py:attr:`BinX`, 
              and :py:attr:`NumX`, If these values are incompatible, you will
              receive an **InvalidValueException** from a subsequent call to 
              :py:meth:`StartExposure()`.
        
        """
        return self._get("startx")
    @StartX.setter
    def StartX(self, StartX: int):
        self._put("startx", StartX=StartX)

    @property
    def StartY(self) -> int:
        """(Read/Write) Set or return the current Y-axis subframe start position.
        
        Raises:
            NotConnectedException: If the device is not connected
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * If binning is active, value is in binned pixels. 
            * Defaults to 0 with :py:attr:`NumY` = :py:attr:`CameraYSize`
              (full frame) on initial camera startup.
        
        Attention:
            * No error check is performed for incompatibilty with :py:attr:`BinY`, 
              and :py:attr:`NumY`, If these values are incompatible, you will
              receive an **InvalidValueException** from a subsequent call to 
              :py:meth:`StartExposure()`.
        
        """
        return self._get("starty")
    @StartY.setter
    def StartY(self, StartY):
        self._put("starty", StartY=StartY)

    @property
    def SubExposureDuration(self) -> float:
        """(Read/Write) Set or return the camera's sub-exposure interval (sec)

        Raises:
            NotImplementedException: The camera does not support 
                on-board stacking with user-supplied sub-exposure interval.
            NotConnectedException: If the device is not connected.
            InvalidValueException: The supplied duration is not valid.
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        """
        return self._get("subexposureduration")
    @SubExposureDuration.setter
    def SubExposureDuration(self, SubexposureDuration: float):
        self._put("subexposureduration", SubexposureDuration=SubexposureDuration)

    def AbortExposure(self) -> None:
        """Abort the current exposure, if any, and returns the camera to Idle state.
        
        Raises:
            NotConnectedException: If the device is not connected.
            InvalidOperationException: If not currently possible (e.g. during image download)
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Unlike :py:meth:`StopExposure()` this method simply discards any
              partially-acquired image data and returns the camera to idle.
            * Will not raise an exception if the camera is already idle.
     
        """
        self._put("abortexposure")

    def PulseGuide(self, Direction: GuideDirections, Duration: int) -> None:
        """Pulse guide in the specified direction for the specified time (ms).
        
        **Non-blocking**: See Notes, and :ref:`async_faq`

        Args:
            Direction: :py:class:`~alpaca.telescope.GuideDirections`
            Interval: duration of the guide move, milliseconds

        Raises:
            NotImplementedException: If the camera does not support pulse guiding 
                (:py:attr:`CanPulseGuide` property is False)
            NotConnectedException: If the device is not connected.
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.
        
        Notes:
            * **Asynchronous**: The method returns as soon pulse-guiding operation
              has been *successfully* started with :py:attr:`IsPulseGuiding' property True. 
              However, you may find that :py:attr:`IsPulseGuiding' is False when you get 
              around to checking it if the 'pulse' is short. This is still a success if you
              get False back and not an exception. See :ref:`async_faq`
            * Some cameras have implemented this as a Synchronous (blocking) operation.
            * :py:class:`~alpaca.telescope.GuideDirections` for North and South 
              have varying interpretations
              by German Equatorial mounts. Some GEM mounts interpret North to be 
              the same rotation direction of the declination axis regardless of 
              their pointing state ("side of the pier"). Others truly implement 
              North and South by reversing the dec-axis rotation depending on 
              their pointing state. **Apps must be prepared for either behavior**. 

        """
        self._put("pulseguide", Direction=Direction, Duration=Duration)

    def StartExposure(self, Duration: float, Light: bool) -> None:
        """Start an exposure. 

        **Non-blocking**: Returns with :py:attr:`ImageReady` = False 
        if exposure has *successfully* been started. See :ref:`async_faq`
        
        Args:
            Duration: Duration of exposure in seconds.
            Light: True for light frame, False for dark frame.

        Raises:
            InvalidValueException: If Duration is invalid, or if :py:attr:`BinX`,
                :py:attr:`BinY`, :py:attr:`NumX`, :py:attr:`NumY`, :py:attr:`StartX`,
                and :py:attr:`StartY` form an illegal combination.
            InvalidOperationException: If :py:attr:`CanAsymmetricBin` is False, yet
                :py:attr:`BinX` is not equal to :py:attr:`BinY`. TODO Is this right?
                Isn't this another combination of illegal *values*?
            NotConnectedException: If the device is not connected.
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device, *including
                reading the ImageReady property*.

        Notes:
            * **Asynchronous** (non-blocking): Use :py:attr:`ImageReady` 
              to determine if the exposure has been *successfully* 
              completed. See :ref:`async_faq`
            * Refer to :py:attr:`ImageReady` for additional info.
 
        """
        self._put("startexposure", Duration=Duration, Light=Light)

    def StopExposure(self) -> None:
        """Stop the current exposure, if any, and download the image data already acquired.
        
        Raises:
            NotImplementedException: If the camera cannot stop an in-progress exposure
                and save the already-acquired image data (:py:attr:`CanStopExposure` is False)
            NotConnectedException: If the device is not connected.
            InvalidOperationException: If not currently possible (e.g. during image download)
            DriverException: If the device cannot *successfully* complete the request. 
                This exception may be encountered on any call to the device.

        Notes:
            * Unlike :py:meth:`AbortExposure()` this method cuts an exposure short 
              while preserving the image data acquired so far, making it available 
              to the app.
            * If an exposure is in progress, the readout process is initiated. 
              Ignored if readout is already in process.
            * Will not raise an exception if the camera is already idle.
             
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
            response = httpx.get("%s/%s" % (self.base_url, attribute), params = pdata, headers = hdrs)
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
        raise NotImplementedException(m)
    elif n == 0x0401:
        raise InvalidValueException(m)
    elif n == 0x0402:
        raise ValueNotSetException(m)
    elif n == 0x0407:
        raise NotConnectedException(m)
    elif n == 0x0408:
        raise ParkedException(m)
    elif n == 0x0409:
        raise SlavedException(m)
    elif n == 0x040B:
        raise InvalidOperationException(m)
    elif n == 0x040c:
        raise ActionNotImplementedException(m)
    elif n >= 0x500 and n <= 0xFFF:
        raise DriverException(n, m)
    else:
        pass
