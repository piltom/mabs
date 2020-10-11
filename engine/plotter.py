import numpy as np
import matplotlib.pyplot as plt

def plotSim(sim):
    t = np.arange(sim.t_range[0],sim.t_range[1], sim.t_step)
    signals_t = []
    out=sim.run()
    for signal in sim.signals:
        signals_t.append(np.array(list(map(signal.get_sample, t))))
    fig, axs = plt.subplots(nrows=len(signals_t)+1, ncols=1, figsize=(7, 7))
    axs[0].set_title(sim.__str__())
    axs[0].plot(t, out, color='C0')
    axs[0].set_xlabel("Time [ms]")
    axs[0].set_ylabel("Amplitude [V]")
    for i, signal in enumerate(signals_t):
        axs[i+1].set_title(sim.signals[i].__str__())
        axs[i+1].plot(t, signal, color='C0')
        axs[i+1].set_xlabel("Time [ms]")
        axs[i+1].set_ylabel("Amplitude [V]")
    fig.tight_layout()
    plt.show()
