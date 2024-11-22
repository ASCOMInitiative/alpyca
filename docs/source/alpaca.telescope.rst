Telescope Class
===============
.. admonition:: Master Interfaces Reference
    :class: green

    .. only:: html

        These green boxes in each interface member each have a link to the
        corresponding member definition in |MasterTelescope|. The information in this
        Alpyca document is provided *for your convenience*. If there is any question,
        the info in |master| is the official specification.

        .. |MasterTelescope| raw:: html

            <a href="https://ascom-standards.org/newdocs/telescope.html" target="_blank">
            Master ITelescopeV4 Interface</a> (external)

    .. only:: rinoh

        These green boxes in each interface member each have a link to the
        corresponding member definition in the `Master ITelescopev4 Interface
        <https://ascom-standards.org/newdocs/telescope.html>`_ document. The information in this
        Alpyca document is provided *for your convenience*. If there is any
        question, the info in `ASCOM Master Interfaces
        <https://ascom-standards.org/newdocs/>`_ is the official specification.

.. the |master| link is in device.py and thus is accessible to all of the device
   specific document contexts.

.. module:: alpaca.telescope
.. autoclass:: Telescope
    :members:
    :inherited-members:

Rate Class
----------
.. autoclass:: Rate
    :members:

Telescope-Related Constants
---------------------------
.. autoenum:: AlignmentModes
    :members:
.. autoenum:: DriveRates
    :members:
.. autoenum:: EquatorialCoordinateType
    :members:
.. autoenum:: GuideDirections
    :members:
.. autoenum:: PierSide
    :members:
.. autoenum:: TelescopeAxes
    :members:
