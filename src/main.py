import numpy as np

from navigation import DeadReckoningNavigationSystem
from data import FlightDataLoader, SensorSuite
from results import plot_results


def run_simulation(file_path="flight.csv"):
    loader = FlightDataLoader(file_path)
    data = loader.load()
    sensors = SensorSuite()
    dr_system = DeadReckoningNavigationSystem(data["x"][0], data["z"][0])

    for i in range(1, len(data["t"])):
        dt = data["t"][i] - data["t"][i - 1]
        measurements = sensors.read_sensors({key: data[key][i] for key in data}, dt)

        current_x, current_z = dr_system.update(measurements, dt)
        error = np.sqrt((current_x - data["x"][i]) ** 2 + (current_z - data["z"][i]) ** 2)
        dr_system.history["error"].append(error)

    plot_results(data, dr_system)


if __name__ == "__main__":
    run_simulation()
