from models import soundwave, micarrays
from models.processors import MinWindowProcessor
from engine import plotter
from engine.timesim import BaseTimeSim
import numpy as np

if __name__=="__main__":
    sw1=soundwave.sin((90,0), 10, 5000, (0,10),fs=100000)
    sw2=soundwave.sin((0,0), 10, 5000, (15,25),fs=100000)
    sw3=soundwave.sin((45,45), 10, 5000, (30,40),fs=100000)
    signals=[sw1,sw2,sw3]
    scma1= micarrays.SemiCoprimeLArray(5,8,9,1, noise=0)

    proc_min5=MinWindowProcessor(20)

    timesim1=BaseTimeSim(scma1,signals,proc_min5,[0,40],0.01, name="TestSim")

    plotter.plotSimFFT(timesim1)
