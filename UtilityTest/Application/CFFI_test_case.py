"""
First part of the script generates phantom flux surfaces.
Second part generates list of pixels that are crossed by it.
"""

import numpy as np 
import matplotlib.pyplot as plt 
import sys
import surface 
import image


# Create surface
Rmin, Rmax = 1.9573, 3.7472             # from JET wall geometry
zmin, zmax = -1.43545, 1.712

# Generate pixels
# Axis as in Wthin.py maker: MUST DECIDE A WAY TO MAKE IT COHERENT IN ALL SCRIPTS
dimR, dimz = 40, 70
i = image.image(dimR, dimz, Rmin+0.15, Rmax-0.15, zmin+0.31, zmax-0.31)

# Surface generation
Rc = (Rmax+Rmin)/2.
zc = (zmax+zmin)/2.
R = 0.51
dim = 100
RSurface = np.linspace(Rc-R, Rc+R, dim)
curve = np.sqrt(R**2-(RSurface-Rc)**2)
reverseCurve = curve[::-1]
zSurface = np.append(zc+curve , zc-reverseCurve[1:])
reverseRSurface = RSurface[::-1]
RSurface = np.append(RSurface, reverseRSurface[1:])

s = surface.surface()
s.FromScratchesCpp(RSurface, zSurface, i)
#s.FromScratchesC(RSurface, zSurface, i)

#print("Ci sono differenze tra due cicli e vettorizzazione?", np.any(s.pixels!=s1.pixels))

# PLOT 
plt.title('Cycles')
plt.pcolor(i.RAxis, i.zAxis, s.plot, cmap='Blues', edgecolor='y')         # pixels in surface

plt.plot(s.R, s.z, color='r')                                # surface
plt.plot(s.R, s.z, 'o', color='g', markersize=1)

plt.axis('scaled')
plt.show()
