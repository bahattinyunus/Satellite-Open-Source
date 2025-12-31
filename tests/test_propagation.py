import pytest
from satellite.propagation.link_budget import calculate_fspl

def test_fspl():
    # Test FSPL @ 1 GHz over 1 km
    # FSPL = 20log10(d) + 20log10(f) + 20log10(4pi/c)
    # FSPL = 20log10(1000) + 20log10(1e9) + 20log10(4pi/2.99e8)
    # FSPL approx 92.45 dB
    loss = calculate_fspl(1e9, 1000)
    assert round(loss, 2) == 92.45

def test_eirp():
    from satellite.propagation.link_budget import calculate_eirp
    assert calculate_eirp(10, 30, 2) == 38
