# Первоначальные настройки
## 1. Пароли и логины
Создать .env файл в корневой директории проекта с содержимым
```
POSTGRES_DB = example_bd
POSTGRES_USER = example_bd_user
POSTGRES_PASSWORD = example_bd_password
MINIO_ROOT_USER = example_minio_user
MINIO_ROOT_PASSWORD = example_minio_password
```
Данные из примера нужно заменить на свои 
## 2. Точка входа и администратор
В корневой директории проекта создать файл entrypoint.sh c помощью текстового редактора(чтобы избежать clrf) с содержимым
```
#!/bin/sh
# Apply database migrations
python notinder/manage.py makemigrations date_app
python notinder/manage.py migrate
# Create Zodiac Signs and Compatibilities
python notinder/manage.py create_zodiac_signs
python notinder/manage.py create_compatibilities
#Create minio bucket
python notinder/manage.py init_minio_bucket
# Create superuser
python notinder/manage.py create_super_user --username=admin --email=myemail@example.com --password=1234
python -m pytest notinder
# Run server
python notinder/manage.py runserver 0.0.0.0:8000
```
Данные для суперпользователя указать свои
# Запуск приложения
С помощью консоли перейти в корневую директорию и выполнить
```
docker-compose up
```
При запуске приложения
1. Проводятся все миграции баззы данных
2. В базу данных добавляются все знаки зодиака и совместимости
3. Создаётся администратор с данными из entrypoint.sh
# Работа с приложением 
Админ панель находится на http://127.0.0.1:8000/admin