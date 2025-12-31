import numpy as np

def calculate_fspl(frequency_hz, distance_m):
    """
    Calculate Free Space Path Loss (FSPL).
    """
    c = 299792458.0
    fspl = 20 * np.log10(distance_m) + 20 * np.log10(frequency_hz) + 20 * np.log10(4 * np.pi / c)
    return fspl

def calculate_rain_attenuation(frequency_ghz, rain_rate_mm_h, elevation_angle_deg, polarization_angle_deg=0):
    """
    Simplified rain attenuation calculation based on ITU-R P.838.
    A = k * R^alpha * L_s
    Note: Simplified for demonstration.
    """
    # Placeholder k and alpha coefficients for Ku-band
    k = 0.03 # Rough approximation
    alpha = 1.15
    gamma_r = k * (rain_rate_mm_h ** alpha)
    
    # Path length adjustment based on elevation
    # L_s = h_r / sin(theta)
    h_r = 4.0  # Rain height in km (typical)
    theta_rad = np.radians(elevation_angle_deg)
    l_s = h_r / np.sin(theta_rad) if elevation_angle_deg > 5 else h_r / np.sin(np.radians(5))
    
    attenuation_db = gamma_r * l_s
    return attenuation_db

def calculate_system_noise_temperature(t_ant_k, t_lna_k, gain_lna_db, t_cable_k=290, loss_cable_db=0.5):
    """
    Calculate total system noise temperature (Tsys).
    Tsys = T_ant + T_lna + T_cable/(G_lna) ...
    """
    g_lna = 10 ** (gain_lna_db / 10)
    l_cable = 10 ** (loss_cable_db / 10)
    # Simplified Friis formula for noise
    t_sys = t_ant_k + t_lna_k + (t_cable_k * (l_cable - 1)) / g_lna
    return t_sys

class LinkBudgetSession:
    def __init__(self, freq_hz, dist_m):
        self.freq_hz = freq_hz
        self.dist_m = dist_m
        self.losses_db = {"fspl": calculate_fspl(freq_hz, dist_m)}
        
    def add_rain_loss(self, rain_rate, elevation):
        self.losses_db["rain"] = calculate_rain_attenuation(self.freq_hz/1e9, rain_rate, elevation)
        
    def get_total_loss(self):
        return sum(self.losses_db.values())

def calculate_eirp(transmit_power_dbw, antenna_gain_dbi, cable_loss_db=0):
    return transmit_power_dbw + antenna_gain_dbi - cable_loss_db

def calculate_received_power(eirp_dbw, path_loss_db, receive_gain_dbi, other_losses_db=0):
    return eirp_dbw - path_loss_db + receive_gain_dbi - other_losses_db

def calculate_snr(received_power_dbw, noise_density_dbw_hz, bandwidth_hz):
    noise_power_dbw = noise_density_dbw_hz + 10 * np.log10(bandwidth_hz)
    return received_power_dbw - noise_power_dbw
