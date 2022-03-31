from alpaca.device import Device

class SafetyMonitor(Device):
    """ASCOM Standard ISafetyMonitor V1 Interface."""

    def __init__(
        self,
        address: str,
        device_number: int,
        protocol: str = "http"
    ):
        """Initialize SafetyMonitor object."""
        super().__init__(address, "safetymonitor", device_number, protocol)

    @property
    def IsSafe(self) -> bool:
        """Indicate whether the monitored state is safe for use.

        Returns:
            True if the state is safe, False if it is unsafe.
        
        """
        return self._get("issafe")
