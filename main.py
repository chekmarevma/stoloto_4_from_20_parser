# ---------------STOLOTO-----------------
import lxml
import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import random


def parse_data(finish: int, start: int=28, data: list=[]):
    '''Парсинг данных по проведенным тиражам, формирование отчета в JSON'''
    print('Обновление данных...')    
    for i in tqdm(range(start + 1, int(finish) + 1)):
        url = f'https://www.stoloto.ru/4x20/archive/{i}'
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'lxml')
        LEFT = [i.text for i in soup.find_all('p', class_='number')[:4]]
        RIGHT = [i.text for i in soup.find_all('p', class_='number')[4:]]
        DATTE = ' '.join(soup.find('div', id='content').find('h1').text.split(', ')[-1].split()[0:3])
        TIMME = soup.find('div', id='content').find('h1').text.split()[-1]
        category_1 = int(soup.find('div', class_='col prizes').find('tbody').find_all('tr')[0].find_all_next('td')[3].text.replace('\xa0', ''))
        category_2 = int(soup.find('div', class_='col prizes').find('tbody').find_all('tr')[1].find_all_next('td')[3].text.replace('\xa0', ''))
        category_3 = int(soup.find('div', class_='col prizes').find('tbody').find_all('tr')[2].find_all_next('td')[3].text.replace('\xa0', ''))
        category_4 = int(soup.find('div', class_='col prizes').find('tbody').find_all('tr')[3].find_all_next('td')[3].text.replace('\xa0', ''))
        category_5 = int(soup.find('div', class_='col prizes').find('tbody').find_all('tr')[4].find_all_next('td')[3].text.replace('\xa0', ''))
        category_6 = int(soup.find('div', class_='col prizes').find('tbody').find_all('tr')[5].find_all_next('td')[3].text.replace('\xa0', ''))
        category_7 = int(soup.find('div', class_='col prizes').find('tbody').find_all('tr')[6].find_all_next('td')[3].text.replace('\xa0', ''))
        category_8 = int(soup.find('div', class_='col prizes').find('tbody').find_all('tr')[7].find_all_next('td')[3].text.replace('\xa0', ''))
        category_9 = int(soup.find('div', class_='col prizes').find('tbody').find_all('tr')[8].find_all_next('td')[3].text.replace('\xa0', ''))
        category_10 = int(soup.find('div', class_='col prizes').find('tbody').find_all('tr')[9].find_all_next('td')[3].text.replace('\xa0', ''))
        category_11 = int(soup.find('div', class_='col prizes').find('tbody').find_all('tr')[10].find_all_next('td')[3].text.replace('\xa0', ''))
        category_12 = int(soup.find('div', class_='col prizes').find('tbody').find_all('tr')[11].find_all_next('td')[3].text.replace('\xa0', ''))

        dic = {'Circulation': i, 'date': DATTE, 'time': TIMME, 'cost': category_11, 'left': ' '.join(LEFT), 'right': ' '.join(RIGHT),
               '4 x 4': category_1, '4 X 3 and 3 X 4': category_2, '4 X 2 and 3 X 4': category_3, '4 X 1 and 1 X 4': category_4,
               '4 X 0 and 0 X 4': category_5, '3 X 3': category_6, '3 X 2 and 2 X 3': category_7, '3 X 1 and 1 X 3': category_8,
               '3 X 0 and 0 X 3': category_9, '2 X 2': category_10, '2 X 1 and 1 X 2': category_11, '2 X 0 and 0 X 2': category_12}
        data.append(dic)
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    go(data)


def go(base: list):
    '''Ввод значений лотереи, проверка возможных выигрышей'''
    answer = input('Ввести значения - 1. Случайные значения - любая клавиша.')
    if answer == '1':
        print('Левое поле:')
        left = set(map(int, input().split()))
        print('Правое поле:')
        right = set(map(int, input().split()))
    else:
        left = set(random.sample(range(1, 21), k=4))
        right = set(random.sample(range(1, 21), k=4))
    money = 0
    prize = 0
    luck = (2, 3, 4)
    for i in base:
        money += i['cost']
        l = set(map(int, i['left'].split()))
        r = set(map(int, i['right'].split()))
        if len(l & left) in luck or len(r & right) in luck:
            rez = f'{len(l & left)} X {len(r & right)}'
            for j in i.keys():
                if rez in j.upper() or rez == j:
                    prize += i[j]
    print(f'Потрачено: {money} рублей')
    print(f'Выиграно: {prize} рублей')
    print(f'Доход: {prize - money} рублей')


print(f'  _     _   _     _   _  \n / \   / \ / \   / \ / \ \n( 4 ) ( и | з ) ( 2 | 0 )\n \_/   \_/ \_/   \_/ \_/ \n')
url = 'https://www.stoloto.ru/4x20/archive'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
last = soup.find('div', class_='data drawings_data').find('div', class_='month').find('div', class_='draw').text

try:
    print('Загрузка данных...')
    with open('data.json', 'r', encoding='utf-8') as file:
        base = json.load(file)
except:
    print('База данных отсутствует')
    parse_data(last)
    with open('data.json', 'r', encoding='utf-8') as file:
        base = json.load(file)
finally:
    last_json = base[-1]['Circulation']
    if last_json < int(last):
        print('Требуется обновление данных')
        parse_data(last, last_json, base)
    else:
        go(base)
