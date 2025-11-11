import math

import typer

app = typer.Typer()


def get_minimal_k(p: float, tau: float) -> float:
    if not 0 < p < 1:
        raise ValueError("p должна быть в интервале (0, 1)")

    if tau <= 0:
        raise ValueError("τ должно быть положительным")

    return -math.log(1.0 - p) / tau


def get_growth_factor(t: float, tau: float) -> float:
    if t <= 0:
        raise ValueError("t должно быть положительным")
    return (t + tau) ** 2 / t ** 2


def get_remembered_percent(k: int, tau: float) -> float:
    return (1.0 - math.exp(-k * tau)) * 100


def get_k_from_theory_condition(tau: float) -> float:
    return 5 / tau


@app.command()
def main(t: float = 59.0, tau: float = 1.0, p: float = 0.95):
    print(f"Входные параметры:\n"
          f"\t• время начала комплексирования t={t} мин,\n"
          f"\t• время комплексирования τ={tau} мин,\n"
          f"\t• требуемая доля запоминания ошибки p={p}.\n")

    k = get_minimal_k(p, tau)
    print(f"Для запоминания не менее {p * 100}% ошибки определения координат положения "
          f"необходим основной параметр комплексирования k ≥ {k:.4f}.\n")

    factor = get_growth_factor(t, tau)
    print(f"Коэффициент роста ошибки за время комплексирования равен {factor:.4f}.\n")

    int_k = math.ceil(k)
    remembered = get_remembered_percent(int_k, tau)
    print(f"За время комплексирования запомнено {remembered:.4f}% ошибки, "
          f"имеющейся на начальный момент.\n")

    theory_k = get_k_from_theory_condition(tau)
    print(f"Запомненная ошибка гарантированно составляет более 99% ошибки "
          f"определения координат положения при значении k = {theory_k:.4f}.")


if __name__ == "__main__":
    app()
