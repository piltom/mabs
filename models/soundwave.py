import numpy as np

class Soundwave():
    def __init__(self, angle, samples, fs, name="unnamed signal"):
        self.angle=angle
        self.anglesine=np.sin(np.pi*angle/180)
        self.nsamples=len(samples)
        self.samples=np.append(samples,0)
        self.fs=fs
        self.fs_khz=self.fs/1000
        self.name=name
    def __str__(self):
        return '%s - Angle %d °' % (self.name, self.angle)
    def get_sample(self, t_ms):
        samples_i = np.int64(np.floor(t_ms*self.fs_khz))
        if not np.isscalar(samples_i):
            for i in range(len(samples_i)):
                if (samples_i[i]<0) or (samples_i[i]>self.nsamples):
                    samples_i[i]=-1
        else:
            if (samples_i<0) or (samples_i>self.nsamples):
                samples_i=-1
        return self.samples[samples_i]
def sin(angle, amplitude, f, duration_ms, fs=None, name=None):
    if fs==None:
        fs=20*f
    if name==None:
        name= "sine %d Hz" % f
    n_samples=np.int64(duration_ms*fs/1000)
    return Soundwave(angle, amplitude*np.sin(f/fs*2*np.pi*np.arange(0,n_samples)), fs, name=name)
