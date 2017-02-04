#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests 
from bs4 import BeautifulSoup
# Модуль для добавления данных в файл
import csv
# Модуль для регулярных выражений
import re


# Чтобы посмотреть какие библиотеки установлены нужно выполнить команду 
# pip freeze

# Функции:
# def get_html():
# def get_total_pages():
# def get_page_data():
# def write_csv():
# def main():	
# # 






# _________________________________ПОЛУЧАЕМ ЮРЛ СТРАНИЦЫ___________________________________________

# Функция принимает в качестве аргумента ЮРЛ
def get_html(url):
	# в переменной r будет хранится запрос к серверу, после ее применения мы получим ответ в виде ссылки
	# response [200] и если мы хотим вывести полный код html страницы мы используем метод text.
	r = requests.get(url)
	return r.text
# __________________________________________________________________________________________________





# _____________________ПОЛУЧАЕМ СКОЛЬКО ВСЕГО СТРАНИЦ И ОБРАБАТЫВАЕМ ИХ_____________________________

def get_total_pages(html):
	soup = BeautifulSoup(html, 'lxml')
	# 2 основных метода:
	# find('div', class or id) принимает название html элемента и его класс или айди, для поиска. Возвращает объект soup(а)
	# find_all("div") выводит все div

	# Создаем объект класса , называем его pages.
	# Вызываем объект soup с методом find и указываем параметры потом фильтруем еще по
	# одному методу с ссылкой , [-1] означает взять последний элемент и получить оттуда ссылку
	# В этой переменной будет лежать ЮРЛ последнего листа в списке
	# Вот она '/sankt-peterburg/telefony?p=594&q=Iphone'
	pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
	# В этой переменной мы порежем ссылочку методом .split("=") убираем равно 
	# вот значение переменной ['/sankt-peterburg/telefony?p', '594&q', 'Iphone']
	# Нас интересует второй элемент , так что добавляем [1]
	# total_pages ='594&q'
	# Разделили (594, q)
	# Берем первый элемент [0]
	# total_pages = 594
	total_pages = pages.split('=')[1].split('&')[0]
	# Возвращаем в типе int 
	return int(total_pages)
# __________________________________________________________________________________________________






# --------------------------БЛОК ПОЛУЧЕНИЯ ДАННЫХ СО СТРАНИЦ-------------------------------


def get_page_data(html):
	soup = BeautifulSoup(html, 'lxml')
	# Получаем список всех item_table
	ads = soup.find('div' , class_='catalog-list').find_all('div', class_='item_table')

	for x in ads:
		# title , price, metro , url


		# _____________________Создаем фильтрацию по релевантности____________________________

		# Переводим тайтл в нижний регистр .lower()
		name = x.find('div', class_='description').find('h3').text.strip().lower()

		# Если название айон есть в name то делаем цикл из траев и ексептов
		if 'iphone' in name:
			try:
				# Находим все h3 в классе description без кареток \\// , используем для этого 
				# функцию strip()
				title = x.find('div', class_='description').find('h3').text.strip()
				# Если трай не удастся то делаем эксепт
			except:
				title = ''

			try:
				# Получаем цену каждого товара из листа
				price = x.find('div', class_='about').text.strip()

			except:
				price = ''	

			try:
				# Получаем метро каждого товара из листа
				metro = x.find('div', class_='data').find_all('p')[-1].text.strip()
			except:
				metro = ''	

			# получаем ЮРЛ каждого элемента из листа файнд
			try:
				url = 'https://www.avito.ru' + x.find('div', class_='description').find('h3').find('a').get('href')
			except:
				url = ''

			# Упаковываем все данные в один контейнер (переменную)
			data = {"title" : title , "price" : price, "metro":metro, "url":url}

			# Функция для записи в файл
			write_csv(data)

		else:
			continue

# _________________________________________________________________________________________________









# _________________ФИНАЛЬНАЯ ФУНКЦИЯ, СОЗДАЕТ ФАЙЛ С РАЗБРОСОМ ДАННЫХ ПО ЯЧЕЙКАМ____________________

# Добавляем в конец файла новые данные 
def write_csv(data):
	with open('avito.csv', 'a') as f:
		writer = csv.writer(f)
		# Создаем кортежи для отображения
		writer.writerow((data['title'], data['price'], data['metro'], data['url']))

# __________________________________________________________________________________________________






# _______________________________________MAIN FUNCTION______________________________________________

def main():
	url = 'https://www.avito.ru/sankt-peterburg/telefony?p=1&q=Iphone'

	base_url = 'https://www.avito.ru/sankt-peterburg/telefony?'
	page_part = 'p=' # Это динамическая часть, будем менять значение p
	# Добавим переменную в основную функцию 
	total_pages = get_total_pages(get_html(url))
	# Это запрос
	query_part = '&q=Iphone'

	for i in range(1,3):
			# Получаем
			# https://www.avito.ru/sankt-peterburg/telefony?p=1&q=Iphone
			# https://www.avito.ru/sankt-peterburg/telefony?p=2&q=Iphone
			url_gen = base_url + page_part + str(i) + query_part
			# Обрабатываем ссылку получением html кода
			# в html лежит код двух страниц
			html = get_html(url_gen)

			get_page_data(html)



# __________________________________________________________________________________________________




# Создание точки входа в программу
if __name__ == '__main__':
	main()
