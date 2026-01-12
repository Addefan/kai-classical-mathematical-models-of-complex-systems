import numpy as np

from data import FlightDataLoader, SensorSuite
from navigation import DeadReckoningNavigationSystem
from navigation import PositionFixNavigationSystem
from results import plot_results


def run_simulation(file_path="flight.csv"):
    loader = FlightDataLoader(file_path)
    data = loader.load()
    sensors = SensorSuite()
    dr_system = DeadReckoningNavigationSystem(data["x"][0], data["z"][0])
    pf_system = PositionFixNavigationSystem(data["x"][0], data["z"][0], cycle_period=400, visibility_time=40)

    for i in range(1, len(data["t"])):
        dt = data["t"][i] - data["t"][i - 1]
        measurements = sensors.read_sensors({key: data[key][i] for key in data}, dt)

        for system in (dr_system, pf_system):
            current_x, current_z = system.update(measurements, dt)
            error = np.sqrt((current_x - data["x"][i]) ** 2 + (current_z - data["z"][i]) ** 2)
            system.history["error"].append(error)

    plot_results(data, dr_system, pf_system)


if __name__ == "__main__":
    run_simulation()
