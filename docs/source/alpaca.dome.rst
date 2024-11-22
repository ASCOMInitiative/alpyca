Dome Class
==========
The Dome interface is designed to provide an enclosure-independent way of
managing access to the sky for the telescope within. Enclosures vary
widely in their design, with roll-off roofs and classic rotating domes
being only two of the possibilities.

Thus, this interface focuses on providing the telescope with access to the
sky at a given sky location specified by alt/az coordinates. For additional
help, see :ref:`dome-faq`  For some history, see the |xxx|

.. |xxx| raw:: html

    <a href="https://ascom-standards.org/Initiative/History.htm#domehist" target="_blank">
    Dome Interface Standard in the History of ASCOM and Alpaca Development</a> (external)

.. admonition:: Master Interfaces Reference
    :class: green

    .. only:: html

        These green boxes in each interface member each have a link to the
        corresponding member definition in |MasterDome|. The information in this
        Alpyca document is provided *for your convenience*. If there is any question,
        the info in |master| is the official specification.

        .. |MasterDome| raw:: html

            <a href="https://ascom-standards.org/newdocs/dome.html" target="_blank">
            Master IDomeV3 Interface</a> (external)

    .. only:: rinoh

        These green boxes in each interface member each have a link to the
        corresponding member definition in the `Master IDomeV3 Interface
        <https://ascom-standards.org/newdocs/dome.html>`_ document. The information in this
        Alpyca document is provided *for your convenience*. If there is any
        question, the info in `ASCOM Master Interfaces
        <https://ascom-standards.org/newdocs/>`_ is the official specification.

.. the |master| link is in device.py and thus is accessible to all of the device
   specific document contexts.

.. module:: alpaca.dome
.. autoclass:: Dome
    :members:
    :inherited-members:

Dome-Related Constants
----------------------
.. autoenum:: ShutterState
    :members:
