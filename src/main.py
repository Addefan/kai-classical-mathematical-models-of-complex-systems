import sys

from model import train, predict


def main(input_csv="statistics.csv"):
    year, week = map(int, input("Введите год и неделю для предсказания через пробел: ").split())

    model = train(input_csv)
    prediction = predict(model, year, week)

    print(f"\nПрогноз заболеваемости на {week} неделю {year} года: {prediction:.1f}")


if __name__ == "__main__":
    input_csv = "statistics.csv"
    if len(sys.argv) > 1:
        input_csv = sys.argv[1]

    main(input_csv)
