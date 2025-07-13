import os
import glob
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Загружает все места из JSON файлов в указанной папке'

    def add_arguments(self, parser):
        parser.add_argument(
            'folder_path',
            type=str,
            help='Путь к папке с JSON файлами'
        )
        
        parser.add_argument(
            '--force',
            action='store_true',
            help='Перезаписать данные мест, если они уже существуют'
        )

    def handle(self, *args, **options):
        folder_path = options['folder_path']
        force = options['force']
        
        if not os.path.exists(folder_path):
            self.stderr.write(
                self.style.ERROR(f'Папка не найдена: {folder_path}')
            )
            return
        
        json_pattern = os.path.join(folder_path, '*.json')
        json_files = glob.glob(json_pattern)
        
        if not json_files:
            self.stderr.write(
                self.style.ERROR(f'JSON файлы не найдены в папке: {folder_path}')
            )
            return
        
        total_files = len(json_files)
        self.stdout.write(f'Найдено {total_files} JSON файлов для загрузки')
        
        success_count = 0
        error_count = 0
        
        for i, json_file in enumerate(json_files, 1):
            filename = os.path.basename(json_file)
            self.stdout.write(f'\n[{i}/{total_files}] Загрузка файла: {filename}')
            
            try:
                call_command('load_place', json_file, force=force, verbosity=0)
                success_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Успешно загружено: {filename}')
                )
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'✗ Ошибка загрузки {filename}: {e}')
                )
        
        self.stdout.write(f'\n' + '='*50)
        self.stdout.write(f'Загрузка завершена!')
        self.stdout.write(f'Успешно загружено: {success_count}')
        self.stdout.write(f'Ошибок: {error_count}')
        self.stdout.write(f'Всего файлов: {total_files}')
        
        if error_count == 0:
            self.stdout.write(
                self.style.SUCCESS('Все файлы успешно загружены!')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Загрузка завершена с {error_count} ошибками.')
            ) 