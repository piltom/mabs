# MABS: Microphone Array Beamforming Simulator

Program for simulating different microphone arrays and evaluating their response to signals,
 using different processors.

## Usage

In its current state (no gui/ui at all), you need to create a script and manually
instantiante the different components of the system (signals, mic arrays, processors, simulation)
and then plot the simulation.

An example of this is shown in the `main.py` file. This code is explained in the following
paragraphs.

Create a new set of signals (must be an array, even if only one):

For now, only the direct class Soundwave usage is implemented. The arguments are
angle of arrival (degrees), signal samples (numpy array), sampling frequency and an optional
string for the name.

```python
from models.soundwave import Soundwave

...

sw1=Soundwave(0, 10*np.sin(0.1*np.pi*np.arange(0,999)), 100000, name="sine 5kHz")
sw2=Soundwave(80, 10*np.sin(0.2*np.pi*np.arange(0,999)), 100000, name="sine 10kHz")
sw3=Soundwave(90, 10*np.sin(0.05*np.pi*np.arange(0,999)), 100000, name="sine 2.5kHz")
signals=[sw1,sw2,sw3]
```

Now we instantiate a microphone array, in this case a semi coprime array (parameters
  are K,M,N,L):

```python
from models.micarrays import SemiCoprimeArray

...

scma1= SemiCoprimeArray(5,8,9,1)
```

Then we need a signal processor. In this case, a minimum window power processor
(parameter is the window width):

```python
from models.processors import MinWindowProcessor

...

proc_min5=MinWindowProcessor(5)
```

Now, with all the elements we can generate a simulation.

Here we use the BaseTimeSim class,
 which takes a microphone array object, the soundwave signal numpy array, the processor object, a list
 with the timeframe in miliseconds, the time step for the simulation in miliseconds and an optional name.

 ```python
 from engine.timesim import BaseTimeSim

 ...

timesim1=BaseTimeSim(scma1,signals,proc_min5,[0,10],0.01, name="TestSim")
 ```

 Finally, using a plotter function from the plotter submodule, we can pass the simulation object as a
 parameter to generate all values and plot them.

 ```python
 from engine import plotter

 ...

plotter.plotSim(timesim1)
 ```
## Todo
- Create functions for generating common sound signals (sine, white noise)
- Create functions for importing audio files
- Create GUI for generating new simulations, adding signals, generating processors, etc.
- Create a way to playback signals and outputs
- Create an optimizer that adjusts parameters of processor within a range to optimize SNR
- Create a 2d representation of the array, and check for overlaps in the microphones
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
