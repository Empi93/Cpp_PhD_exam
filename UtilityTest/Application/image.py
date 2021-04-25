import numpy as np 
import matplotlib.pyplot as plt
import scipy as scipy

class pixel: 
    def __init__(self, v1, v2, v3, v4):
        self.v1, self.v2, self.v3, self.v4 = v1, v2, v3, v4         # vertices  

class image:
    def __init__(self, dimR, dimz, RMin, RMax, zMin, zMax):
        self.dimR, self.dimz = dimR, dimz
        self.RMin, self.RMax = RMin, RMax
        self.zMin, self.zMax = zMin, zMax
        self.tomoImage = np.zeros((dimz, dimR))
        self.IF = 2  # Increase Factor

        self.RAxis = np.linspace(RMin, RMax, dimR+1)         
        self.zAxis = np.linspace(zMin, zMax, dimz+1)   
        self.RAxisIF = np.linspace(self.RMin, self.RMax, self.dimR*self.IF+1)         
        self.zAxisIF = np.linspace(self.zMin, self.zMax, self.dimz*self.IF+1)  

        self.pixels = np.empty(((dimR)*(dimz), 4, 2))
        for i in range(len(self.pixels)):
            for j,pos in enumerate([[0, 0], [1, 0], [0, 1], [1,1]]) :
                self.pixels[i][j] = [self.RAxis[(i%dimR)+pos[0]], self.zAxis[(i//dimR)+pos[1]]] 

        self.pixelsIF = np.empty(((self.dimR)*(self.dimz)*self.IF**2, 4, 2))
        for i in range(len(self.pixelsIF)):
            for j,pos in enumerate([[0, 0], [1, 0], [0, 1], [1,1]]) :
                self.pixelsIF[i][j] = [self.RAxisIF[(i%(self.dimR*self.IF))+pos[0]], self.zAxisIF[(i//(self.dimR*self.IF))+pos[1]]]

    def Mask(self, surfaces, W):
        self.GoodPixels = np.array([], dtype=int)

        for s in surfaces:
            self.GoodPixels=np.append(self.GoodPixels, s.pixels)

        # add the magnetic axis pixels if not already included
        for i, pixel in enumerate(self.pixels):
            R = (np.max(pixel[:,0])+np.min(pixel[:,0]))/2.
            z = (np.max(pixel[:,1])+np.min(pixel[:,1]))/2.
            if (np.min(surfaces[0].R)<R)&(R<np.max(surfaces[0].R))&(np.min(surfaces[0].z)<z)&(z<np.max(surfaces[0].z)):
                self.GoodPixels=np.append(self.GoodPixels, i)

        self.GoodPixels = np.sort(np.unique(self.GoodPixels))

        Wcut = W[:, np.ndarray.tolist(self.GoodPixels)]
            
        # cut undesired pixels, if necessary
        if np.any(np.sum(Wcut, axis=0)==0):
            self.ZeroSumPixels = self.GoodPixels[np.where(np.sum(Wcut, axis=0)==0)]
            self.GoodPixels = np.delete(self.GoodPixels, np.where(np.sum(Wcut, axis=0)==0))
        else:
            self.ZeroSumPixels = []

        for s in surfaces:
            s.PixelsToLocal(self.GoodPixels)

        Wcut = W[:, np.ndarray.tolist(self.GoodPixels)]

        # Check mask:
        if np.any(np.sum(Wcut, axis=0)==0):
            print("Attenzione, la maschera sull'immagine non ha funzionato a dovere")
            index = np.where((np.sum(Wcut, axis=0)==0)==True)
            print('Ci sono '+str(len(index[0]))+' pixel problematici:')
            for i in index[0]:
                print(self.GoodPixels[i], self.GoodPixels[i]//self.dimR, self.GoodPixels[i]%self.dimR)

        return Wcut

    def DeleteArtefacts(self, F, LastSurface, surfaces, strong = False):
        # Delete artefacts at the border of the image
        if (LastSurface!=None):
            surfaces = surfaces[LastSurface:]
            self.ToZeroPixels = np.array([], dtype=int)
            for s in surfaces:
                self.ToZeroPixels = np.append(self.ToZeroPixels, s.pixelsLocal)      # Pixels that experiences artefacts at the border of the image
            F[np.ndarray.tolist(self.ToZeroPixels)]=0.
        
        if strong == True:
            # Taglio conteggi high field side
            camera_deg = -77.58
            camera_deg = -camera_deg * np.pi / 180.0    # revert positivity, tan has a period pi so no translation is neede
            camera_R0 = 302.15*0.01
            camera_z0 = 344.2*0.01

            camera_m = np.tan(camera_deg)
            camera_q = camera_z0 - camera_R0 * camera_m

            # taglio conteggi bassi a sinistra
            camera_deg1 = -80.62
            camera_deg1 = -camera_deg1 * np.pi / 180.0    # revert positivity, tan has a period pi so no translation is neede
            camera_R01 = 302.15*0.01
            camera_z01 = 344.2*0.01
            camera_m1 = np.tan(camera_deg1)
            camera_q1 = camera_z01 - camera_R01 * camera_m1

            camera_deg2 = -2.14
            camera_deg2 = -camera_deg2 * np.pi / 180.0    # revert positivity, tan has a period pi so no translation is neede
            camera_R02 = 605.5*0.01
            camera_z02 = 0.*0.01
            camera_m2 = np.tan(camera_deg2)
            camera_q2 = camera_z02 - camera_R02 * camera_m2

            for i, pixel in enumerate(self.pixels):
                R = (np.max(pixel[:,0])+np.min(pixel[:,0]))/2.
                z = (np.max(pixel[:,1])+np.min(pixel[:,1]))/2.

                if z>camera_m*R+camera_q:
                    F[np.where(self.GoodPixels==i)[0]] = 0.

                if (z>=camera_m1*R+camera_q1)&(z<camera_m2*R+camera_q2):
                    F[np.where(self.GoodPixels==i)[0]] = 0.
        
        return F

    def CompleteImage(self, F):
        # transfer F back to the complete 2D image
        self.tomoImage = np.zeros((self.dimz, self.dimR))
        for i, f in enumerate(F):
            self.tomoImage[self.GoodPixels[i]//self.dimR][self.GoodPixels[i]%self.dimR] = f

    def IncreasePixels(self):
        """
        first you should CompleteImage, then IncreasePixels
        """

        tomoImage = np.zeros((self.dimz*self.IF, self.dimR*self.IF))
        for i in range(int(self.dimz*self.IF)):
            for j in range(int(self.dimR*self.IF)):
                tomoImage[i][j]=self.tomoImage[i//self.IF][j//self.IF]
        self.tomoImageIF = tomoImage


    def InterpolatePixels(self):
        RMin = self.RMin + (self.RMax-self.RMin)/2./self.dimR
        RMax = self.RMax - (self.RMax-self.RMin)/2./self.dimR
        zMin = self.zMin + (self.zMax-self.zMin)/2./self.dimz
        zMax = self.zMax - (self.zMax-self.zMin)/2./self.dimz

        # Fill sum(W, axis=0)==0 pixels and increase pixels by 4
        if (len(self.ZeroSumPixels)>0):
            Originalz, OriginalR = np.mgrid[zMin:zMax:self.dimz*1j, RMin:RMax:self.dimR*1j]
            points = np.delete(np.transpose([Originalz.reshape(self.dimR*self.dimz),OriginalR.reshape(self.dimR*self.dimz)]), self.ZeroSumPixels, axis=0)
            ImageToBeCompleted = np.delete(self.tomoImage.reshape(self.dimR*self.dimz), self.ZeroSumPixels)
            Newz, NewR = np.mgrid[zMin:zMax:self.dimz*1j, RMin:RMax:self.dimR*1j]
            
            self.tomoImage = scipy.interpolate.griddata(points, ImageToBeCompleted, (Newz, NewR), method='nearest')
        
            
        # Increase pixels by 4
        Originalz, OriginalR = np.mgrid[zMin:zMax:self.dimz*1j, RMin:RMax:self.dimR*1j]
        points = np.transpose([Originalz.reshape(self.dimR*self.dimz),OriginalR.reshape(self.dimR*self.dimz)])
        Newz, NewR = np.mgrid[zMin:zMax:self.dimz*self.IF*1j, RMin:RMax:self.dimR*self.IF*1j]
        self.tomoImageIF = scipy.interpolate.griddata(points, self.tomoImage.reshape(self.dimR*self.dimz), (Newz, NewR), method='cubic')

    
    def SlidingWindowAverage(self):
        syntImage = np.zeros((self.dimz, self.dimR))

        for i in range(self.dimz):
            for j in range(self.dimR):
                syntImage[i, j] = (self.syntImage[i*self.IF, j*self.IF] 
                                    + self.syntImage[i*self.IF+1, j*self.IF] 
                                    + self.syntImage[i*self.IF, j*self.IF+1] 
                                    + self.syntImage[i*self.IF+1, j*self.IF+1]
                                    )/4.

        return syntImage.reshape(self.dimz*self.dimR)

    def SlidingWindowSmoothingIF(self):
        syntImage = np.zeros((self.dimz*self.IF, self.dimR*self.IF))
        for i in range(self.dimz*self.IF):
            for j in range(self.dimR*self.IF):
                if (i==0)&(j==0):
                    syntImage[i][j] = (self.syntImage[i][j]+self.syntImage[i+1][j]+self.syntImage[i][j+1])/3.
                elif (i==(np.shape(self.syntImage)[0]-1)) & (j==(np.shape(self.syntImage)[1]-1)):
                    syntImage[i][j] = (self.syntImage[i][j]+self.syntImage[i-1][j]+self.syntImage[i][j-1])/3.
                elif (i==0) & (j==(np.shape(self.syntImage)[1]-1)):
                    syntImage[i][j] = (self.syntImage[i][j]+self.syntImage[i+1][j]+self.syntImage[i][j-1])/3.
                elif (i==(np.shape(self.syntImage)[0]-1)) & (j==0):
                    syntImage[i][j] = (self.syntImage[i][j]+self.syntImage[i][j+1]+self.syntImage[i-1][j])/3.
                elif (i==0):
                    syntImage[i][j] = (self.syntImage[i][j]+self.syntImage[i+1][j]+self.syntImage[i][j+1]+self.syntImage[i][j-1])/4.
                elif (j==0):
                    syntImage[i][j] = (self.syntImage[i][j]+self.syntImage[i+1][j]+self.syntImage[i][j+1]+self.syntImage[i-1][j])/4.
                elif (i==(np.shape(self.syntImage)[0]-1)):
                    syntImage[i][j] = (self.syntImage[i][j]+self.syntImage[i][j+1]+self.syntImage[i-1][j]+self.syntImage[i][j-1])/4.
                elif (j==(np.shape(self.syntImage)[1]-1)):
                    syntImage[i][j] = (self.syntImage[i][j]+self.syntImage[i+1][j]+self.syntImage[i-1][j]+self.syntImage[i][j-1])/4.
                else:
                    syntImage[i][j] = (self.syntImage[i][j]+self.syntImage[i+1][j]+self.syntImage[i][j+1]+self.syntImage[i-1][j]+self.syntImage[i][j-1])/5.

        self.syntImage = syntImage

    def MakeSyntheticData(self, profile, surfaces, W, MagneticAxis='None', LH='N'):
        """
        To be used with an equilibrium created for a 40x70 image
        """
        self.syntImage = np.zeros((self.dimz*self.IF, self.dimR*self.IF))
        counter = np.full((self.dimz*self.IF, self.dimR*self.IF), 1.)
        for i,s in enumerate(surfaces):
            for p in s.pixels:
                self.syntImage[p//(self.dimR*self.IF), p%(self.dimR*self.IF)] += profile[i]
                counter[p//(self.dimR*self.IF), p%(self.dimR*self.IF)] += 1.
        
        self.syntImage = self.syntImage/counter
        
        if LH == 'N':
            self.SlidingWindowSmoothingIF()
            self.syntImageReduced = self.SlidingWindowAverage()
            return np.dot(W, self.syntImageReduced)

        if LH == 'L':
            coeff = 1. 
        if LH == 'R':
            coeff = -1. 
        
        for i, pixel in enumerate(self.pixelsIF):
            R = (np.max(pixel[:,0])+np.min(pixel[:,0]))/2.
            z = (np.max(pixel[:,1])+np.min(pixel[:,1]))/2.

            if (coeff*(R-MagneticAxis[0])>0):
                self.syntImage[i//(self.dimR*self.IF), i%(self.dimR*self.IF)] = 0.
            
        self.SlidingWindowSmoothingIF()
        self.syntImageReduced = self.SlidingWindowAverage()
        return np.dot(W, self.syntImageReduced)

    def MakeSyntheticDataFunction(self, function, par, W, MagneticAxis='None', LH='N'):
        """
        To be used with an equilibrium created for a 40x70 image
        """
        self.syntImage = np.zeros((self.dimz*self.IF, self.dimR*self.IF))
        
        for i, pixel in enumerate(self.pixelsIF):
            R = (np.max(pixel[:,0])+np.min(pixel[:,0]))/2.
            z = (np.max(pixel[:,1])+np.min(pixel[:,1]))/2.
            self.syntImage[i//(self.dimR*self.IF), i%(self.dimR*self.IF)] = function(R, z, par)

        if LH == 'N':
            self.SlidingWindowSmoothingIF()
            self.syntImageReduced = self.SlidingWindowAverage()
            return np.dot(W, self.syntImageReduced)

        if LH == 'L':
            coeff = 1. 
        if LH == 'R':
            coeff = -1.  
        
        for i, pixel in enumerate(self.pixelsIF):
            R = (np.max(pixel[:,0])+np.min(pixel[:,0]))/2.
            z = (np.max(pixel[:,1])+np.min(pixel[:,1]))/2.

            if (coeff*(R-MagneticAxis[0])>0):
                self.syntImage[i//(self.dimR*self.IF), i%(self.dimR*self.IF)] = 0.
            
        self.SlidingWindowSmoothingIF()

        self.syntImageReduced = self.SlidingWindowAverage()
        return np.dot(W, self.syntImageReduced)

        
                

    

