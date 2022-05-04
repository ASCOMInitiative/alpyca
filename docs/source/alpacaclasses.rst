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
        
ASCOM Alpaca Device Classes
===========================
Each of these Classes implements the properties, methods, exceptions, and enumerated
constants of the corresponding ASCOM device interface.

.. toctree::
   :maxdepth: 4

   alpaca.camera
   alpaca.covercalibrator
   alpaca.dome
   alpaca.filterwheel
   alpaca.focuser
   alpaca.observingconditions
   alpaca.rotator
   alpaca.safetymonitor
   alpaca.switch
   alpaca.telescope
   alpaca.device
