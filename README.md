# Первоначальные настройки
Создать .env файл в корневой директории проекта с содержимым
```
POSTGRES_DB = example_bd
POSTGRES_USER = example_bd_user
POSTGRES_PASSWORD = example_bd_password
MINIO_ROOT_USER = example_minio_user
MINIO_ROOT_PASSWORD = example_minio_password
RABBITMQ_DEFAULT_USER = example_rabbit_user
RABBITMQ_DEFAULT_PASS = example_rabbit_password
AWS_ACCESS_KEY_ID = example_id
AWS_SECRET_ACCESS_KEY = example_key
AWS_STORAGE_BUCKET_NAME = example_bucket
```
Данные из примера нужно заменить на свои
# Запуск приложения
С помощью консоли перейти в корневую директорию и выполнить
```
docker-compose up
```
# Работа с приложением
1. Тесты вызываются с помощью
```
docker exec -it <container_name_or_id> python -m pytest notinder
```
2. Создать администратора с помощью
```
docker exec -it <container_name_or_id> python notinder/manage.py create_super_user --username=admin --email=myemail@example.com --password=1234
```
3. Админ панель находится на http://127.0.0.1:8000/admin
3. Тесты вызываются с помощью
```
docker exec -it <container_name_or_id> python -m pytest notinder
```