from models import soundwave, micarrays
from models.processors import MinWindowProcessor
from engine import plotter
from engine.timesim import BaseTimeSim
from engine.directivity import prodprocdirectivity_fsweep, prodprocdirectivity

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    sw1 = soundwave.sin((90, 0), 10, 5000, (0, 10), fs=100000)
    sw2 = soundwave.sin((0, 0), 10, 5000, (15, 25), fs=100000)
    sw3 = soundwave.sin((45, 45), 10, 5000, (30, 40), fs=100000)
    signals = [sw1, sw2, sw3]
    scma1 = micarrays.SemiCoprimeArray(5, 7, 0.15)
    #scma1= micarrays.SemiCoprimeXArray(5,7,9,1, noise=0)
    #scma1= micarrays.ULAArray(23, 1, noise=0)
    #scma1 = micarrays.TriCoprimeArray(7, 11, 13, 1, noise=0)
    directivity, flabels = prodprocdirectivity_fsweep(
        scma1.micPos, f_range=[50, 40000, 50])
    plotter.plotColormap(directivity, y_labels=flabels)
    """
    intheta = 0
    while (intheta >= 0):
        print("Escriba texto")
        intheta = int(input())
        plotter.plotPolar(list(range(360)), directivity[:, intheta])
    """
    #plotter.plotPolar(list(range(360)), directivity[45,:])

    # timesim1=BaseTimeSim(scma1,signals,proc_min5,[0,40],0.01, name="TestSim")

    # plotter.plotSimFFT(timesim1)
