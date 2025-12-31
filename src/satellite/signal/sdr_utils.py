import numpy as np

def generate_carrier(fs, fc, duration):
    """
    Generate a simple complex carrier signal.
    """
    t = np.arange(0, duration, 1/fs)
    signal = np.exp(1j * 2 * np.pi * fc * t)
    return signal

def apply_doppler(signal, fs, shift_hz):
    """
    Simulate Doppler shift by rotating the signal.
    """
    t = np.arange(len(signal)) / fs
    shifted_signal = signal * np.exp(1j * 2 * np.pi * shift_hz * t)
    return shifted_signal
