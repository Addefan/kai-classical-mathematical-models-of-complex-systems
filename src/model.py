import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from sklearn.model_selection import train_test_split


def get_data(input_csv):
    df = pd.read_csv(input_csv)

    X = df.drop("incidence", axis=1)
    y = df["incidence"]

    return X, y


def train(input_csv="statistics.csv"):
    X, y = get_data(input_csv)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)

    model = RandomForestRegressor(n_estimators=1000)
    print("\nОбучение модели...\n")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    print("Метрики обученной модели:")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")

    return model


def predict(model, year: int, week: int):
    X = pd.DataFrame([[year, week]], columns=["year", "week"])
    pred = model.predict(X)[0]
    return float(pred)
