Rotator Class
=============
The Rotator V3 interface provides for a common offset between its mechanical
angle, plus the angle at which an attached imager may be mounted, and the
equatorial  position angle (PA) on the sky. By calling
:meth:`~alpaca.rotator.Rotator.Sync()` with a known current PA (from plate
solving etc.), you can cause the rotator (and imager) to work in PA for you
as well as other apps that might be using the rotator.

.. admonition:: Master Interfaces Reference
    :class: green

    .. only:: html

        These green boxes in each interface member each have a link to the
        corresponding member definition in |MasterRotator|. The information in this
        Alpyca document is provided *for your convenience*. If there is any question,
        the info in |master| is the official specification.

        .. |MasterRotator| raw:: html

            <a href="https://ascom-standards.org/newdocs/rotator.html" target="_blank">
            Master IRotatorV4 Interface</a> (external)

    .. only:: rinoh

        These green boxes in each interface member each have a link to the
        corresponding member definition in the `Master IRotatorv4 Interface
        <https://ascom-standards.org/newdocs/rotator.html>`_ document. The information in this
        Alpyca document is provided *for your convenience*. If there is any
        question, the info in `ASCOM Master Interfaces
        <https://ascom-standards.org/newdocs/>`_ is the official specification.

.. the |master| link is in device.py and thus is accessible to all of the device
   specific document contexts.

.. module:: alpaca.rotator
.. autoclass:: Rotator
    :members:
    :inherited-members:
