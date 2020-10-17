import numpy as np

def SemiCoprimeArray(K,M,N,L, noise=0):
    """Linear Semi-Coprime microphone array in x axis."""
    freq=343*M*N/(2*L)
    d=343/(2*freq)
    subarrayK=np.linspace((0,0,0), ((K-1)*d,0,0), K)
    subarrayM=np.linspace((0,0,0), (L,0,0), M)
    subarrayN=np.linspace((0,0,0), (L,0,0), N)
    micPos=np.array([subarrayK, subarrayM, subarrayN])

    name='SemiCoprimeLArray - N: %d M: %d K: %d L: %d' % (N, M, K, L)

    return GenericArray(micPos, noise, name)

def SemiCoprimeLArray(K,M,N,L, noise=0):
    """Two Linear Semi-Coprime microphone array in an L shape."""
    freq=343*M*N/(2*L)
    d=343/(2*freq)
    subarrayK=np.concatenate((np.linspace((0,0,0), ((K-1)*d,0,0), K),np.linspace((0,0,0), (0,(K-1)*d,0), K)))
    subarrayM=np.concatenate((np.linspace((0,0,0), (L,0,0), M), np.linspace((0,0,0), (0,L,0), M)))
    subarrayN=np.concatenate((np.linspace((0,0,0), (L,0,0), N), np.linspace((0,0,0), (0,L,0), N)))
    micPos=np.array([subarrayK, subarrayM, subarrayN])

    name='SemiCoprimeLArray - N: %d M: %d K: %d L: %d' % (N, M, K, L)

    return GenericArray(micPos, noise, name)

class GenericArray():
    """Generic Microphone array class"""
    def __init__(self,micPos, noise, name="Unnamed"):
        self.micPos=micPos
        self.micNoise=noise
        self.name=name
        self.delayCache={}
    def __str__(self):
        return self.name
    def getOut(self, signals, t_ms):
        micOuts=np.zeros(len(self.micPos))
        for signal in signals:
            for i in range(len(self.micPos)):
                if not ((str(signal.angles),i) in self.delayCache):
                    self.delayCache[(str(signal.angles),i)]=np.sum(self.micPos[i]*signal.w, axis=1)*1000/343.3
                micOuts[i]=micOuts[i]+sum(signal.get_sample(t_ms+self.delayCache[(str(signal.angles),i)]))
        return np.array(micOuts)
