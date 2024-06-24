Camera Class
============
.. admonition:: Master Interfaces Reference
    :class: green

    These green boxes in each interface member each have a link to the
    corresponding member definition in the |master|. The information in this
    Alpyca document is provided *for your convenience*. If there is any question,
    the info in |master| is the official specification.

.. Note::

    See the :ref:`Example` below.

.. the |master| link is in device.py and thus is accessible to all of the device
   specific document contexts.

.. module:: alpaca.camera
.. autoclass:: Camera
    :members:
    :inherited-members:

ImageMetadata Class
-------------------
.. autoclass:: ImageMetadata
    :members:

Camera-Related Constants
------------------------
.. autoenum:: CameraStates
    :members:
.. autoenum:: SensorType
    :members:
.. autoenum:: ImageArrayElementTypes
    :members:

.. _Example:

Example: Acquiring an Image, Creating FITS Image
------------------------------------------------

Using numpy and astropy.io.fits, connect to an Alpaca Camera,
acquire a short image, download and make a local FITS file::

    import os
    import time
    import array
    from alpaca.camera import *     # Sorry Python purists, this has multiple required Classes
    import numpy as np
    import astropy.io.fits as fits

    #
    # Set up the camera
    #
    c = Camera('localhost:32323', 0)    # Connect to the ALpaca Omni Simulator
    c.Connected = True
    c.BinX = 1
    c.BinY = 1
    # Assure full frame after binning change
    c.StartX = 0
    c.StartY = 0
    c.NumX = c.CameraXSize // c.BinX    # Watch it, this needs to be an int (typ)
    c.NumY = c.CameraYSize // c.BinY
    #
    # Acquire a light image, wait while printing % complete
    #
    c.StartExposure(2.0, True)
    while not c.ImageReady:
        time.sleep(0.5)
        print(f'{c.PercentCompleted}% complete')
    print('finished')
    #
    # OK image acquired, grab the image array and the metadata
    #
    img = c.ImageArray
    imginfo = c.ImageArrayInfo
    if imginfo.ImageElementType == ImageArrayElementTypes.Int32:
        if c.MaxADU <= 65535:
            imgDataType = np.uint16 # Required for BZERO & BSCALE to be written
        else:
            imgDataType = np.int32
    elif imginfo.ImageElementType == ImageArrayElementTypes.Double:
        imgDataType = np.float64
    #
    # Make a numpy array of he correct shape for astropy.io.fits
    #
    if imginfo.Rank == 2:
        nda = np.array(img, dtype=imgDataType).transpose()
    else:
        nda = np.array(img, dtype=imgDataType).transpose(2,1,0)
    #
    # Create the FITS header and common FITS fields
    #
    hdr = fits.Header()
    hdr['COMMENT'] = 'FITS (Flexible Image Transport System) format defined in Astronomy and'
    hdr['COMMENT'] = 'Astrophysics Supplement Series v44/p363, v44/p371, v73/p359, v73/p365.'
    hdr['COMMENT'] = 'Contact the NASA Science Office of Standards and Technology for the'
    hdr['COMMENT'] = 'FITS Definition document #100 and other FITS information.'
    if imgDataType ==  np.uint16:
        hdr['BZERO'] = 32768.0
        hdr['BSCALE'] = 1.0
    hdr['EXPOSURE'] = c.LastExposureDuration
    hdr['EXPTIME'] = c.LastExposureDuration
    hdr['DATE-OBS'] = c.LastExposureStartTime
    hdr['TIMESYS'] = 'UTC'
    hdr['XBINNING'] = c.BinX
    hdr['YBINNING'] = c.BinY
    hdr['INSTRUME'] = c.SensorName
    try:
        hdr['GAIN'] = c.Gain
    except:
        pass
    try:
        hdr['OFFSET'] = c.Offset
        if type(c.Offset == int):
            hdr['PEDESTAL'] = c.Offset
    except:
        pass
    hdr['HISTORY'] = 'Created using Python alpyca-client library'
    #
    # Create the final FITS from the numpy array and FITS info
    #
    hdu = fits.PrimaryHDU(nda, header=hdr)

    img_file = f"{os.getenv('USERPROFILE')}/Desktop/test.fts"
    hdu.writeto(img_file, overwrite=True)
    c.Connected = False

    print("Booyah! Your FITS image is ready.")

Resulting FITS header::

    Header listing for HDU #1:
    SIMPLE  =                    T / conforms to FITS standard
    BITPIX  =                   16 / array data type
    NAXIS   =                    2 / number of array dimensions
    NAXIS1  =                 1280
    NAXIS2  =                 1024
    EXPOSURE=            2.0052547
    EXPTIME =            2.0052547
    DATE-OBS= '2022-04-15T18:20:50'
    TIMESYS = 'UTC     '
    XBINNING=                    1
    YBINNING=                    1
    INSTRUME= 'MyCamera'
    BSCALE  =                    1
    BZERO   =                32768
    COMMENT FITS (Flexible Image Transport System) format defined in Astronomy and
    COMMENT Astrophysics Supplement Series v44/p363, v44/p371, v73/p359, v73/p365.
    COMMENT Contact the NASA Science Office of Standards and Technology for the
    COMMENT FITS Definition document #100 and other FITS information.
    HISTORY Created using Python alpyca-client library
    END
