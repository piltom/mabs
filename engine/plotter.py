import numpy as np
import matplotlib.pyplot as plt


def plotSimFFT(sim):
    t = np.arange(sim.t_range[0], sim.t_range[1], sim.t_step)
    signals_t = []
    if(not sim.wasRun()):
        out = sim.run()
    else:
        out = sim.getOut()
    for signal in sim.signals:
        signals_t.append(np.array(list(map(signal.get_sample, t))))
    fig, axs = plt.subplots(nrows=len(signals_t)+1, ncols=2, figsize=(7, 7))
    axs[0, 0].set_title(sim.__str__())
    axs[0, 0].plot(t, out, color='C0')
    axs[0, 0].set_xlabel("Time [ms]")
    axs[0, 0].set_ylabel("Amplitude [V]")
    axs[0, 1].set_title("Frequency")
    axs[0, 1].plot(20*np.log10(np.abs(np.fft.fft(out))), color='C0')
    axs[0, 1].set_xlabel("Frequency")
    axs[0, 1].set_ylabel("Module")
    for i, signal in enumerate(signals_t):
        axs[i+1, 0].set_title(sim.signals[i].__str__())
        axs[i+1, 0].plot(t, signal, color='C0')
        axs[i+1, 0].set_xlabel("Time [ms]")
        axs[i+1, 0].set_ylabel("Amplitude [V]")
        axs[i+1, 1].set_title("Frequency spectra")
        axs[i+1, 1].plot(20*np.log10(np.abs(np.fft.fft(signal))), color='C0')
        axs[i+1, 1].set_xlabel("Frequency")
        axs[i+1, 1].set_ylabel("Module")
    plt.show()


def plotSim(sim, save_to=None):
    t = np.arange(sim.t_range[0], sim.t_range[1], sim.t_step)
    signals_t = []
    if(not sim.wasRun()):
        out = sim.run()
    else:
        out = sim.getOut()
    for signal in sim.signals:
        signals_t.append(np.array(list(map(signal.get_sample, t))))
    fig, axs = plt.subplots(nrows=len(signals_t)+1, ncols=1, figsize=(7, 7), squeeze=False)
    axs[0][0].set_title(sim.__str__())
    axs[0][0].plot(t, out, color='C0')
    axs[0][0].set_xlabel("Time [ms]")
    axs[0][0].set_ylabel("Amplitude")
    for i, signal in enumerate(signals_t):
        axs[i+1][0].set_title(sim.signals[i].__str__())
        axs[i+1][0].plot(t, signal, color='C0')
        axs[i+1][0].set_xlabel("Time [ms]")
        axs[i+1][0].set_ylabel("Amplitude")
    fig.tight_layout()
    if save_to is None:
        plt.show()
    else:
        plt.savefig(save_to, format='png')


def plotPolar(angles, values, save_to=None, text={}):
    plt.clf()
    plt.axes(projection='polar').set_ylim(-40, 0)
    plt.polar(np.deg2rad(angles), values)
    if "title" in text:
        plt.title(text["title"])
    plt.tight_layout()
    if save_to is None:
        plt.show()
    else:
        plt.savefig(save_to, format='png')


def plotColormap(values, x_labels=None, y_labels=None, save_to=None, text={}):
    plt.clf()
    if x_labels is None:
        x_labels = list(range(values.shape[1]))
    if y_labels is None:
        y_labels = list(range(values.shape[0]))
    plt.pcolormesh(x_labels, y_labels, values, cmap="viridis", shading="auto")
    plt.clim(-60, 0)
    plt.colorbar()
    if "xlabel" in text:
        plt.xlabel(text["xlabel"])
    if "ylabel" in text:
        plt.ylabel(text["ylabel"])
    if "title" in text:
        plt.title(text["title"])
    if save_to is None:
        plt.show()
    else:
        plt.savefig(save_to, format='png')
