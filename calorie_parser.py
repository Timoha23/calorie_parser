import csv
import time
from random import choice

import requests
from bs4 import BeautifulSoup


# создаем csv с заголовками
with open("result.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        (
            "Название",
            "Энергия (ккал)",
            "Белки (г)",
            "Углеводы (г)",
            "Жиры (г)"
        )
    )



LOGS = True # измени на False если не хочешь видеть процесс в консоле
PAGES_COUNT = 1000
LIMIT = 10
count_page = 1

desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']


def random_headers():
    return {'user-agent': choice(desktop_agents),'accept':'*/*'}


for _ in range(PAGES_COUNT):
    headers = random_headers()
    if LOGS is True:
        user_agent = headers['user-agent']
        print(f'Парсим страницу номер {count_page}. Выбранный юзер-агент: {user_agent}')
        if count_page % 10 == 0:
            print(f'Остановка на 5 сек. Спаршено {count_page}/{PAGES_COUNT} страниц.')
    
    if count_page % 10 == 0:
        # после каждой 10-ой спаршеной страницей останавливаемся на 5 сек
        time.sleep(5)

    url = f'https://www.tablicakalorijnosti.ru/tablitsa-produktov?page={count_page}'


    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    # собираем данные продуктов
    products_data = soup.find("md-table-container").find("tbody").find_all("tr")
    for item in products_data:
        product = item.find_all("td")
        title = product[0].text.strip().replace(',', '.')
        calories = product[1].text.strip().replace(',', '.')
        proteins = product[2].text.strip().replace(',', '.')
        carbohydrates = product[3].text.strip().replace(',', '.')
        fats = product[4].text.strip().replace(',', '.')

        with open("result.csv", "a", encoding="utf-8-sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )
    
    count_page += 1
