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


if __name__ == "__main__":
    loader = FlightDataLoader("flight.csv")
    data = loader.load()
    print(data)
