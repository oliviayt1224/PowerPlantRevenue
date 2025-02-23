import sys
import os

# Add the 'src' directory to sys.path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.append(src_path)

# Now you can import from the src module
import functions

def test_total_usage_check():
    sim = functions.Simulation()
    df, total_power_usage = sim.calculate_revenue()
    assert sum(df["Power Usage"]) <= total_power_usage

