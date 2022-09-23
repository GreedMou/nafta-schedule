import requests

url = 'https://dekanat.nung.edu.ua/cgi-bin/timetable.cgi?n=701&lev=142&faculty=0&course=0&query='

r = requests.get(url)

data = r.json()['suggestions']

г