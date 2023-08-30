from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from date_app.models import ZodiacSign  # Импортируйте модель ZodiacSign

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser with additional fields'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username')
        parser.add_argument('--email', type=str, help='Email')
        parser.add_argument('--password', type=str, help='Password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        zodiac_sign, created = ZodiacSign.objects.get_or_create(name='Admin')

        gender = 'male'
        photo_path = 'no photo'

        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            zodiac_sign=zodiac_sign,  # Передаем экземпляр знака зодиака
            gender=gender,
            photo_path=photo_path,
        )

        self.stdout.write(self.style.SUCCESS(f'Superuser {username} successfully created'))