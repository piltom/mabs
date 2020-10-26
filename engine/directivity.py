import numpy as np

def minprocdirectivity(micPos, f):
    directivity = np.zeros((360,360)) # directivity[phi][theta]
    gains = np.zeros(len(micPos))

    for phi in range(360):
        for theta in range(360):
            w=np.array([np.cos(np.pi*phi/180)*np.cos(np.pi*theta/180),
                        np.cos(np.pi*phi/180)*np.sin(np.pi*theta/180),
                        np.sin(np.pi*phi/180)]) # Weights matrix
            for i, subArr in enumerate(micPos):
                realPart = 0
                imagPart = 0
                for position in subArr:
                    delay  = np.sum(w*position)/343.3 # c=343.3
                    realPart += np.cos(2*np.pi*f*delay)
                    imagPart += np.sin(2*np.pi*f*delay)
                gains[i] = np.sqrt(realPart*realPart + imagPart*imagPart)/len(subArr)
            directivity[phi][theta]=np.min(gains[0])
    return directivity
