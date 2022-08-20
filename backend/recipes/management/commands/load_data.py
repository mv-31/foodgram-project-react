from csv import reader

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load data from csv file to DB'

    def handle(self, *args, **kwargs):
        path = 'recipes/data/ingredients.csv'
        try:
            with open(path, 'r', encoding='UTF-8') as file:
                if not file:
                    return 'Файл пуст'
                for row in reader(file):
                    if len(row) == 2:
                        Ingredient.objects.get_or_create(
                            name=row[0], measurement_unit=row[1],
                        )
        except FileNotFoundError:
            raise CommandError('Файл не найден')
        return 'Данные добавлены'
