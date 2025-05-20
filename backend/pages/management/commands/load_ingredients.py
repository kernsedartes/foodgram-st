import json
from django.core.management.base import BaseCommand
from api.models import Ingredient


class Command(BaseCommand):
    help = "Загружает ингредиенты из JSON-файла"

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str, help="Путь к JSON-файлу")

    def handle(self, *args, **options):
        filepath = options["filepath"]
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                created_count = 0
                for item in data:
                    obj, created = Ingredient.objects.get_or_create(
                        name=item["name"],
                        measurement_unit=item["measurement_unit"],
                    )
                    if created:
                        created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Загружено ингредиентов: {created_count}"
                    )
                )
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Файл не найден: {filepath}"))
        except json.JSONDecodeError:
            self.stderr.write(
                self.style.ERROR(f"Ошибка в формате JSON: {filepath}")
            )
