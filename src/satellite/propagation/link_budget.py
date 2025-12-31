import numpy as np

def calculate_fspl(frequency_hz, distance_m):
    """
    Calculate Free Space Path Loss (FSPL).
    
    Args:
        frequency_hz (float): Carrier frequency in Hz.
        distance_m (float): Distance between transmitter and receiver in meters.
        
    Returns:
        float: Path loss in dB.
    """
    c = 299792458.0  # Speed of light
    fspl = 20 * np.log10(distance_m) + 20 * np.log10(frequency_hz) + 20 * np.log10(4 * np.pi / c)
    return fspl

def calculate_eirp(transmit_power_dbw, antenna_gain_dbi, cable_loss_db=0):
    """
    Calculate Effective Isotropic Radiated Power (EIRP).
    """
    return transmit_power_dbw + antenna_gain_dbi - cable_loss_db

def calculate_received_power(eirp_dbw, path_loss_db, receive_gain_dbi, other_losses_db=0):
    """
    Calculate received power (Pr) in dBW.
    """
    return eirp_dbw - path_loss_db + receive_gain_dbi - other_losses_db

def calculate_snr(received_power_dbw, noise_density_dbw_hz, bandwidth_hz):
    """
    Calculate Signal-to-Noise Ratio (SNR).
    """
    noise_power_dbw = noise_density_dbw_hz + 10 * np.log10(bandwidth_hz)
    return received_power_dbw - noise_power_dbw

if __name__ == "__main__":
    # Example Calculation
    freq = 12e9  # 12 GHz (Ku band)
    dist = 36000e3  # 36,000 km (GEO)
    
    loss = calculate_fspl(freq, dist)
    print(f"FSPL at {freq/1e9} GHz and {dist/1e3} km: {loss:.2f} dB")
