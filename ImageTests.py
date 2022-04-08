import os
import time
import array
from alpaca.camera import *
import numpy as np
import astropy.io.fits as fits

c = Camera('localhost:32323', 0)
c.Connected = True
c.BinX = 1 
c.BinY = 1
c.StartX = 0
c.StartY = 0
c.NumX = c.CameraXSize // c.BinX    # Watch it, this needs to be an int (typ)
c.NumY = c.CameraYSize // c.BinY
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
#
# Create the final FITS from the numpy array and FITS info
#
hdu = fits.PrimaryHDU(nda, header=hdr)
hdr['HISTORY'] = 'Created by ImageTests.py using Python alpyca-client library'

img_file = f"{os.getenv('USERPROFILE')}/Desktop/test.fts"
hdu.writeto(img_file, overwrite=True)
c.Connected = False

print("done")