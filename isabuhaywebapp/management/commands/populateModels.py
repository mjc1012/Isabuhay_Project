from django.core.management.base import BaseCommand
from isabuhaywebapp.models import *
class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        model = Promo(uploads=1, price=10.00)
        model.save()
        model = Promo(uploads=5, price=45.00)
        model.save()
        model = Promo(uploads=10, price=80.00)
        model.save()
        model = Promo(uploads=25, price=200.00)
        model.save()