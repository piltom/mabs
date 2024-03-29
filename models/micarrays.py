import numpy as np


def ULAArray(K, L, noise=0):
    """
    Linear ULA microphone array

    Function for creating a GenericArray representing an ULA microphone
    array.

    Args:
        K (int): Number of mics in the ULA subarray
        L (int): Length of mic bar

    Returns:
        GenericArray: Generic Array class representing an ULA array.

    """

    freq = 343*K/(2*L)
    d = 343/(2*freq)
    subarrayK = np.concatenate((np.linspace(
        (-d*(K//2), 0, 0), (d*(K//2), 0, 0), K), np.linspace((0, -d*(K//2), 0), (0, d*(K//2), 0), K)))
    micPos = np.array([subarrayK])

    name = 'ULAArray - K: %d L: %f' % (K, L)

    return GenericArray(micPos, noise, name)


def coprimeArray(K, M, N, L, noise=0):
    """
    Linear Semi-Coprime microphone array

    Function for creating a GenericArray representing a semi coprime microphone
    array.

    Args:
        K (int): Number of mics in the small ULA subarray
        M (int): Number of mics in the first coprime subarray
        N (int): Number of mics in the second coprime subarray
        L (int): Length of mic bar

    Returns:
        GenericArray: Generic Array class representing a linear semi coprime array.

    """

    freq = 343*M*N/(2*L)
    d = 343/(2*freq)
    subarrayK = np.linspace((0, 0, 0), ((K-1)*d, 0, 0), K)
    subarrayM = np.linspace((0, 0, 0), (d*N*(M-1), 0, 0), M)
    subarrayN = np.linspace((0, 0, 0), (d*M*(N-1), 0, 0), N)
    micPos = np.array([subarrayK, subarrayM, subarrayN])

    name = 'coprimeLArray - N: %d M: %d K: %d L: %f' % (N, M, K, L)

    return GenericArray(micPos, noise, name)


def SemiCoprimeArray(N, M, L, noise=0):
    freq = 343*M*N/(2*L)
    d = 343/(2*freq)
    subarrayN = np.linspace((0, 0, 0), (M*(N-1)*d, 0, 0), N)
    subarrayM = np.linspace((0, 0, 0), (d*N*(M-1), 0, 0), M)
    micPos = np.array([subarrayN, subarrayM])

    name = 'SemiCoprimeLArray - N: %d M: %d L: %f' % (N, M, L)

    return GenericArray(micPos, noise, name)


def SemiCoprimeLArray(K, M, N, L, noise=0):
    """Two Linear Semi-Coprime microphone array in a L shape."""
    freq = 343*M*N/(2*L)
    d = 343/(2*freq)
    subarrayK = np.concatenate((np.linspace(
        (0, 0, 0), ((K-1)*d, 0, 0), K), np.linspace((0, 0, 0), (0, (K-1)*d, 0), K)))
    subarrayM = np.concatenate((np.linspace(
        (0, 0, 0), (d*N*(M-1), 0, 0), M), np.linspace((0, 0, 0), (0, d*N*(M-1), 0), M)))
    subarrayN = np.concatenate((np.linspace(
        (0, 0, 0), (d*M*(N-1), 0, 0), N), np.linspace((0, 0, 0), (0, d*M*(N-1), 0), N)))
    micPos = np.array([subarrayK, subarrayM, subarrayN])

    name = 'SemiCoprimeLArray - N: %d M: %d K: %d L: %f' % (N, M, K, L)

    return GenericArray(micPos, noise, name)


def SemiCoprimeXArray(K, M, N, L, noise=0):
    """Two Linear Semi-Coprime microphone array in a X shape."""
    freq = 343*M*N/(2*L)
    d = 343/(2*freq)
    subarrayK = np.concatenate((np.linspace(
        (-d*(K//2), 0, 0), (d*(K//2), 0, 0), K), np.linspace((0, -d*(K//2), 0), (0, d*(K//2), 0), K)))
    subarrayM = np.concatenate((np.linspace((-d*N*(M//2), 0, 0), (d*N*(M//2), 0, 0), M),
                               np.linspace((0, -d*N*(M//2), 0), (0, d*N*(M//2), 0), M)))
    subarrayN = np.concatenate((np.linspace((-d*M*(N//2), 0, 0), (d*M*(N//2), 0, 0), N),
                               np.linspace((0, -d*M*(N//2), 0), (0, d*M*(N//2), 0), N)))
    micPos = np.array([subarrayK, subarrayM, subarrayN]
                      )  # Returns array of arrays

    name = 'SemiCoprimeXArray - N: %d M: %d K: %d L: %f' % (N, M, K, L)

    return GenericArray(micPos, noise, name)


def TriCoprimeArray(K, M, N, R, noise=0):
    """Three Linear Semi-Coprime microphone array in a peace sign shape."""
    freq = 343*M*N/(2*R)
    d = 343/(2*freq)

    subarrayK = np.concatenate((np.linspace((0, 0, 0), ((K-1)*d, 0, 0), K),
                                np.linspace(
                                    (0, 0, 0), ((K-1)*d*np.cos(np.pi/3), (K-1)*d*np.sin(np.pi/3), 0), K),
                                np.linspace((0, 0, 0), ((K-1)*d*np.cos(-np.pi/3), (K-1)*d*np.sin(-np.pi/3), 0), K)))
    subarrayM = np.concatenate((np.linspace((0, 0, 0), (d*N*M, 0, 0), M),
                                np.linspace(
                                    (0, 0, 0), (d*N*M*np.cos(np.pi/3), d*N*M*np.sin(np.pi/3), 0), M),
                                np.linspace((0, 0, 0), (d*N*M*np.cos(-np.pi/3), d*N*M*np.sin(-np.pi/3), 0), M)))
    subarrayN = np.concatenate((np.linspace((0, 0, 0), (d*N*M, 0, 0), N),
                                np.linspace(
                                    (0, 0, 0), (d*N*M*np.cos(np.pi/3), d*N*M*np.sin(np.pi/3), 0), N),
                                np.linspace((0, 0, 0), (d*N*M*np.cos(-np.pi/3), d*N*M*np.sin(-np.pi/3), 0), N)))

    micPos = np.array([subarrayM, subarrayN, subarrayK]
                      )  # Returns array of arrays

    name = 'TriCoprimeArray - N: %d M: %d K: %d R: %f' % (N, M, K, R)
    return GenericArray(micPos, noise, name)


def unpackInstantiate(arr_type, params):
    if arr_type == "ULA":
        return ULAArray(int(params["K"]), float(params["L"]))
    elif arr_type == "SemiCoprime":
        return SemiCoprimeArray(int(params["N"]), int(params["M"]), float(params["L"]))
    else:
        return None


class GenericArray():
    """Generic Microphone array class"""

    def __init__(self, micPos, noise, name="Unnamed"):
        self.micPos = micPos
        self.micNoise = noise
        self.name = name
        self.delayCache = {}

    def __str__(self):
        return self.name

    def getOut(self, signals, t_ms):
        micOuts = np.zeros(len(self.micPos))
        for signal in signals:
            for i in range(len(self.micPos)):
                if not ((str(signal.angles), i) in self.delayCache):
                    self.delayCache[(str(signal.angles), i)] = np.sum(
                        self.micPos[i]*signal.w, axis=1)*1000/343.3
                micOuts[i] = micOuts[i] + \
                    sum(signal.get_sample(
                        t_ms+self.delayCache[(str(signal.angles), i)]))

        return np.array(micOuts)
