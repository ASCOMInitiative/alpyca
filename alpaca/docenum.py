from enum import IntEnum
class DocIntEnum(IntEnum):
    """Used to provide textual documentation for Enum classes
    
    Example:
        ::

            class CameraStates(DocIntEnum):
                \"\"\"Current condition of the Camera\"\"\"
                cameraIdle      = 0, 'Inactive'
                cameraWaiting   = 1, 'Waiting for ??'
                cameraExposing  = 2, 'Acquiring photons'
                cameraReading   = 3, 'Reading from the sensor'
                cameraDownload  = 4, 'Downloading the image data'
                cameraError     = 5, 'An error condition exists'

    References
        https://stackoverflow.com/questions/50473951/how-can-i-attach-documentation-to-members-of-a-python-enum/50473952#50473952

    """
    def __new__(cls, value, doc=None):
        self = int.__new__(cls, value)  # calling super().__new__(value) here would fail
        self._value_ = value
        if doc is not None:
            self.__doc__ = doc
        return self
