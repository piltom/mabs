import numpy as np

def minprocdirectivity(micPos, f):
    directivity = np.zeros((360,360)) # directivity[phi][theta]
    gains = np.zeros(len(micPos))

    for phi in range(360):
        phiRad = phi*np.pi/180
        for theta in range(360):
            thetaRad = theta*np.pi/180
            w=np.array([np.cos(phiRad)*np.cos(thetaRad),
                        np.cos(phiRad)*np.sin(thetaRad),
                        np.sin(phiRad)]) # Weights matrix
            for i, subArr in enumerate(micPos):
                delays = np.sum(subArr*w, axis=1)/343.3
                realPart = np.sum(np.cos(2*np.pi*f*delays))
                imagPart = np.sum(np.sin(2*np.pi*f*delays))
                gains[i] = np.sqrt(realPart*realPart + imagPart*imagPart)/len(subArr)
            directivity[phi][theta]=20*np.log10(np.min(gains))
    return directivity
