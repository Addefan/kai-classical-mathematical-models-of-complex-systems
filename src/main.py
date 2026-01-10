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

        current_x_dr, current_z_dr = dr_system.update(measurements, dt)
        error_dr = np.sqrt((current_x_dr - data["x"][i]) ** 2 + (current_z_dr - data["z"][i]) ** 2)
        dr_system.history["error"].append(error_dr)

        current_x_pf, current_z_pf = pf_system.update(measurements, dt)
        error_pf = np.sqrt((current_x_pf - data["x"][i]) ** 2 + (current_z_pf - data["z"][i]) ** 2)
        pf_system.history["error"].append(error_pf)

    plot_results(data, dr_system, pf_system)


if __name__ == "__main__":
    run_simulation()
