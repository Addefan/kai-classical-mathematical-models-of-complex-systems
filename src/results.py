from functools import wraps

import matplotlib.pyplot as plt


def plot_results(data, dr_system=None):
    plt.figure(figsize=(16, 12))
    plot_trajectory(data, dr_system)
    plot_x(data, dr_system)
    plot_z(data, dr_system)
    plot_error(data, dr_system)
    plt.show()


def plot(nrows, ncols, title, xlabel, ylabel):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            fig = plt.gcf()
            if not hasattr(fig, "_plot_idx"):
                fig._plot_idx = 0
            fig._plot_idx += 1

            plt.subplot(nrows, ncols, fig._plot_idx)
            result = func(*args, **kwargs)
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.legend()
            plt.grid(True)
            return result

        return wrapper

    return decorator


@plot(2, 2, "Ошибка определения места положения", "Время, с", "Ошибка, м")
def plot_error(data, dr_system):
    if dr_system is not None:
        plt.plot(data["t"], dr_system.history["error"], "r", label="Без комплексирования")


@plot(2, 2, "Координата X во времени", "Время, с", "Координата X, м")
def plot_x(data, dr_system):
    plt.plot(data["t"], data["x"], "k--", label="Со спутника")

    if dr_system is not None:
        dr_x, _ = dr_system.get_trajectory()
        plt.plot(data["t"], dr_x, "r", label="Без комплексирования")


@plot(2, 2, "Координата Z во времени", "Время, с", "Координата Z, м")
def plot_z(data, dr_system):
    plt.plot(data["t"], data["z"], "k--", label="Со спутника")

    if dr_system is not None:
        _, dr_z = dr_system.get_trajectory()
        plt.plot(data["t"], dr_z, "r", label="Без комплексирования")


@plot(2, 2, "Траектория полета", "Координата X, м", "Координата Z, м")
def plot_trajectory(data, dr_system):
    plt.plot(data["x"], data["z"], "k--", label="Со спутника")

    if dr_system is not None:
        dr_x, dr_z = dr_system.get_trajectory()
        plt.plot(dr_x, dr_z, "r", label="Без комплексирования")
