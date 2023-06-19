# AroundRussia_backend

### Как запустить проект:

Клонировать репозиторий:
```
git clone git@github.com:Price-Aggregator/AroundRussia_backend.git
```

Перейти в ветку develop и подгрузить актуальную версию:

```
git checkout develop
git pull
```

Перейти в папку infra:
```
cd infra/
```

Создать test_env файл и заполнить его по шаблону:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<название базы данных>
POSTGRES_USER=<имя пользователя базы данных>
POSTGRES_PASSWORD=<пароль базы данных>
DB_HOST=db
DB_PORT=<порт>(по умолчанию = 5432)
TOKEN=<токен travelpayouts>
```

В этой же папке выполнить команду развертывания проекта:
```
docker-compose up -d
```

Выполнить миграции:
```
docker-compose exec backend python manage.py migrate
```

Создать суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```

Подключить статику:
```
docker-compose exec backend python manage.py collectstatic --no-input
```

(Опционально) Загрузить список городов в базу данных
```
docker-compose exec backend python manage.py fill_database_cities
```

Проект станет доступен по адресу:
```
http://127.0.0.1/
```

Для остановки проекта выполните команду:
```
docker-compose stop
```

Или воспользуйтесь комбинацией клавиш Ctrl+C в терминале с запущенным докером.

### (Опционально) Заполнение БД.

Проект поддерживает заполнение базы данных командой.

Заполняются IATA коды городов, названия городов и их координаты.

Чтобы залить данные в базу необходимо выполнить комманду:
```
docker-compose exec backend python manage.py fill_database_cities
```

### Системные требования

Версия Python:
```
Python 3.11
```

Зависимости:
```
Зависимости указаны в файле backend/requirements.txt
```

### Документация

Документация расположена по адресу:

```
http://127.0.0.1/api/docs/

```