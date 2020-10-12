import numpy as np

class SemiCoprimeArray():
    def __init__(self, K,M,N,L, noise=0):
        self.M=M
        self.K=K
        self.N=N
        self.L=L
        self.freq=343*M*N/(2*L)
        self.d=343/(2*self.freq)
        self.mDelays=np.array(range(M))*1000*N*self.d/343
        self.nDelays=np.array(range(N))*1000*M*self.d/343
        self.kDelays=np.array(range(K))*1000*self.d/343
        self.noise=np.sqrt(noise)
    def __str__(self):
        return 'SemiCoprimeArray - N: %d M: %d K: %d L: %d' % (self.N, self.M, self.K, self.L)
    def getOut(self, signals, t_ms):
        micsM=0
        micsN=0
        micsK=0
        for signal in signals:
            micsM=micsM + signal.get_sample(t_ms+self.mDelays*signal.phicos*signal.thetacos) + np.random.normal(0,self.noise)
            micsN=micsN + signal.get_sample(t_ms+self.nDelays*signal.phicos*signal.thetacos) + np.random.normal(0,self.noise)
            micsK=micsK + signal.get_sample(t_ms+self.kDelays*signal.phicos*signal.thetacos) + np.random.normal(0,self.noise)
        return np.array([sum(micsN)/self.N,sum(micsM)/self.M,sum(micsK)/self.K])

class SemiCoprimeLArray():
    def __init__(self, K,M,N,L, noise=0):
        self.M=M
        self.K=K
        self.N=N
        self.L=L
        self.freq=343*M*N/(2*L)
        self.d=343/(2*self.freq)
        self.mDelays=np.array(range(M))*1000*N*self.d/343
        self.nDelays=np.array(range(N))*1000*M*self.d/343
        self.kDelays=np.array(range(K))*1000*self.d/343
        self.noise=np.sqrt(noise)
    def __str__(self):
        return 'SemiCoprimeArray - N: %d M: %d K: %d L: %d' % (self.N, self.M, self.K, self.L)
    def getOut(self, signals, t_ms):
        micsM=0
        micsN=0
        micsK=0
        for signal in signals:
            micsM=micsM + signal.get_sample(t_ms+self.mDelays*signal.phicos*signal.thetacos) + signal.get_sample(t_ms+self.mDelays*signal.phicos*signal.thetasin) + np.random.normal(0,self.noise)
            micsN=micsN + signal.get_sample(t_ms+self.nDelays*signal.phicos*signal.thetacos) + signal.get_sample(t_ms+self.nDelays*signal.phicos*signal.thetasin) + np.random.normal(0,self.noise)
            micsK=micsK + signal.get_sample(t_ms+self.kDelays*signal.phicos*signal.thetacos) + signal.get_sample(t_ms+self.kDelays*signal.phicos*signal.thetasin) + np.random.normal(0,self.noise)
        return np.array([sum(micsN)/(2*self.N),sum(micsM)/(2*self.M),sum(micsK)/(2*self.K)])
