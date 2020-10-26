import numpy as np

def minprocdirectivity(micPos, f):
    directivity = np.zeros((360,360)) # directivity[phi][theta]
    gains = np.zeros(len(micPos))

    for phi in range(360):
        for theta in range(360):
            for i, subArr in enumerate(micPos):
                gains[i] = np.sqrt(realPart*realPart + imagPart*imagPart)/len(subArr)
    return directivity
