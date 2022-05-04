..
    The rinohtype PDF builder I use chokes on right-justified images
    failing to wrap them with the text. It also chokes on the |xxx|
    format hyperlinks to externals that I use for opening in a separate
    tab. Therefore I have html and rinoh conditionals in these docs (typ)
    
.. only:: html

    .. image:: alpaca128.png
        :height: 92px
        :width: 128px
        :align: right
        
Frequently Asked Questions
==========================

.. _async_faq:

How can I tell if my asynchronous request failed after being started?
---------------------------------------------------------------------
See :ref:`intro-stat`

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

.. caution::

    .. only:: html
        
        Have a look at this article |excpdang|. While the article uses the C# language and acync/await
        to illustrate the so-called "dangers" (failing to await), the exact same principles apply here.
        In the example above, you really must use 
        :py:attr:`Focuser.IsMoving <alpaca.focuser.Focuser.IsMoving>`
        to determine completion. It is the 'await'
        in this cross-language/cross-platform environment. If you ignore 
        :py:attr:`Focuser.IsMoving <alpaca.focuser.Focuser.IsMoving>` and instead 
        “double-check” the results by comparing your request with the results, you run several risks

    .. only:: rinoh

        Have a look at this article
        `Why exceptions in async methods are “dangerous” in C# <https://medium.com/@alexandre.malavasi/why-exceptions-in-async-methods-are-dangerous-in-c-fda7d382b0ff>`_. 
        While the article uses the C# language and acync/await
        to illustrate the so-called "dangers" (failing to await), the exact same principles apply here.
        In the example above, you really must use 
        :py:attr:`Focuser.IsMoving <alpaca.focuser.Focuser.IsMoving>`
        to determine completion. It is the 'await'
        in this cross-language/cross-platform environment. If you ignore 
        :py:attr:`Focuser.IsMoving <alpaca.focuser.Focuser.IsMoving>` and instead 
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

What is the meaning of "pointing state" in the docs for SideOfPier?
-------------------------------------------------------------------

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

.. _dsop-faq:

What is DestinationSideOfPier and why would I want to use it?
-----------------------------------------------------------------------

The :py:attr:`DestinationSideOfPier <alpaca.telescope.Telescope.DestinationSideOfPier>`
property is provided for applications to manage pier flipping during automated image sequences.
Basically you provide it with an RA and Dec, and it comes back telling you the pointing state 
:py:attr:`SideOfPier <alpaca.telescope.Telescope.SideOfPier>` that would result 
from a slew-to *at the 
present time*. Looking at the current SideOfPier and DestinationSideOfPier tells you if the mount 
would flip on a slew to those coordinates. This info is based on the given RA/Dec at the given 
time, so is not a static function.  

The mount knows where all of its settings are, how they  are applied, and what their effects are. 
All it needs to do is tell the app the outcome of a slew to a point. Obviously if trash RA/Dec 
are given the mount would raise an exception for invalid coordinates.

As your image sequence progresses, at the beginning of each image you add the exposure interval 
to the RA (RA is a time coordinate, right?) and if you're really picky adjust by the 0.27% 
difference from sidereal to solar time, then call DestinationSideOfPier(RA + image, Dec). 
If it tells you the flip point will be reached before the end of the exposure, then you have 
some choices to make:

1. Will the mount track past the flip point far enough to allow the image to proceed "from here" 
   and complete, so you could do the flip at the end while the image downloads?
2. If the mount is hard limited at the flip point then you would have to wait until the target 
   drifts past the flip point, flip, then proceed. Not many mounts are hard limited against tracking 
   past their flip points.

The tricky parts are

1. For #1 above, knowing whether, and how far, the mount can track past its flip point. My own 
   experience is that most German mounts can track at least one "typical" exposure interval past 
   their flip points. In the old days this would be 1800 seconds for  grungy CCDs with bad read 
   noise and narrowband filter, but nowadays, especially with CMOS, even narrowband exposures 
   are significantly shorter. Even at the celestial equator, 1800 seconds is only 7.5 degrees, 
   and less as declination increases (by cos(dec)). Tracking 7.5 degrees or less past a flip 
   point seems within the capability of most GEMs. Also, if you can image past the flip 
   point, you can download the image in parallel with flipping the mount, so the penalty 
   for flipping is the flip time minus the image download time.
2. For #2 above, how long to wait before flipping? To handle this, stop tracking for safety, 
   then periodically call DestinationSideOfPier(RA, Dec) for your target's coordinates 
   while the target itself drifts towards, then past, the flip point (which  you don't 
   know but who cares?).  Wait until it tells you that the mount will flip. 
   Turn on tracking, slew to your target, the mount will flip, and off you go toward 
   the west with your image sequence.

.. _moveaxis-faq:

What does MoveAxis() do and how do I use it?
--------------------------------------------

This method supports control of the mount about its mechanical axes. Upon successful return, 
the telescope will start moving at the specified rate about the specified axis and continue 
*indefinitely*. This method must be called for each axis separately. The axis motions may run 
concurrently, each at their own rate. Set the rate for an axis to zero to restore the motion 
about that axis to the rate set by the :py:attr:`TrackingRate` property. 
Tracking motion (if enabled) is suspended during this mode of operation.

**Notes:**

* The movement rate must be within the value(s) obtained from a 
  :py:class:`~alpaca.telescope.Rate` object in the
  :py:meth:`~alpaca.telescope.Telescope.AxisRates()` list for the desired axis. 
* The rate is a signed value with negative rates moving in the oposite direction to 
  positive rates.
* The values specified in 
  :py:meth:`~alpaca.telescope.Telescope.AxisRates()` are absolute, unsigned values and apply 
  to both directions, determined by the sign used in this command.
* The value of :py:attr:`~alpaca.telescope.Telescope.Slewing` will be True if the 
  mount is moving about any of its 
  axes as a result of this method being called. This can be used to simulate a handbox 
  by initiating motion with the MouseDown event and stopping the motion with the 
  MouseUp event.
* When the motion is stopped by setting the rate to zero the mount will be set to the 
  previous 
  :py:attr:`~alpaca.telescope.Telescope.TrackingRate` or to no movement, 
  depending on the state of the 
  :py:attr:`~alpaca.telescope.Telescope.Tracking` property.
* It may be possible to implement satellite tracking by using the 
  :py:meth:`~alpaca.telescope.Telescope.MoveAxis()` method to 
  move the scope in the required manner to track a satellite.



