import csv
import html
import re
import sys
import time

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

BASE_URL = "https://www.influenza.spb.ru/surveillance/flu-bulletin"

retry_strategy = Retry(
    total=5,
    status_forcelist=[504],
    allowed_methods=["GET"]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session = Session()
session.mount("http://", adapter)
session.mount("https://", adapter)


def extract_incidence_rate(html_text: str):
    incidence = re.search(r"составив\s(\d+[,.]\d)\sна\s10\s000\sнаселения", html_text)
    if incidence is None:
        return None

    return float(incidence.group(1).replace(",", "."))


def fetch_bulletin(year: int, week: int):
    params = {
        "year": str(year),
        "week": f"{week:02d}"
    }

    response = session.get(BASE_URL, params=params)
    response.raise_for_status()
    time.sleep(0.5)

    incidence = extract_incidence_rate(html.unescape(response.text))
    return incidence


def _get_year_week_pairs(start_year: int, start_week: int, end_year: int, end_week: int):
    years_weeks = []

    for week in range(start_week, 53 + 1):
        years_weeks.append((start_year, week))

    for year in range(start_year + 1, end_year):
        for week in range(1, 53 + 1):
            years_weeks.append((year, week))

    for week in range(1, end_week + 1):
        years_weeks.append((end_year, week))

    return years_weeks


def fetch_statistics(start_year: int, start_week: int, end_year: int, end_week: int, output_csv="out.csv"):
    with open(output_csv, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["year", "week", "incidence"])
        writer.writeheader()

        for year, week in _get_year_week_pairs(start_year, start_week, end_year, end_week):
            incidence = fetch_bulletin(year, week)
            if incidence is None:
                print(f"Данных за {week} неделю {year} года нет.")
                continue

            row = {
                "year": year,
                "week": week,
                "incidence": incidence,
            }
            writer.writerow(row)


def main(output_csv="statistics.csv"):
    start_date = map(int, input("Введите год и неделю \033[1mначала\033[0m сбора данных через пробел: ").split())
    end_date = map(int, input("Введите год и неделю \033[1mокончания\033[0m сбора данных через пробел: ").split())
    fetch_statistics(*start_date, *end_date, output_csv=output_csv)


if __name__ == "__main__":
    output_csv = "statistics.csv"
    if len(sys.argv) > 1:
        output_csv = sys.argv[1]

    main(output_csv)
