import numpy as np

class SemiCoprimeArray():
    def __init__(self, K,M,N,L):
        self.M=M
        self.K=K
        self.N=N
        self.L=L
        self.freq=343*M*N/(2*L)
        self.d=343/(2*self.freq)
        self.mDelays=np.array(range(M))*1000*N*self.d/343
        self.nDelays=np.array(range(N))*1000*M*self.d/343
        self.kDelays=np.array(range(K))*1000*self.d/343
    def __str__(self):
        return 'SemiCoprimeArray - N: %d M: %d K: %d L: %d' % (self.N, self.M, self.K, self.L)
    def getOut(self, signals, t_ms):
        outM=0
        outN=0
        outK=0
        for signal in signals:
            outM=outM + np.sum(signal.get_sample(t_ms+self.mDelays*signal.anglesine))
            outN=outN + np.sum(signal.get_sample(t_ms+self.nDelays*signal.anglesine))
            outK=outK + np.sum(signal.get_sample(t_ms+self.kDelays*signal.anglesine))
        return np.array([outN/self.N,outM/self.M,outK/self.K])
