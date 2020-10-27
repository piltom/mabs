from models import soundwave, micarrays
from models.processors import MinWindowProcessor
from engine import plotter
from engine.timesim import BaseTimeSim
from engine.directivity import minprocdirectivity

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

if __name__=="__main__":
    sw1=soundwave.sin((90,0), 10, 5000, (0,10),fs=100000)
    sw2=soundwave.sin((0,0), 10, 5000, (15,25),fs=100000)
    sw3=soundwave.sin((45,45), 10, 5000, (30,40),fs=100000)
    signals=[sw1,sw2,sw3]
    #scma1= micarrays.SemiCoprimeXArray(5,7,9,1, noise=0)
    #scma1= micarrays.ULAArray(23, 1, noise=0)
    scma1= micarrays.TriCoprimeArray(5,7,1, noise=0)
    directivity = minprocdirectivity(scma1.micPos, 5000)

    inphi = 0
    while (inphi>=0):
        print("Escriba texto")
        intheta=input()
        plotter.plotPolar(list(range(360)), directivity[:,int(intheta)])

    #plotter.plotPolar(list(range(360)), directivity[45,:])


    # timesim1=BaseTimeSim(scma1,signals,proc_min5,[0,40],0.01, name="TestSim")

    # plotter.plotSimFFT(timesim1)
