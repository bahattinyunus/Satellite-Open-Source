from skyfield.api import Topos, load
import numpy as np

class OrbitDynamics:
    def __init__(self, tle_line1=None, tle_line2=None):
        self.stations = load('de421.bsp')
        self.ts = load.timescale()
        if tle_line1 and tle_line2:
            self.satellite = load.tle_lines(tle_line1, tle_line2)
        else:
            # Default to ISS for example if no TLE provided
            self.satellite = None

    def get_position(self, time):
        """
        Get satellite position at a specific time.
        """
        if not self.satellite:
            return None
        geocentric = self.satellite.at(time)
        return geocentric.position.km

    def calculate_doppler_shift(self, center_freq_hz, range_rate_km_s):
        """
        Calculate Doppler shift.
        f_shift = f * (v_relative / c)
        """
        c_km_s = 299792.458
        doppler_shift = center_freq_hz * (range_rate_km_s / c_km_s)
        return doppler_shift

def doppler_example():
    calc = OrbitDynamics()
    freq = 435e6  # 435 MHz (Amateur Satellite Band)
    v_rel = 7.5  # Typical LEO velocity relative to ground is lower but range rate varies
    shift = calc.calculate_doppler_shift(freq, v_rel)
    print(f"Doppler shift at {freq/1e6} MHz with {v_rel} km/s approach: {shift/1e3:.2f} kHz")

if __name__ == "__main__":
    doppler_example()
