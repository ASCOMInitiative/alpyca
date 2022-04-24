Introduction and Quick Start
============================
This package provides access to ASCOM compatible astronomy devices via the Alpaca network protocol. 
For more information see the |ascsite|, specifically the |devhelp| section, and the |apiref|.

.. _intro-stat:

Status of This Document
-----------------------
The descriptions of the ASCOM Standard interfaces implemented in Alpyca Client are 
our best efforts as of May 2022. At that time, the ASCOM Core Team announced that 
they are formalizing the operation of the non-blocking (asynchronous) methods 
in the standards documentation. This library manual includes additional information 
and clarification of the asynchronous methods which follows the formal specification 
changes as of that time. If there are any significant changes, we will release an 
updated (compatible) library as soon as  possible. We wanted to get you started 
in the right direction!

Member Capitalization
---------------------
This help file provides detailed descripions of the ASCOM Interfaces for all supported device types.
Note that, rather than follow :pep:`8`, the method and property names, as well as enumerations 
and exceptions, all follow the capitalization that has historically been assigned to ASCOM
interface members. The Class and member descriptions, notes, and exceptions raised all 
follow the universal ASCOM standards established long ago.

Numeric Datatypes
-----------------
The Alpyca Client library takes care of numeric conversions so you always work in native 
Python numbers. When comparing numeric datatypes here in Python 3, keep the following in mind:

* Python 3's ``float`` is equivalent to a double-precision floating point in other languages 
  (e.g. ``double`` in C#, 64-bit)
* Python 3's ``int`` is not restricted by the number of bits, and can expand to the limit 
  of available memory.

Example::

    # A Python 3 program to demonstrate that we can store
    # large numbers in Python 3
    x = 10000000000000000000000000000000000000000000
    x = x + 1
    print (x)
Output::

    10000000000000000000000000000000000000000001
 
Common Misconceptions and Confusions
------------------------------------
Throughout the evolution of ASCOM, and particularly recently with Alpaca, our goal has been to
provide a strong framework for reliability and integrity. We see newcomers to programming 
looking for help on the |supforum|. There are a few subject areas within which misconceptions
and confusion are common. Before starting an application development project with Alpyca Client,
you may benefit from reviewing the following design principles that are *foundational*:

* |princ|
* |async|
* |excep|

.. |ascsite| raw:: html

    <a href="https://ascom-standards.org/index.htm" target="_blank">
    ASCOM Initiative web site</a> (external)

.. |devhelp| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Index.htm" target="_blank">
    Alpaca Developers</a> (external)

.. |apiref| raw:: html

    <a href="https://github.com/ASCOMInitiative/ASCOMRemote/raw/master/Documentation/ASCOM%20Alpaca%20API%20Reference.pdf"
    target="_blank">Alpaca API Reference (PDF)</a> (external)

.. |supforum| raw:: html

    <a href="https://ascomtalk.groups.io/g/Developer" target="_blank">
    ASCOM Driver and Application Development Support Forum</a> (external)

.. |princ| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Principles.htm" target="_blank">
    The General Principles</a> (external)

.. |async| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Async.htm" target="_blank">
    Asynchronous APIs</a> (external)

.. |excep| raw:: html

    <a href="https://ascom-standards.org/AlpacaDeveloper/Exceptions.htm" target="_blank">
    Exceptions in ASCOM</a> (external)




