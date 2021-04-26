import numpy as np 
import matplotlib.pyplot as plt
import os
import pandas as pd
import sys
from cffi import FFI
#from _surface_object.lib import PixelsCpp
ffi = FFI()


class surface:
    def __init__(self):
        self.R = []
        self.z = []

        self.m, self.q, self.case = [],[],[]

        self.plot = []
        self.pixels = []      # list of pixel positions
    
    def FromScratchesCpp (self, RSurface, zSurface, image):
        self.R = RSurface
        self.z = zSurface

        self.m, self.q, self.case = self.LineInterpolation()
        self.plot = np.zeros((image.dimz,image.dimR))
        self.pixels = []     # list of pixel positions
        self.PixelsCpp(image)              # list of the position of pixels crossed by surface
        self.PixelsSorter(image)             # rearrange pixels according to taxi distance

    def print(self, root, i):
        """
        Print to file all the variables, so that excecution time is shorter 
        for further inversions.
        """
        os.system('mkdir ./objects')
        """
        data = pd.DataFrame({'R': self.R,
                            'z': self.z,
                            'm': self.m,
                            'q': self.q,
                            'case': self.case,
                            'pixels': self.pixels})
        data.write_csv('objects/'+str(shot)+'line'+str(i)+'.dat')
        """
        outFile = open('objects/'+root+str(i)+'.dat', 'w')
        outFile.write(str(len(self.R)) + '    ' 
                    + str(len(self.m)) + '    ' 
                    + str(len(self.pixels))+'\n')
        for i in range(self.R.size):
            outFile.write(str(self.R[i]) + '    ' + str(self.z[i])+'\n')
        for i in range(self.m.size):
            outFile.write(str(self.m[i]) + '    ' + str(self.q[i]) + '    ' + str(self.case[i])+'\n')
        for i in range(len(self.pixels)):
            outFile.write(str(self.pixels[i])+'\n')

    def LineInterpolation(self):                    # evaluates m and q of the lines that join two close points in the surface
        m = np.zeros(len(self.R)-1)
        q = np.zeros(len(self.R)-1)
        case = np.zeros(len(self.R)-1)

        for i in range(len(m)):
            # volendo nei primi due punti posso mettere subito m=0 e q=x o y a seconda
            if self.R[i]==self.R[i+1]:                                  # m = infty
                case[i] = 0
                m[i] = (self.R[i]-self.R[i+1])/(self.z[i]-self.z[i+1])
                q[i] = self.R[i] - self.z[i]*m[i]
            elif self.z[i]==self.z[i+1]:                                # m = 0
                case[i] = 1
                m[i] = (self.z[i]-self.z[i+1])/(self.R[i]-self.R[i+1])
                q[i] = self.z[i] - self.R[i]*m[i]
            else:                                                               # m > 0
                m[i] = (self.z[i]-self.z[i+1])/(self.R[i]-self.R[i+1])
                q[i] = self.z[i] - self.R[i]*m[i]
                case[i] = 2
                """
                if m[i]>0:
                    case[i] = 2
                elif m[i]<0:
                    case[i] = 3
                else:
                    print("error in LineInterpolation()")
                """
        
        return m, q, case

    def PixelDistanceForSorting(self, reference, image):
        # pixels center
        #return                      # Certesian
        return (np.abs(reference%image.dimR-self.pixels%image.dimR)+np.abs(reference//image.dimR-self.pixels//image.dimR))       # Taxi

    def PixelsSorter (self, image):
        if len(self.pixels)==0:
            return

        newPixels = np.array([self.pixels[0]])
        self.pixels = np.delete(self.pixels, 0, axis=0)

        while(len(self.pixels)>0):
            i = np.argmin(self.PixelDistanceForSorting(newPixels[-1], image))
            newPixels = np.append(newPixels, self.pixels[i])
            self.pixels = np.delete(self.pixels, i)

        self.pixels=newPixels

    def PixelsToLocal (self, GoodPixels):
        """
        Translate self.pixels into the new indexes of F
        """
        self.pixelsLocal = np.array([], dtype = int)
        for pixel in self.pixels:
            self.pixelsLocal = np.append(self.pixelsLocal, np.where(GoodPixels==pixel)[0])
        self.pixelsLocal = np.array(self.pixelsLocal, dtype=int)
    
    def PixelsCpp (self, image):
        #from _surface_object.lib import PixelsCpp       
        ffi.cdef("""
                struct bsurface;
                typedef struct bsurface bsurface_t;

                bsurface_t * bsurface_create(float* Rb, float* zb, float* m, float* q, 
                             float* Case, float coordinates[][4][2], 
                             const float Rm, const float RM, const float zm,
                             const float zM, const int lenB, const int dimR, 
                             const int dimz);
                void bsurface_destroy(bsurface_t *m);

                int* GetBorderMask(bsurface_t *b);
                """)
        libBsurface = ffi.dlopen(os.path.join('../../bin/', 'libBsurface.so'))

        # Call C function
        b = libBsurface.bsurface_create(self.R.tolist(), self.z.tolist(), 
                                    self.m.tolist(), self.q.tolist(),  
                                    self.case.tolist(), image.pixels.tolist(),
                                    image.RMin, image.RMax, image.zMin, image.zMax, 
                                    len(self.R), image.dimR, image.dimz)
        plot_result_cffi = libBsurface.GetBorderMask(b)
        #libBsurface.bsurface_destroy(b)

        for i in range(image.dimR*image.dimz):
            if (plot_result_cffi[i] == 1):
                self.plot[i//image.dimR][i%image.dimR]=1
                self.pixels.append(i)
        
        self.pixels = np.unique(np.array(self.pixels, dtype = int))

# UTILITY TEST
if __name__ == "__main__":
    # test PixelsLocal
    GoodPixels = np.array([2, 5, 7, 8, 9])