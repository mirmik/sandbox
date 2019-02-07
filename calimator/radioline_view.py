#!/usr/bin/env python3
#coding: utf-8

'''
======================
3D surface (color map)
======================

Demonstrates plotting a 3D surface colored with the coolwarm color map.
The surface is made opaque by using antialiased=False.

Also demonstrates using the LinearLocator and custom formatting for the
z axis tick labels.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

from pprint import pprint
from hexdump import hexdump

def window(arr, size, coords):
	assert(size[0] % 2)
	assert(size[1] % 2)
	xd = int(size[0] / 2)
	yd = int(size[1] / 2)

	xmin = coords[0] - xd
	xmax = coords[0] + xd

	ymin = coords[1] - yd
	ymax = coords[1] + yd

	if xmin < 0: xmin = 0 
	if xmax >= arr.shape[0]: xmax = arr.shape[0] - 1

	if ymin < 0: ymin = 0 
	if ymax >= arr.shape[1]: ymax = arr.shape[1] - 1

	wnd = arr[xmin:xmax+1, ymin:ymax+1]

	return wnd

file = open('ocont3d_4.dat', 'rb')

sect1 = file.read(512)
sect2 = file.read(10240)
sect3 = file.read(1024)

completed = bool(sect3[0:1])
infoformed = bool(sect3[1:2])
cdim = int.from_bytes(sect3[10*4: 11*4], byteorder='little')
ndim = int.from_bytes(sect3[11*4: 12*4], byteorder='little')
fdim = int.from_bytes(sect3[12*4: 13*4], byteorder='little')
transposed = int.from_bytes(sect3[14*4: 14*4 + 1], byteorder='little')

fcoords_sect = file.read(fdim * 8) 
ccoords_sect = file.read(cdim * 8) 
ncoords_sect = file.read(ndim * 8)
data_sect = file.read(cdim*ndim*fdim * 8 * 2)

print("completed: {}".format(completed))
print("infoformed: {}".format(infoformed))
print("transposed: {}".format(transposed))
print("cdim: {}".format(cdim))
print("ndim: {}".format(ndim))
print("fdim: {}".format(fdim))

#print("ccoords_sect:")
#hexdump(ccoords_sect)

#print("ncoords_sect:")
#hexdump(ncoords_sect)

fcoords = np.fromstring( fcoords_sect, np.float64 )
print("fcoords:")
print(fcoords)

ccoords = np.fromstring( ccoords_sect, np.float64 )
print("ccoords:")
print(ccoords)

ncoords = np.fromstring( ncoords_sect, np.float64 )
print("ncoords:")
print(ncoords)

data = np.fromstring( data_sect, np.float64 ).reshape((cdim*fdim*ndim,2))

np.set_printoptions(threshold=np.nan)

amp = data[:,0]
amp = amp.reshape((cdim, ndim))

for c in range(0, cdim):
	for n in range(0, ndim):
		if amp[c,n] >= 418:
			amp[c,n] = np.median(window(amp, size=(15,15), coords=(c,n)))

print("amp:")
print(amp.astype(int))

phs = data[:,1]
phs = phs.reshape((cdim, ndim))
#print("phs:")
#print(phs)

fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.
X = ccoords
Y = ncoords
X, Y = np.meshgrid(X, Y)

Z = amp #amp.reshape((cdim, ndim))

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
#ax.set_zlim(-1.01, 1.01)
#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
#fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()