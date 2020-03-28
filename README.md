# Парсер для выкачивания книг с сайта tululu.org и генерации html каталга

Скрипт проходится по книгам заданной категории и выкачивает файлы, изображение обложек и информацию о книгах.

## Установка
Для установки зависимостией выполните
```shell script
pip install -r requirements.txt
```

Для скачивания книг запустите и генерации html страниц запустите
```shell script
python3 ./src/app.py --start_page 50 --end_page 60
```

- `--start_page` - страница жанра с которой нужно начинать скачивание книг
- `--end_page` - страница жанра до которой (не включительно) скачивать книги. Необязательный параметр.
Если не передан - будет скачивать до конца раздела

## Настроечные аргументы
Дополнительные опциональные параметры позволяют указать названия папок для скачивания файлов книг и изображений обложек, задать URL категории и название 
json файла с информацией о книгах.

 - `--book_path` - папка для сохранения файлов книг. По умолчанию `books`
 - `--image_path` - папка для сохранения изображений обложек. По умолчанию `images`
 - `--category_url` - URL жанра книг. По умолчанию `http://tululu.org/l55/`
 - `--book_json` - название json файла в который сохраняется информация о книгах. По умолчанию `books.json`
 - `--root_path` - папка в которой будет находиться содержимое web-сайта. По умолчнию `html`
 - `--html_template_path` - Папка с шаблоном страницы с книгами. По умолчанию `template`
 - `--html_template` - название файла шаблона который используется для ганерации страниц. По умолчанию `index.html`
 - `--books_per_page` - количество книг на страницу. По умолчанию `20`

Пример строки запуска с полным набором параметров
```shell script
python3 ./src/app.py --start_page 3 --end_page 5 --book_path knigi --image_path kartinki --category_url http://tululu.org/l54/ --book_json knijki.json \
--root_path my_site --html_template_path shablony --html_template page_template --books_per_page 10
```

## Линтинг
Для проверки кода на соответствие PEP-8 выполните
```shell script
flake8 src
pycodestyle src
```
