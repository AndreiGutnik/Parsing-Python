import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://auto.ria.com/newauto/marka-volkswagen/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         'Chrome/90.0.4430.85 Safari/537.36', 'accept': '*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='proposition_link')
    cars = []
    for item in items:
        uah_prace = item.find('span', class_='size16')
        if uah_prace:
            uah_prace = uah_prace.get_text(strip=True)
        else:
            uah_prace = 'Точную цену уточняйте!'
        cars.append({
            'title': item.find('span', class_='link').get_text(strip=True),
            'link': HOST + item.get('href'),
            'usd_prace': item.find('span', class_='green bold size22').get_text(strip=True),
            'uah_prace': uah_prace,
            'city': item.find('span', class_='item region').get_text(strip=True),
        })
    return cars

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка','Ссылка','Цена в USD','Цена в UAH','Город'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_prace'], item['uah_prace'], item['city']])




def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1,pages_count+1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params = {'page':page})
            cars.extend(get_content(html.text))
            #cars = get_content(html.text)
        #print(cars)
        #print(len(cars))
        save_file(cars, FILE)
        print(f'\nПарсинг успешно завершен!\nПолучено {len(cars)} автомобилей')
        input(f'\nХотите открыть полученный файл {FILE}?')
        os.startfile(FILE)
    else:
        print('Error')

parse()