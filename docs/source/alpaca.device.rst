:orphan:

Device Superclass
=================
This contains methods and properties that are shared by all ASCOM/Alpaca classes. 
Its members appear within the ASCOM/Alpaca class documentation as well as here.

In addition, this class contains the low-level HTTP I/O used to communicate within
Alpaca devices. Rather than using the traditional Python *requests* library, Alpyca
uses `HTTPX A next-generation *requests*-compatible 
HTTP client for Python <https://www.python-httpx.org/>`_ 
which supports async/await and optionally HTTP/2.0, both of which are included for future upgrades. If your 
app does HTTP requests itself, you can use the included *HTTPX* instead of the more common *requests*, and you
already have support for async/await on the HTTP requests.

.. module:: alpaca.device
.. autoclass:: Device
    :members:
    :undoc-members:
    :noindex:

    