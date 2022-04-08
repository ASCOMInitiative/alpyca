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
img = c.ImageArray
imginfo = c.ImageArrayInfo          # These lists are alwats 32 bit int
if imginfo.Rank == 2:
    #nda = np.array(img).transpose()     # TODO ?? Data Types and 3-D array ??
    nda = np.array(img).transpose()      # TODO ?? Data Types and 3-D array ??
else:
    nda = np.array(img)

hdu = fits.PrimaryHDU(nda)
hdu.writeto('C:/Users/Robert B. Denny/Desktop/test.fts', overwrite=True)
c.Connected = False

print("done")