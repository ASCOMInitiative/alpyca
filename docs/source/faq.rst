Frequently Asked Questions
==========================

.. _async_faq:

How can I tell if my asynchronous request failed after being started?
---------------------------------------------------------------------
All asynchronous (non-blocking) methods in ASCOM are paired with corresponding properties that
allow you to determine if the operation (running in the background) has finished. There are two
places where an async operation can fail:

1. When you call the method that starts the operation, for example 
   :py:meth:`Focuser.Move <alpaca.focuser.Focuser.Move>`. If you get an exception here, 
   it means the device couldn't *start* the operation, for whatever reason. Common
   reasons include an out-of-range request or an unconnected device.
2. Later you read the property that tells you whether the async operation has finished,
   for example :py:attr:`Focuser.IsMoving <alpaca.focuser.Focuser.IsMoving>`. If you see 
   the value change to indicate that the operation has finished, you can be *100% certain
   that it completed successfully*. On the other hand, if you get an exception here (usually
   a :py:class:`~alpaca.exceptions.DriverException`), it means the device *failed to finish the 
   operation successfully*. In this case, the device is compromsed and requires special attention.


.. _dome-faq:

The :doc:`Dome Interface <alpaca.dome>` seems complex and confusing. Help me do basic things.
---------------------------------------------------------------------------------------------

    [Q] **How can I tell if I'm connected to a roll-off roof or a "dumb" clamshell?**

    [A] Look for :py:attr:`~alpaca.dome.Dome.CanSetAzimuth` to be False. This means 
    that there is no way to move the opening to the sky at all. The only functions 
    available will be those related to opening and closing the roof or clamshell to
    provide access to the entire sky (or not).

    [Q] **How do I control a rotating dome with a simple shutter?**

    [A] If :py:attr:`~alpaca.dome.Dome.CanSetAltitude` is False, then you have a common
    dome with a rotatable opening (e.g., a slit). You can 
    :py:meth:`~alpaca.dome.Dome.SlewToAzimuth()` 
    to position the slit, and of course :py:meth:`~alpaca.dome.Dome.OpenShutter()` and 
    :py:meth:`CloseShutter()`. 

    [Q] **How can I adjust the location of the opening (slit, port, clamshell leaves) to 
    account for the geometry and offset of the optics?**

    [A] The Dome interface does not provide for this, as it requires current pointing
    information from the mount/telescope, as well as mount configuration and 
    measurements. This is a composite task requiring information about two devices, and
    is thus out of scope for a Dome device by itself. Your application is responsible
    for transforming the telescope alt/az to the alt/az needed for the dome.
    
    There are, however, a few integrated/combined telescope/mount/dome control systems (COMSOFT
    PC/TCS, DFM TCS, for example) which expose both :py:class:`~alpaca.telescope.Telescope` 
    and :py:class:`~alpaca.dome.Dome` interfaces. The slaving properties in the ASCOM
    Dome interface are provided for these types of control systems. 
