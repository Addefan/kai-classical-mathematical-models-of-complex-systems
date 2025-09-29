from model import train, predict

if __name__ == "__main__":
    year, week = map(int, input("Введите год и неделю для предсказания через пробел: ").split())

    model = train("../statistics_test.csv")
    prediction = predict(model, year, week)

    print(f"\nПрогноз заболеваемости на {week} неделю {year} года: {prediction:.1f}")
