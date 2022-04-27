Discovery
=========
Provides device discovery service. Search your local network segment (or VLAN) for Alpaca device
*servers*, returning a list of ``ipaddress:port`` strings for each one found. 
Each Alpaca device server may provide access to multiple Alpaca device types,
and multiple Alpaca devices of a given type. Use the :py:mod:`alpaca.management` functions to access the
details of the served device(s).

Example::

    from alpaca.import discovery

    svrs = discovery.search_ipv4()
    print(svrs)

Output::

    ['127.0.0.1:32323', '192.168.1.12:11111', '192.168.1.31:11111']

This example shows one Alpaca server on the local host, two Alpaca servers on the LAN.

.. automodule:: alpaca.discovery
   :members:
   :undoc-members:
   :show-inheritance:
