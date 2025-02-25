ASCOM Alpaca Exception Classes
==============================
    These exception classes are defined in the
    `Alpaca API Reference <https://ascom-standards.org/AlpacaDeveloper/ASCOMAlpacaAPIReference.html>`_
    and `ASCOM Master Interfaces (Alpaca and COM) <https://ascom-standards.org/newdocs/>`_
    on the ASCOM main web site.

Exception Characteristics
-------------------------
    When these ASCOM Alpaca specific exceptions are raised by the device, the
    internal logic reconstructs them as Python exceptions from the incoming
    device response JSON. Thus you get the same exceptions by name and value as
    defined in the ASCOM API.

**Internal Arguments**
    It's common to access the message of a built-in Python exception as provided
    by ``catch ex:`` as an ``ex.args`` array. These custom exceptions define
    ``ex.args[0]`` as the error number and ``ex.args[1]`` as the error message.

**Properties**
    The exceptions not only have number and message attributes like built-in
    Python exception objects, but they also have ``number`` and ``message``
    properties. Within an exception as provided by a ``catch ex:`` you can get
    the error number as ``ex.number`` and the error message as ``ex.message``.

**String Conversion**
    Like built-in Python exceptions, you can print out the exception parts via
    ``str(ex)`` which produces a string with the the error message then the
    error number in parentheses. For example, a ``DriverException`` with code
    ``0x506``:

    ``Datalink connect failure (Error Code: 0x506)``

    As usual you can get the exception name via ``type(ex).__name__``.

**Default Uncaught Exceptions**

    Like built-in Python exceptions, the console output for uncaught exceptions
    prints the name of the exception and its error number and message as
    formatted by ``str(ex)``, for example:

    ``alpaca.exceptions.DriverException: Datalink connect failure (Error Code: 0x506)``

Exception Definitions
---------------------

.. automodule:: alpaca.exceptions
   :members:
   :undoc-members:
   :show-inheritance:
