import numpy as np


def prodprocdirectivity(micPos, f):
    directivity = np.zeros((360, 360))  # directivity[phi][theta]
    gains = np.zeros(len(micPos))

    for phi in range(360):
        phiRad = phi*np.pi/180
        for theta in range(360):
            thetaRad = theta*np.pi/180
            w = np.array([np.cos(phiRad)*np.cos(thetaRad),
                          np.cos(phiRad)*np.sin(thetaRad),
                          np.sin(phiRad)])  # Weights matrix
            for i, subArr in enumerate(micPos):
                delays = np.sum(subArr*w, axis=1)/343.3
                realPart = np.sum(np.cos(2*np.pi*f*delays))
                imagPart = np.sum(np.sin(2*np.pi*f*delays))
                gains[i] = np.sqrt(realPart*realPart
                                   + imagPart*imagPart)/len(subArr)
            directivity[phi][theta] = 20*np.log10(np.prod(gains))
    return directivity


def prodprocdirectivity_fsweep(micPos, f_range=[100, 40000, 200], phi_0=0):
    # directivity[phi][theta]
    directivity = np.zeros((int((f_range[1]-f_range[0])/f_range[2]), 180))
    gains = np.zeros(len(micPos))  # one 0 per subarray
    for f_i, f in enumerate(range(*f_range)):
        phiRad = phi_0*np.pi/180
        for theta in range(180):
            thetaRad = theta*np.pi/180
            w = np.array([np.cos(phiRad)*np.cos(thetaRad),
                          np.cos(phiRad)*np.sin(thetaRad),
                          np.sin(phiRad)])  # Weights matrix
            for i, subArr in enumerate(micPos):
                delays = np.sum(subArr*w, axis=1)/343.3
                realPart = np.sum(np.cos(2*np.pi*f*delays))
                imagPart = np.sum(np.sin(2*np.pi*f*delays))
                gains[i] = np.sqrt(realPart*realPart
                                   + imagPart*imagPart)/len(subArr)
                directivity[f_i][theta] = 20*np.log10(np.prod(gains))
    return directivity, list(range(*f_range))
