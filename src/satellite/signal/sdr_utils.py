import numpy as np

def generate_carrier(fs, fc, duration):
    t = np.arange(0, duration, 1/fs)
    signal = np.exp(1j * 2 * np.pi * fc * t)
    return signal

def apply_doppler(signal, fs, shift_hz):
    t = np.arange(len(signal)) / fs
    shifted_signal = signal * np.exp(1j * 2 * np.pi * shift_hz * t)
    return shifted_signal

def rrc_filter_taps(beta, span, sps):
    """
    Generate Root-Raised Cosine (RRC) filter taps.
    """
    n = np.arange(-span * sps, span * sps + 1)
    t = n / sps
    taps = np.zeros(len(n))
    
    for i, ti in enumerate(t):
        if ti == 0:
            taps[i] = 1 - beta + 4 * beta / np.pi
        elif abs(ti) == 1 / (4 * beta):
            taps[i] = (beta / np.sqrt(2)) * (
                (1 + 2 / np.pi) * np.sin(np.pi / (4 * beta)) + 
                (1 - 2 / np.pi) * np.cos(np.pi / (4 * beta))
            )
        else:
            taps[i] = (np.sin(np.pi * ti * (1 - beta)) + 
                       4 * beta * ti * np.cos(np.pi * ti * (1 + beta))) / (
                       np.pi * ti * (1 - (4 * beta * ti)**2))
    return taps / np.sqrt(sps)

class QPSKModulator:
    def __init__(self, sps=4, beta=0.35):
        self.sps = sps
        self.beta = beta
        self.taps = rrc_filter_taps(beta, 10, sps)
        
    def modulate(self, data_bits):
        # Data bits to symbols
        symbols = (2 * data_bits[0::2] - 1) + 1j * (2 * data_bits[1::2] - 1)
        symbols /= np.sqrt(2)
        
        # Upsample
        upsampled = np.zeros(len(symbols) * self.sps, dtype=complex)
        upsampled[::self.sps] = symbols
        
        # Filter
        return np.convolve(upsampled, self.taps, mode='full')
