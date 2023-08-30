from django.core.management.base import BaseCommand
from date_app.models import Compatibility, ZodiacSign

class Command(BaseCommand):
    help = 'Creates compatibility combinations with a weight of 1'

    def handle(self, *args, **options):
        zodiac_signs = ZodiacSign.objects.all()

        compatibilities_created = 0
        for i, sign1 in enumerate(zodiac_signs):
            for sign2 in zodiac_signs[i + 1:]:
                Compatibility.objects.create(sign1=sign1, sign2=sign2, weight=1)
                compatibilities_created += 1

        for sign in zodiac_signs:
            Compatibility.objects.create(sign1=sign, sign2=sign, weight=1)
            compatibilities_created += 1

        self.stdout.write(self.style.SUCCESS(f'Created {compatibilities_created} compatibilities'))