from django.core.management.base import BaseCommand
from api.models import Ingredient


class Command(BaseCommand):
    help = "Удаляет все ингредиенты из базы данных"

    def handle(self, *args, **kwargs):
        count = Ingredient.objects.count()
        Ingredient.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Удалено ингредиентов: {count}"))
