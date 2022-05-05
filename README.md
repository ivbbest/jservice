# Реализовать веб-сервис на Django с использованием REST API

## Задача

1. Создать веб-сервис, который принимает POST запросом количество вопросов, которые запрашиваются с публичного API https://jservice.io/api/random?count=1. Все вопросы сохраняются в базу данных. Ответ на POST запрос будет содержать предпоследний вопрос, либо пустой объект при его отсутствии.
2. Полученные ответы должны сохраняться в базе данных из п. 1, причем сохранена должна быть как минимум следующая информация (название колонок и типы данный можете выбрать сами, также можете добавлять свои колонки): 1. ID вопроса, 2. Текст вопроса, 3. Текст ответа, 4. - Дата создания вопроса. В случае, если в БД имеется такой же вопрос, к публичному API с викторинами должны выполняться дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины.
3. С помощью Docker (предпочтительно - docker-compose) развернуть образ с любой опенсорсной СУБД (предпочтительно - PostgreSQL).

## Использование Docker

### Установка Docker.
Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

### Запуск проекта.
Склонируйте репозиторий `git clone https://github.com/ivbbest/jservice.git` в текущую папку.

### Настройка проекта

Создайте `.env` файл в корне репозитория:

```
      - DEBUG=1
      - POSTGRES_NAME=NAME
      - POSTGRES_USER=USER
      - POSTGRES_PASSWORD=PASSWORD
      - SECRET_KEY=SECRET_KEY
```
Пример `.env`:

```
      - DEBUG=1
      - POSTGRES_NAME=jservice_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=1234
      - SECRET_KEY=SECRET_KEY
```

Внесите при необходимости корректировки в переменные окружения.


### Сборка образов и запуск контейнеров

В корне репозитория выполните команду:

```bash
docker-compose up -d --build
```

При первом запуске данный процесс может занять несколько минут.

### Накатите миграции
```bash
docker-compose exec web python manage.py migrate
```

### Остановка контейнеров

Для остановки контейнеров выполните команду:

```bash
docker-compose stop
```

### Инициализация проекта

Команды выполняются внутри контейнера приложения:

```bash
docker-compose exec app bash
```

#### Пример запроса через curl:

```bash
curl --header "Content-Type: application/json" --request POST --data '{"questions_num":3}'  http://localhost:5000
```

Примечание: число questions_num не должно превышать 100

#### Пример запроса через Postman

Отправьте POST запрос по адресу http://127.0.0.1:8000/api/question/ с телом == кол-ву запросов к вышеуказанному [API сервису](https://jservice.io/api/random?count=1):
```
{"questions_num": int}
```
В ответ придет предыдущей сохранённый вопрос для викторины. В случае его отсутствия - пустой объект.

### База данных

#### Показать список всех записей таблицы question:
```bash
SELECT * FROM question;
```

#### Вывести количество всех записей в таблице question:
```bash
SELECT COUNT(*) FROM question;
```

#### Удалить все записи из таблицы question:
```bash
TRUNCATE TABLE question;
```
