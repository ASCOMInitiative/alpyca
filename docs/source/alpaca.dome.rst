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

.. module:: alpaca.dome
.. autoclass:: Dome
    :members:
    :inherited-members:

Dome-Related Constants
----------------------
.. autoenum:: ShutterState
    :members:
