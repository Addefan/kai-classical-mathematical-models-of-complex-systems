import numpy as np
import pandas as pd


class FlightDataLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = {}

    def load(self):
        df = pd.read_csv(self.filepath)

        self.data["t"] = df.iloc[:, 0].values  # время, с
        self.data["alpha"] = df.iloc[:, 1].values  # угол атаки, °
        self.data["psi"] = df.iloc[:, 2].values  # курс, °
        self.data["v"] = df.iloc[:, 3].values  # воздушная/истинная скорость, м/c
        self.data["omega"] = df.iloc[:, 4].values  # угол ветра, °
        self.data["w"] = df.iloc[:, 5].values  # скорость ветра, м/c
        self.data["x"] = df.iloc[:, 6].values  # координата X со спутника, м
        self.data["z"] = df.iloc[:, 7].values  # координата Z со спутника, м

        return self.data


class SensorSuite:
    def __init__(self, gyro_drift_rate=0.00003, gyro_noise_std=0.3, gps_noise_std=3.0):
        self.gyro_drift_rate = gyro_drift_rate
        self.gyro_noise_std = gyro_noise_std
        self.gps_noise_std = gps_noise_std
        self.current_gyro_bias = 0.0

    def read_sensors(self, data, dt):
        self.current_gyro_bias += self.gyro_drift_rate * dt
        gyro_noise = np.random.normal(0, self.gyro_noise_std)
        measured_psi = data["psi"] + self.current_gyro_bias + gyro_noise

        gps_x_noise = np.random.normal(0, self.gps_noise_std)
        gps_z_noise = np.random.normal(0, self.gps_noise_std)
        measured_x = data["x"] + gps_x_noise
        measured_z = data["z"] + gps_z_noise

        return {
            "t": data["t"],
            "alpha": data["alpha"],
            "psi": measured_psi,
            "v": data["v"],
            "omega": data["omega"],
            "w": data["w"],
            "x": measured_x,
            "z": measured_z,
        }


if __name__ == "__main__":
    loader = FlightDataLoader("flight.csv")
    data = loader.load()
    print(data)
