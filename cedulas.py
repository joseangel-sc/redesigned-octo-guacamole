import requests
from bs4 import BeautifulSoup
import json

URL = 'https://www.buholegal.com/'

NAME_CLASS = 'card-header text-center'
TABLE_CLASS = 'table table-sm'


def extract_data_from_html(soup) -> dict:
    name = soup.find_all(class_=NAME_CLASS)
    name = extract_name(name)
    details = soup.find_all(class_=TABLE_CLASS)
    table_data = extract_study_details(details)
    return {**name, **table_data}


def extract_name(name_element) -> dict:
    name_and_cedula = name_element[0].text.split('\n')
    name = name_and_cedula[0].strip()
    cedula = int(name_and_cedula[1].strip().split(':')[1])
    return {'name': name, 'cedula': cedula}


def extract_study_details(table_element):
    table = table_element[0]
    rows = table.find_all('td')
    data = dict()
    state = 0
    for field_name, field_data in zip(rows[1:], rows[2:]):
        state += 1
        if state % 2 == 0:
            continue
        field_name = field_name.text.strip()
        field_data = field_data.text.strip()
        data[field_name] = field_data

    return data


def request_one(number):
    response = requests.get(f'{URL}{number}')
    return BeautifulSoup(response.content, 'html.parser')


def write_data(data_dict):
    with open('data.txt', 'a') as f:
        json.dump(data_dict, f, ensure_ascii=False)
        f.write('\n')


def get_next():
    with open('data.txt', 'r') as f:
        read = f.readlines()
    next_extract = json.loads(read[-1])['cedula'] + 1
    print(f"now it's the turn for {next_extract}")
    return next_extract


if __name__ == '__main__':
    next_page = get_next()
    while True:
        data = request_one(next_page)
        details = extract_data_from_html(data)
        write_data(details)
        next_page = get_next()
