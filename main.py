from bs4 import BeautifulSoup
from requests import get
import sqlite3
from sys import argv

def parse_price(price):
	return float(price.replace(' ', '').replace('zł', '').replace(',','.').replace('donegocjacji',''))

def parse_page(number):
	print(f'Pracuje nad stroną numer {number}.')
	page = get(f'{URL}?page={number}')
	bs = BeautifulSoup(page.content, "html.parser")
	for offer in bs.find_all('div', attrs={'data-cy': 'l-card', 'class': ['css-19ucd76']}):
		name = offer.find('h6', class_='css-v3vynn-Text eu5v0x0').get_text().strip()
		price = parse_price(offer.find('p', class_='css-wpfvmn-Text eu5v0x0').get_text())
		location = offer.find('p', class_='css-p6wsjo-Text eu5v0x0').get_text().strip().split('-')[0]
		time_added = offer.find('p', class_='css-p6wsjo-Text eu5v0x0').get_text().strip().split('-')[1]
		year = offer.find('p', class_='css-1obsecn').get_text()
		link = offer.find('a')
		cursor.execute('INSERT INTO offers VALUES(?,?,?,?,?,?)', (name, price,year, location, time_added,link['href']))

		db.commit()

URL = 'https://www.olx.pl/d/motoryzacja/samochody/suwalki/?search%5Bdist%5D=100&search%5Bfilter_float_price:from%5D=10000&search%5Bfilter_float_price:to%5D=50000&search%5Bfilter_enum_petrol%5D%5B0%5D=petrol&search%5Bfilter_float_milage:to%5D=150000&search%5Bfilter_enum_country_origin%5D%5B0%5D=pl'
db = sqlite3.connect('auta.db')
cursor = db.cursor()

if len(argv) > 1 and argv[1] == 'setup':
	cursor.execute('''CREATE TABLE offers (name TEXT, price REAL,year TEXT, city TEXT, date TEXT,URL TEXT )''')
	quit()
#python main.py setup

for page in range(10):
	parse_page(page)

db.close()

