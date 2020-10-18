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

For creating a pure tone (i.e. a sine wave) we can use function `soundwave.sin( angles, amplitude, frequency, timerange)`. Extra optional parameters are `fs` (sampling frequency) and `name`. Parameter angles
should be a tuple of the form: `(elevation, azimuth)`, in degrees. `timerange` can be a tuple or array
containing the start and end of the signal in milliseconds.

```python
from models import Soundwave

...

sw1=soundwave.sin((90,0), 10, 5000, (0,10),fs=100000)
sw2=soundwave.sin((0,0), 10, 5000, (15,25),fs=100000)
sw3=soundwave.sin((45,45), 10, 5000, (30,40),fs=100000)
signals=[sw1,sw2,sw3]
```

Now we instantiate a microphone array, in this case a semi coprime array. Parameters
are K,M,N,L,noise (variance of a 0 centered gaussian). For details on this parameters
check the documentation or the function docstring.

```python
from models import micarrays

...

scma1= micarrays.SemiCoprimeArray(5,8,9,1,noise=0.1)
```
>Note: This function is just an interface to the `models.micarrays.GenericArray`
class. This generic class takes an array of subarrays of microphone positions, microphone noise
and an optional name. This way you can create any configuration you like.

Then we need a signal processor. In this case, a minimum window power processor
(parameter is the window width):

```python
from models.processors import MinWindowProcessor

...

proc_min5=MinWindowProcessor(5)
```

Now, with all the elements we can generate a simulation.

Here we use the BaseTimeSim class,
which takes a microphone array object, the soundwave signal numpy array, the processor object,
a list with the timeframe in miliseconds, the time step for the simulation in miliseconds and an optional name.

 ```python
 from engine.timesim import BaseTimeSim

 ...

timesim1=BaseTimeSim(scma1,signals,proc_min5,[0,40],0.01, name="TestSim")
 ```

 Finally, using a plotter function from the plotter submodule, we can pass the simulation object as a
 parameter to generate all values and plot them. This function used here plots the output and the
 original signals, both in time and frecuency.

 ```python
 from engine import plotter

 ...

plotter.plotSimFFT(timesim1)
 ```
## Todo
- Create more functions for generating common sound signals (sine, white noise)
- Create functions for importing audio files
- Add more mic array generating functions.
- Add a way to plot the directivity
- Create GUI for generating new simulations, adding signals, generating processors, etc.
- Create a way to playback signals and outputs
- Create an optimizer that adjusts parameters of processor within a range to optimize SNR
- Create a 2d representation of the array, and check for overlaps in the microphones
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
