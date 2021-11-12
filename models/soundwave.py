import numpy as np


class Soundwave():
    def __init__(self, angles, samples, fs, t_start=0, name="unnamed signal"):
        self.angles = angles
        phi = angles[0]
        theta = angles[1]
        phicos = np.cos(np.pi*phi/180)
        phisin = np.sin(np.pi*phi/180)
        thetasin = np.sin(np.pi*theta/180)
        thetacos = np.cos(np.pi*theta/180)
        self.w = np.array([phicos*thetacos, phicos*thetasin, phisin])
        self.nsamples = len(samples)
        self.samples = np.append(samples, 0)
        self.fs = fs
        self.fs_khz = self.fs/1000
        self.t_start = t_start
        self.name = name

    def __str__(self):
        return '%s - phi:%d ° theta:%d °' % (self.name,
                                             self.angles[0],
                                             self.angles[1])

    def get_sample(self, t_ms):
        samples_i = np.int64(np.floor((t_ms-self.t_start)*self.fs_khz))
        if not np.isscalar(samples_i):
            for i in range(len(samples_i)):
                if (samples_i[i] < 0) or (samples_i[i] > self.nsamples):
                    samples_i[i] = -1
        else:
            if (samples_i < 0) or (samples_i > self.nsamples):
                samples_i = -1
        return self.samples[samples_i]


def sin(angles, amplitude, f, timerange, fs=None, name=None):
    if fs is None:
        fs = 20*f
    if name is None:
        name = "sine %d Hz" % f
    n_samples = np.int64((timerange[1]-timerange[0])*fs/1000)

    return Soundwave(angles,
                     amplitude*np.sin(f/fs*2*np.pi*np.arange(0, n_samples)),
                     fs,
                     t_start=timerange[0],
                     name=name)
