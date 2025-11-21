import json
from django.core.management.base import BaseCommand
from store.models import StockBalance


class Command(BaseCommand):
    help = 'Экспортирует остатки товаров в JSON файл'

    def add_arguments(self, parser):
        parser.add_argument(
            'output_file',
            type=str,
            help='Файл, в который будут сохранены остатки'
        )

    def handle(self, *args, **options):
        output_file = options['output_file']

        data = []

        for stock in StockBalance.objects.select_related('product'):
            data.append({
                'product': stock.product.name,
                'quantity': stock.quantity
            })

        try:
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

                self.stdout.write(self.style.SUCCESS("Данные успешно выгружены"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка записи файла: {e}"))
