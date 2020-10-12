import numpy as np

class BaseTimeSim():
    def __init__(self, mic_array, signals, processor, t_range, t_step, name='unnamed sim'):
        self.mic_array=mic_array
        self.signals=signals
        self.processor=processor
        self.processor.setupBuffer(len(signals))
        self.t_range=t_range
        self.t_step=t_step
        self.name=name
        self.out=None
    def __str__(self):
        return '%s Array: %s Processor: %s step:%f ms' % (self.name, self.mic_array.__str__(), self.processor.__str__(), self.t_step)
    def getOut(self):
        return np.array(self.out)
    def wasRun(self):
        return not self.out is None
    def run(self):
        self.processor.clearBuffer()
        steps = np.int64((self.t_range[1]-self.t_range[0])/self.t_step)
        out = np.zeros(steps)
        for n in range(steps):
            t=n*self.t_step
            out[n]=self.processor.process(self.mic_array.getOut(self.signals, t))
        self.out=out
        return np.array(self.out)
