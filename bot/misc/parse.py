# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup


def parse_table(table):
    rows = []
    for row in table.findAll('tr'):
        is_empty = False
        for cell in row.findAll('td'):
            if cell.text == ' ':
                is_empty = True
                break
        if not is_empty:
            rows.append(row)
    return rows


def get_data(rows):
    data = {}
    key = 0
    for row in rows:
        for i, cell in enumerate(row.findAll('td')):
            if i == 0:
                key = cell.text
                data[key] = {}
            elif i == 1:
                text = cell.text
                text = f'{text[0:5]} — {text[5:]}'
                data[key]['hours'] = text
            elif i == 2:
                text_array = str(cell).split('<br/>')
                data[key]['is_remote'] = 'remote_work' in text_array[0]
                data[key]['subject'] = text_array[1]
                data[key]['lecturer'] = text_array[3].split('<')[0].lstrip().rstrip()
                url = re.search(r'((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)',
                                str(cell))
                if url:
                    data[key]['url'] = url.group()
                else:
                    data[key]['url'] = None
    return data

def get_schedule(offset=0):
    url = 'https://dekanat.nung.edu.ua/cgi-bin/timetable.cgi?n=700&group=6194'
    r = requests.post(url)

    soup = BeautifulSoup(r.content, 'html5lib')

    tables = soup.findAll('table')
    rows = parse_table(tables[offset])
    data = get_data(rows)
    return data