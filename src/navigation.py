from abc import ABC, abstractmethod

import numpy as np


class NavigationSystem(ABC):
    def __init__(self, x0, z0):
        self.x = x0
        self.z = z0

        self.history = {
            "x": [x0],
            "z": [z0],
            "error": [0],
        }

    @abstractmethod
    def update(self, inputs, dt):
        ...

    def get_trajectory(self):
        return self.history["x"], self.history["z"]


class DeadReckoningNavigationSystem(NavigationSystem):
    def update(self, inputs, dt):
        psi = np.radians(inputs["psi"])
        v = inputs["v"]
        w = inputs["w"]
        omega = np.radians(inputs["omega"])
        alpha = np.radians(inputs["alpha"])

        self.x += (v * np.cos(psi) + w * np.cos(omega)) * np.cos(alpha) * dt
        self.z += (v * np.sin(psi) + w * np.sin(omega)) * np.cos(alpha) * dt

        self.history["x"].append(self.x)
        self.history["z"].append(self.z)

        return self.x, self.z


class PositionFixNavigationSystem(DeadReckoningNavigationSystem):
    def __init__(self, x0, z0, k=0.05, cycle_period=1200, visibility_time=60):
        super().__init__(x0, z0)
        self.k = k
        self.cycle_period = cycle_period
        self.visibility_time = visibility_time

        self.timer = 0.0

    def update(self, inputs, dt):
        super().update(inputs, dt)

        self.timer += dt
        cycle_time = self.timer % self.cycle_period
        is_gps_available = cycle_time > (self.cycle_period - self.visibility_time)

        if is_gps_available:
            gps_x = inputs["x"]
            gps_z = inputs["z"]

            self.x += self.k * (gps_x - self.x)
            self.z += self.k * (gps_z - self.z)

            self.history["x"][-1] = self.x
            self.history["z"][-1] = self.z

        return self.x, self.z
