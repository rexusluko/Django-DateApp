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

docker exec -it <container_name_or_id> python -m pytest notinder

2. ? В корне start.txt который нужно скопировать в entrypoint.sh, зачем эти действия
5. docker-compose.web.command запускает скрипт bash entrypoint.sh, entrypoint.sh - не существует, нет проблем закидывать его репозиторий

4. .gitignore ожидает мержа
6. docker-compose.web.volumes смотрит на локальные файлы а не тома. Нужно отдельно статику и медиа прокидывать а не весь код бека
11. Приложения не разбиты на маленькие части, все в одном application
12. Медод api/v1/register/
12.3. По хорошему выдавать Bearer токен при регистрации
14. Методы api/v1/like/ и api/v1/dislike/ - Используется APIView вместо generics.CreateAPIView
14.2. Логику лучше описать в serializers
15. Модель CustomUser - хардкод полей first_name, last_name, last_login
16. Файл date_app.photo - Некорректное название, лучше создать новый application и/или в нем сделать utils и там описать логику