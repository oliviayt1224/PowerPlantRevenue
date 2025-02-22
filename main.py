from functions import *

if __name__ == "__main__":
    sim = Simulation()
    print("To use the Power Plant Revenue Simulator, here is a intro of the methodology this program uses. \n"
          "Would you like to skip it (Yes/No)?")
    intro_skip = input()
    if intro_skip == "No":
        sim.intro()

    sim.variable_selection()
    sim.calculate_revenue()
