import datetime

from Airport import Airport
from Simulation import Simulation

if __name__ == "__main__":
    airport = Airport(num_runways=3)
    sim = Simulation(airport, simulation_hours=24)
    sim.run()