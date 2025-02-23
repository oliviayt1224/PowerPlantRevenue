from src.functions import *

if __name__ == "__main__":
    sim = Simulation()
    print("To use the Power Plant Revenue Simulator, here is a intro of the methodology this program uses. \n"
          "Would you like to skip it (Yes/No)?")
    intro_skip = input()
    if intro_skip == "No":
        sim.intro()

    sim.printing_out_default()
    simulation_mode = input("Do you want to proceed with the default values? (Yes/No)")
    if simulation_mode == "No":
        sim.variable_selection()

    df, total_power_usage = sim.calculate_revenue()

    print("Total revenue within the month: "+sim.targeted_month+" "+str(sum(df["Revenue"])))

