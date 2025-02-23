from src import functions


def test_total_usage_check():
    sim = functions.Simulation()
    df, total_power_usage = sim.calculate_revenue()
    assert round(sum(df["Power Usage"]),6) <= total_power_usage

