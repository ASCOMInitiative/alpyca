:orphan:

Device Superclass
=================
This contains methods and properties that are shared by all ASCOM/Alpaca classes. 
Note that the \:orphan\: tag above prevents warnings as this is not an any toctree.
Its members appear within the classes for which this is a superclass.

The low-level HTTP I/O uses `HTTPX A next-generation *requests*-compatible 
HTTP client for Python <https://www.python-httpx.org/>`_ 
which supports async/await and optionally HTTP/2.0, both of which are included for future upgrades. If your 
app does HTTP requests, you can use the included *HTTPX* instead of the more common *requests*, and you
already have support for async/await on the HTTP requests.

.. module:: alpaca.device
.. autoclass:: Device
    :members:
    :undoc-members:
    :noindex:

    