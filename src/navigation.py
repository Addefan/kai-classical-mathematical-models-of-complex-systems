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
