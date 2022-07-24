Rotator Class
=============
The Rotator V3 interface provides for a common offset between its mechanical
angle, plus the angle at which an attached imager may be mounted, and the
equatorial  position angle (PA) on the sky. By calling
:py:meth:`~alpaca.rotator.Rotator.Sync()` with a known current PA (from plate
solving etc.), you can cause the rotator (and imager) to work in PA for you
as well as other apps that might be using the rotator.

.. module:: alpaca.rotator
.. autoclass:: Rotator
    :members:
    :inherited-members:
