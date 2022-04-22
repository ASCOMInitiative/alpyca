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

**Use Caution:**

Have a look at this article |excpdang|. While the article uses the C# language and acync/await
to illustrate the so-called "dangers" (failing to await), the exact same principles apply here.
In the example above, you really must use IsMoving to determine completion. It is the 'await'
in this cross-language/cross-platform environment. Iff you ignore IsMoving and instead 
“double-check” the results by comparing your request with the results, you run several risks

1. A lost exception (an integrity bust),
2. a false completion indication if the device passes through the requested 
   position on its way to settling to its final place, and 
3. needing to decide what “close enough” means. 

Plus it needlessly complicates your code. We have to design for, and require, 
trustworthy devices/drivers.

.. |excpdang| raw:: html

    <a href="https://medium.com/@alexandre.malavasi/why-exceptions-in-async-methods-are-dangerous-in-c-fda7d382b0ff" 
    target="_blank">
    Why exceptions in async methods are “dangerous” in C#</a> (external)


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

.. _ptgstate-faq:

What is the meaning of "pointing state" in the docs for Telescope.SideOfPier?
-----------------------------------------------------------------------------

In the docs for :py:attr:`Telescope.SideOfPier <alpaca.telescope.Telescope.SideOfPier>` and
:py:meth:`Telescope.DestinationSideOfPier() <alpaca.telescope.Telescope.DestinationSideOfPier>`,
for historical reasons, the name ``SideOfPier`` does not reflect its true meaning. 
The name will *not* be changed (so as to preserve compatibility), 
but the meaning has since become clear. *All* conventional mounts (German, fork, etc) have two 
pointing states for a given equatorial (sky) position. Mechanical limitations often make it 
impossible for the mount to position the optics at given HA/Dec in one of the two pointing states, 
but there are places where the same point can be reached sensibly in both pointing states 
(e.g. near the pole and close to the meridian). In order to understand these pointing states, 
consider the following (thanks to TPOINT author Patrick Wallace for this info):

All conventional telescope mounts have two axes nominally at right angles. For an equatorial, 
the longitude axis is mechanical hour angle and the latitude axis is mechanical declination. 
Sky coordinates and mechanical coordinates are two completely separate arenas. This becomes 
rather more obvious if your mount is an altaz, but it's still true for an equatorial. 
Both mount axes can in principle move over a range of 360 deg. This is distinct from sky 
HA/Dec, where Dec is limited to a 180 deg range (+90 to -90). Apart from practical limitations, 
any point in the sky can be seen in two mechanical orientations. To get from one to the other 
the HA axis is moved 180 deg and the Dec axis is moved through the pole a distance twice the 
sky codeclination (90 - sky declination).

Mechanical zero HA/Dec will be one of the two ways of pointing at the intersection of the 
celestial equator and the local meridian. In order to support Dome slaving, where it is 
important to know which side of the pier the mount is actually on, ASCOM has adopted the 
convention that the Normal pointing state will be the state where a German Equatorial mount 
is on the East side of the pier, looking West, with the counterweights below the optical 
assembly and that pierEast will represent this pointing state.

Move your scope to this position and consider the two mechanical encoders zeroed. The two 
pointing states are, then: 

+-------------------------------+-------------------------------------------------------------+
| **Normal** (pierEast)         | Where the mechanical Dec is in the range -90 deg to +90 deg |
+-------------------------------+-------------------------------------------------------------+
|**Beyond the pole** (pierWest) | Where the mechanical Dec is in the range -180 deg to -90    |
+-------------------------------+                                                             |
|                               | deg or +90 deg to +180 deg                                  |
+-------------------------------+-------------------------------------------------------------+

"Side of pier" is a *consequence* of the former definition, not something fundamental. 
Apart from mechanical interference, the telescope can move from one side of the pier to 
the other without the mechanical Dec having changed: you could track Polaris forever 
with the telescope moving from west of pier to east of pier or vice versa every 12h. 
Thus, "side of pier" is, in general, not a useful term (except perhaps in a loose, 
descriptive, explanatory sense). All this applies to a fork mount just as much as to a 
GEM, and it would be wrong to make the "beyond pole" state illegal for the former. 
Your mount may not be able to get there if your camera hits the fork, but it's 
possible on some mounts. Whether this is useful depends on whether you're in 
Hawaii or Finland.

To first order, the relationship between sky and mechanical HA/Dec is as follows:

**Normal state**

    * HA_sky = HA_mech
    * Dec_sky = Dec_mech

**Beyond the pole**

    * HA_sky = HA_mech + 12h, expressed in range ± 12h
    * Dec_sky = 180d - Dec_mech, expressed in range ± 90d

Astronomy software often needs to know which which pointing state the mount is in. 
Examples include setting guiding polarities and calculating dome opening azimuth/altitude. 
The meaning of the :py:attr:`Telescope.SideOfPier <alpaca.telescope.Telescope.SideOfPier>` 
property, then is: 

+--------------+--------------------------------+
| **pierEast** | Normal pointing state          |
+--------------+--------------------------------+
| **pierWest** | Beyond the pole pointing state |
+--------------+--------------------------------+

If the mount hardware reports neither the true pointing state (or equivalent) nor the mechanical 
declination axis position (which varies from -180 to +180), a driver cannot calculate the 
pointing state, and *must not* implement SideOfPier. If the mount hardware reports only the 
mechanical declination axis position (-180 to +180) then a driver can calculate 
SideOfPier as follows: 

    * **pierEast** = abs(mechanical dec) <= 90 deg
    * **pierWest** = abs(mechanical Dec) > 90 deg

It is allowed (though not required) that SideOfPier may be written to force the mount to flip. 
Doing so, however, may change the right ascension of the telescope. During flipping, 
Telescope.Slewing must return True.

Pointing State and Side of Pier - Help for Driver Developers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A further document published on the ASCOM website, `Pointing State and Side of Pier 
<https://download.ascom-standards.org/docs/SideOfPier(1.2).pdf>`_ (PDF), is also
installed in the Developer Documentation folder by the ASCOM Developer Components 
installer. This further explains the pointing state concept and includes 
diagrams illustrating how it relates to physical side of pier for German equatorial 
telescopes. It also includes details of the tests performed by Conform to determine 
whether the driver correctly reports the pointing state as defined above.




