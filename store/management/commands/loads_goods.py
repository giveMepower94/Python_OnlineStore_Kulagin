from django.core.management.base import BaseCommand
from store.models import Product, StockBalance
import json


class Command(BaseCommand):
    help = 'Загружает товары и остатки из JSON файла'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Путь к JSON файлу с товарами'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("Файл не найден"))
            return

        for item in data:
            product, created = Product.objects.get_or_create(
                name=item['name'],
                defaults={
                    'description': item.get('description', ''),
                    'price': item.get('price', 0)
                }
            )

            StockBalance.objects.update_or_create(
                product=product,
                defaults={
                    'quantity': item.get('quantity', 0)
                }
            )

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены"))
