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
    
Alpaca Device Server Management
===============================
Provides information about an Alpaca device server found via 
:doc:`alpaca.discovery`, and the devices which are provided by 
that server. For more information see the |apiref|. 

Example using the Management functions::

    svrs = discovery.search_ipv4()
    print(svrs)
    for svr in svrs:
        print(f"At {svr}")
        print (f"  V{management.apiversions(svr)} server")
        print (f"  {management.description(svr)['ServerName']}")
        devs = management.configureddevices(svr)
        for dev in devs:
            print(f"    {dev['DeviceType']}[{dev['DeviceNumber']}]: {dev['DeviceName']}")

Output::

    ['127.0.0.1:32323', '127.0.0.1:11111']
    At 127.0.0.1:32323
        V[1] server
        ASCOM Alpaca Simulators
            Camera[0]: Alpaca Camera Sim
            CoverCalibrator[0]: Alpaca CoverCalibrator Simulator
            Dome[0]: Alpaca Dome Sim
            FilterWheel[0]: Alpaca Filter Wheel Sim
            Focuser[0]: Alpaca Focuser Sim
            ObservingConditions[0]: Alpaca Observing Conditions Sim
            Rotator[0]: Alpaca Rotator Sim
            SafetyMonitor[0]: Alpaca SafetyMonitor Sim
            Switch[0]: Alpaca Switch V2 Sim
            Telescope[0]: Alpaca Telescope Sim
    At 127.0.0.1:11111
        V[1] server
        ASCOM Remote Server
            Rotator[0]: Rotator Simulator
            Telescope[0]: Telescope Simulator for .NET
            Focuser[0]: ASCOM Simulator Focuser Driver

.. |apiref| raw:: html

    <a href="https://github.com/ASCOMInitiative/ASCOMRemote/raw/master/Documentation/ASCOM%20Alpaca%20API%20Reference.pdf"
    target="_blank">Alpaca API Reference (PDF)</a> (external)

.. automodule:: alpaca.management
   :members:
   :undoc-members:
   :show-inheritance:
