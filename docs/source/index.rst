..
    The rinohtype PDF builder I use chokes on right-justified images
    failing to wrap them with the text. It also chokes on the |xxx|
    format hyperlinks to externals that I use for opening in a separate
    tab. Therefore I have html and rinoh conditionals in these docs (typ)
    Don't ask me why I had to repeat the main title for html and rinoh
    separately....

.. only:: html

    .. image:: alpaca128.png
        :height: 92px
        :width: 128px
        :align: right

    ====================================
    Welcome to the Alpyca Client Library
    ====================================

.. only:: rinoh

    ====================================
    Welcome to the Alpyca Client Library
    ====================================

This document describes the Alpyca Client package for Python 3. The package provides all of the ASCOM Standard 
universal interfaces to astronomical devices using the Alpaca network protocol. As an application developer, your
usage of the various devices is simplified and universal, independent of the particular make/model of device.
For example, the same code can be used to control any ASCOM-compatible telescope. This includes not only 
telescopes that are controlled with classic ASCOM/COM on a Windows machine, but also any telescopes which
are *not* connected to a Windows machine, but instead speak Alpaca natively. The Windows ASCOM Remote 
middleware gives an Alpaca interface to any Windows-resident device, allowing you to use the device via 
this library from any platform on the net or local host.

.. only:: html

    For background see |about| on the |ascsite|. As an astronomy developer wanting to use Alpaca, we suggest 
    you look over |devhelp| join the |supforum|.

    .. Attention::
        Alpaca is not dependent on Windows. See |about|.

.. only:: rinoh

    For background see 
    `About Alpaca and ASCOM <https://ascom-standards.org/About/Index.htm>`_
    on the 
    `ASCOM Initiative web site <https://ascom-standards.org/index.htm>`_. 
    As an astronomy developer wanting to use Alpaca, we suggest 
    you look over 
    `Alpaca Developers Info <https://ascom-standards.org/AlpacaDeveloper/Index.htm>`_ and join the 
    `ASCOM Driver and Application Development Support Forum <https://ascomtalk.groups.io/g/Developer>`_.

    .. Attention::
        Alpaca is not dependent on Windows! See `About Alpaca and ASCOM <https://ascom-standards.org/About/Index.htm>`_.

.. |ascsite| raw:: html

    <a href="https://ascom-standards.org/index.htm" target="_blank">
    ASCOM Initiative web site</a> (external)

.. |about| raw:: html

    <a href="https://ascom-standards.org/About/Index.htm" target="_blank">
    About Alpaca and ASCOM</a> (external)

.. |devhelp| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Index.htm" target="_blank">
    Alpaca Developers Info</a> (external)

.. |supforum| raw:: html

    <a href="https://ascomtalk.groups.io/g/Developer" target="_blank">
    ASCOM Driver and Application Development Support Forum</a> (external)


.. toctree::
    :maxdepth: 2

    introduction

    alpacaclasses

    alpaca.exceptions

    alpaca.discovery

    alpaca.management

    faq

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
