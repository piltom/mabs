from models import soundwave
from models.micarrays import SemiCoprimeArray
from models.processors import MinWindowProcessor
from engine import plotter
from engine.timesim import BaseTimeSim
import numpy as np

sw1=soundwave.sin(0, 10, 5000, 10,fs=100000)
sw2=soundwave.sin(70, 11, 10000, 10,fs=100000)
sw3=soundwave.sin(85, 9, 2500, 10,fs=100000)
signals=[sw1,sw2,sw3]
scma1= SemiCoprimeArray(5,8,9,1, noise=1)

proc_min5=MinWindowProcessor(20)

timesim1=BaseTimeSim(scma1,signals,proc_min5,[0,10],0.01, name="TestSim")

plotter.plotSim(timesim1)
