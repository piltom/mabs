# MABS: Microphone Array Beamforming Simulator

Program for simulating different microphone arrays and evaluating their response to signals,
 using different processors.

## Usage OUTDATED - Needs update to new parameters

In its current state (no gui/ui at all), you need to create a script and manually
instantiante the different components of the system (signals, mic arrays, processors, simulation)
and then plot the simulation.

An example of this is shown in the `main.py` file. This code is explained in the following
paragraphs.

Create a new set of signals (must be an array, even if only one):

For creating a pure tone (i.e. a sine wave) we can use function soundwave.sin(angle, amplitude, frequency, duration_ms). Extra optional parameters are `fs` (sampling frequency) and `name`.

```python
from models import Soundwave

...

sw1=soundwave.sin(0, 10, 5000, 10,fs=100000)
sw2=soundwave.sin(70, 11, 10000, 10,fs=100000)
sw3=soundwave.sin(85, 9, 2500, 10,fs=100000)
signals=[sw1,sw2,sw3]
```

Now we instantiate a microphone array, in this case a semi coprime array. Parameters
  are K,M,N,L,noise (variance of a 0 centered gaussian).

```python
from models.micarrays import SemiCoprimeArray

...

scma1= SemiCoprimeArray(5,8,9,1,noise=1)
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
