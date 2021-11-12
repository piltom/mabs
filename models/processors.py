import numpy as np
from collections import deque


class MinWindowProcessor():
    def __init__(self, window_size):
        self.window_size = window_size
        self.buffers = []
        self.name = 'Min processor (window=%i)' % window_size

    def __str__(self):
        return self.name

    def setupBuffer(self, nsignals):
        self.buffers = []
        for i in range(nsignals):
            self.buffers.append(deque([], maxlen=self.window_size))

    def clearBuffer(self):
        for buf in self.buffers:
            buf.clear()

    def process(self, values):
        for i, val in enumerate(values):
            self.buffers[i].append(val*val)
        sums = list(map(sum, self.buffers))
        return values[min(range(len(sums)), key=sums.__getitem__)]
