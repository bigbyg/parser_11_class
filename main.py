import requests
from bs4 import BeautifulSoup
import datetime
import csv
import time
import json


def get_books():
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")
    soup, header = get_html_text()
    genre = soup.find('h1', class_='genre-name').text

    save_csv(cur_time, genre)

    soup, header = get_html_text()

    page_count = int(soup.find('div', class_='pagination-numbers').find_all('a')[-1].text)
    books_data = []


    for page in range(1, page_count + 1):
        url = f'https://www.labirint.ru/genres/2308/?page={page}'
        responce = requests.get(url=url, headers=header)
        soup = BeautifulSoup(responce.text, 'html.parser')
        books_items = soup.find_all('div', class_='genres-carousel__item')
        for book in books_items:
            try:
                book_title = book.find('span', class_='product-title').text.strip()
            except:
                book_title = 'Нет названия книги'

            try:
                book_author = book.find('div', class_='product-author').text.strip()
            except:
                book_author = 'Нет автора книги'

            try:
                book_price = book.find('span', class_='price-val').text.strip()
            except:
                book_price = 'Нет ценника'

            try:
                book_publishment = book.find('a', class_='product-pubhouse__pubhouse').text.strip()
            except:
                book_publishment = 'Нет издательства'

            try:
                book_cell = book.find('span', class_='card-label__text card-label__text_turned').text.strip()
            except:
                book_cell = 'Нет скидки'


            books_data.append(
                {
                    'book_title': book_title,
                    'book_author': book_author,
                    'book_publishment': book_publishment,
                    'book_price': book_price,
                    'book_cell': book_cell
                }
            )
            with open(f'labitint_{cur_time}_{genre}.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        book_title,
                        book_author,
                        book_publishment,
                        book_price,
                        book_cell
                    )
                )
        print(str(page) + f'/{page_count}-страница')
        time.sleep(1)
    save_json(books_data, cur_time, genre)




def get_html_text():
    url = 'https://www.labirint.ru/genres/2308/'
    header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.2.1495 Yowser/2.5 Safari/537.36'
    }
    responce = requests.get(url=url, headers=header).text
    soup = BeautifulSoup(responce, 'html.parser')
    return soup, header


def save_json(books_data, cur_time, genre):
    with open(f'labirint_{cur_time}_{genre}.json', 'w', encoding='utf-8') as file:
        json.dump(books_data, file, indent=4, ensure_ascii=False)


def save_csv(cur_time, genre):
    with open(f'labitint_{cur_time}_{genre}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Название книги',
                'Автор книги',
                'Издательство',
                'Цена',
                'Скидка на книгу',
                'Наличие'
            )
        )

if __name__ == '__main__':
    get_books()
