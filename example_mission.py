from satellite.propagation.link_budget import LinkBudgetSession
from satellite.orbit.orbit_dynamics import OrbitDynamics
from satellite.signal.sdr_utils import QPSKModulator
import numpy as np

def run_mission_simulation():
    print("--- Satellite-Open-Source Mission Simulation ---")
    
    # 1. Orbit Analysis (ISS Example)
    orbit = OrbitDynamics()
    pass_info = orbit.find_next_pass(41.0082, 28.9784) # Istanbul
    print(f"Next 3 events for Istanbul: {pass_info[:3]}")
    
    # 2. Link Budget
    freq = 12.5e9 # Ku-Band
    dist = 420e3  # ~420km ISS altitude
    session = LinkBudgetSession(freq, dist)
    session.add_rain_loss(rain_rate=25, elevation=45)
    
    total_loss = session.get_total_loss()
    print(f"Total Path Loss (including rain): {total_loss:.2f} dB")
    
    # 3. Signal Generation
    mod = QPSKModulator(sps=8)
    data = np.random.randint(0, 2, 100)
    signal = mod.modulate(data)
    print(f"Modulated Signal Generated: {len(signal)} samples")

if __name__ == "__main__":
    run_mission_simulation()
