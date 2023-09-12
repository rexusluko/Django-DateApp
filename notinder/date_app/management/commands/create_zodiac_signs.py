from date_app.models import ZodiacSign
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create ZodiacSign entries'

    def handle(self, *args, **kwargs):
        zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius',
                        'Capricorn', 'Aquarius', 'Pisces']

        for sign in zodiac_signs:
            ZodiacSign.objects.create(name=sign)

        self.stdout.write(self.style.SUCCESS('Successfully created ZodiacSign entries'))