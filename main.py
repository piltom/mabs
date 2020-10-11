from models.soundwave import Soundwave
from models.micarrays import SemiCoprimeArray
from models.processors import MinWindowProcessor
from engine import plotter
from engine.timesim import BaseTimeSim
import numpy as np

sw1=Soundwave(0, 10*np.sin(0.1*np.pi*np.arange(0,999)), 100000, name="sine 5kHz")
sw2=Soundwave(80, 10*np.sin(0.2*np.pi*np.arange(0,999)), 100000, name="sine 10kHz")
sw3=Soundwave(90, 10*np.sin(0.05*np.pi*np.arange(0,999)), 100000, name="sine 2.5kHz")
signals=[sw1,sw2,sw3]
scma1= SemiCoprimeArray(5,8,9,1)

proc_min5=MinWindowProcessor(5)

timesim1=BaseTimeSim(scma1,signals,proc_min5,[0,10],0.01, name="TestSim")

plotter.plotSim(timesim1)
