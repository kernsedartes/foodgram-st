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
                skipped_count = 0
                errors = []

                for index, item in enumerate(data, start=1):
                    # Проверяем структуру Fixture
                    if not all(
                        key in item for key in ["model", "pk", "fields"]
                    ):
                        errors.append(
                            f"Запись #{index}: неверный формат (ожидается Fixture)"
                        )
                        skipped_count += 1
                        continue

                    fields = item["fields"]
                    if (
                        "name" not in fields
                        or "measurement_unit" not in fields
                    ):
                        errors.append(
                            f"Запись #{index}: нет 'name' или 'measurement_unit' в fields"
                        )
                        skipped_count += 1
                        continue

                    # Создаём ингредиент
                    obj, created = Ingredient.objects.get_or_create(
                        name=fields["name"],
                        measurement_unit=fields["measurement_unit"],
                    )
                    if created:
                        created_count += 1

                # Вывод результатов
                self.stdout.write(
                    self.style.SUCCESS(f"Загружено: {created_count}")
                )
                if skipped_count:
                    self.stdout.write(
                        self.style.WARNING(f"Пропущено: {skipped_count}")
                    )
                if errors:
                    self.stdout.write(self.style.ERROR("\n".join(errors)))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Файл не найден: {filepath}"))
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR("Ошибка формата JSON"))
