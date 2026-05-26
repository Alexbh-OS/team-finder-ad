# TeamFinder 

**TeamFinder** — платформа ,которая позволяет пользователям создавать IT-проекты и находить участников в команду.

## Функциональность

- Регистрация и авторизация пользователей
- Создание, редактирование и удаление проектов
- Добавление навыков к проектам
- Поиск проектов по навыкам
- Добавление проектов в избранное



## Технологический стек

* **Backend:** Python 3.12, Django 5.x
* **Database:** PostgreSQL
* **Infrastructure:** Docker, Docker Compose
* **Frontend:** HTML5, CSS3 (Flexbox/Grid), JavaScript (AJAX)
* **Environment:** Python-dotenv, Decouple


## Запуск проекта

### 1\. Подготовка окружения

- git clone<url_репозитория>  Клонируйте репозиторий через HTTPS или SSH

- python -m venv venv - Создайте виртуальное окружение 

- source venv/bin/activate (для Linux/Mac) - Активируйте виртуальное окружение 

  venv\\Scripts\\activate (для Windows)

- pip install -r requirements.txt -  Установите необходимые зависимости:



### 2\. Настройка переменных среды (.env)

Создайте файл .env в корневой папке проекта и заполните его по примеру:

DJANGO\_SECRET\_KEY=ваш\_секретный\_ключ

DJANGO\_DEBUG = True

ALLOWED\_HOSTS = 127.0.0.1,localhost

POSTGRES\_DB = team\_finder
POSTGRES\_USER = postgres

POSTGRES\_PASSWORD = postgres
POSTGRES\_HOST = localhost
POSTGRES\_PORT = 5432


### 3\. Запуск базы данных

Проект использует PostgreSQL. Запустите её через Docker Compose:

- docker compose up -d


### 4\. Применение миграций и запуск

Создайте структуру таблиц и запустите локальный сервер разработки:

- python manage.py migrate - Создайте структуру таблиц
- python manage.py runserver - Запустите локальный сервер разработки

Проект будет доступен по адресу: http://localhost:8000


## Автор

Кондратьев Александр

Гитхаб автора: https://github.com/Alexbh-OS
Почта автора: sanyo478fin@gmail.com





