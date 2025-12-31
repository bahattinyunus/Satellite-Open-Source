from skyfield.api import Topos, load, wgs84
import numpy as np
from datetime import datetime

class OrbitDynamics:
    def __init__(self, tle_line1=None, tle_line2=None):
        self.stations = load('de421.bsp')
        self.ts = load.timescale()
        if tle_line1 and tle_line2:
            self.satellite = load.tle_lines(tle_line1, tle_line2)
        else:
            # Default to ISS for example
            self.satellite = load.tle_lines(
                '1 25544U 98067A   23351.52047801  .00016029  00000-0  28795-3 0  9990',
                '2 25544  51.6416 288.5835 0004381  31.9566 112.9152 15.49506253430580'
            )

    def get_position(self, time=None):
        if time is None:
            time = self.ts.now()
        geocentric = self.satellite.at(time)
        return geocentric.position.km

    def calculate_doppler_shift(self, center_freq_hz, range_rate_km_s):
        c_km_s = 299792.458
        doppler_shift = center_freq_hz * (range_rate_km_s / c_km_s)
        return doppler_shift

    def find_next_pass(self, lat, lon, alt_m=0, duration_days=1):
        """
        Find orbital passes for a ground station.
        """
        ground_station = wgs84.latlon(lat, lon, elevation_m=alt_m)
        t0 = self.ts.now()
        t1 = self.ts.from_datetime(t0.utc_datetime().replace(day=t0.utc_datetime().day + duration_days))
        
        times, events = self.satellite.find_events(ground_station, t0, t1, altitude_degrees=10.0)
        
        passes = []
        for t, event in zip(times, events):
            event_name = ('AOS', 'MAX', 'LOS')[event]
            passes.append({
                "time": t.utc_iso(),
                "event": event_name
            })
        return passes

    def calculate_footprint(self, resolution=50):
        """
        Estimate the satellite's footprint area (radius in km).
        """
        geocentric = self.satellite.at(self.ts.now())
        subpoint = wgs84.subpoint(geocentric)
        height_km = subpoint.elevation.km
        earth_radius_km = 6371.0
        
        # Horizon angle
        rho = np.arcsin(earth_radius_km / (earth_radius_km + height_km))
        # Max central angle
        eta_max = np.degrees(np.pi/2 - rho)
        
        return {
            "lat": subpoint.latitude.degrees,
            "lon": subpoint.longitude.degrees,
            "height_km": height_km,
            "max_coverage_angle_deg": eta_max
        }
