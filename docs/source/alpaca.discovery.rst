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

Alpaca Device Server Discovery
==============================
This module provides Alpaca device server discovery service. Search your
local network segment (or VLAN) for Alpaca device *servers*, returning
a list consisting of ``ipaddress:port`` strings for each one found.
Each Alpaca device server may provide access to multiple Alpaca device
types, and multiple Alpaca devices of a given type.

.. Note::
    Use the :doc:`alpaca.management` functions to learn the details of
    the served device(s). See the example there.

Example::

    from alpaca import discovery

    svrs = discovery.search_ipv4()  # Note there is an IPv6 function as well
    print(svrs)

Output::

    ['127.0.0.1:32323', '192.168.1.12:11111', '192.168.1.31:11111']

This example shows one Alpaca server on the local host, two Alpaca servers
on the LAN.

.. automodule:: alpaca.discovery
   :members:
   :undoc-members:
   :show-inheritance:
