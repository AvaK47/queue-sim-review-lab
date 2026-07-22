import sys
import os
# Add parent directory to path so we can import mm1_sim
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import mm1_sim

def test_simulation_runs():
    """Weak test: just ensures the simulation runs without crashing."""
    try:
        avg, waits = mm1_sim.run_simulation(lambda_=0.5, mu=1.0, total_time=10.0, seed=123)
    except Exception as e:
        assert False, f"Simulation raised exception: {e}"
    # We do NOT check that waits are non‑negative (that’s the point of the bug)
    assert avg is not None
