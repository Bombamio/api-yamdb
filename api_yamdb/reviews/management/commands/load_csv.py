import csv
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from reviews.models import Category, Comment, Genre, Review, Title


DIR_CSV_FILES = Path(settings.STATICFILES_DIRS[0]) / 'data'

CURRENT_FORMAT_DATE = '%Y-%m-%dT%H:%M:%S.%fZ'


class Command(BaseCommand):
    """Импорт данных из csv файлов."""

    help = 'Импортирует данные из CSV в модель MyModel'

    def handle(self, *args, **kwargs):
        """Основная команда выполнения загрузки."""
        self.load_categories_genre(filename='category.csv',
                                   model_name='Категория', model=Category)
        self.load_categories_genre(filename='genre.csv',
                                   model_name='Жанр', model=Genre)
        self.load_titles(filename='titles.csv',
                         model_name='Произведения', model=Title)
        self.load_users(filename='users.csv',
                        model_name='Пользователи', model=get_user_model())
        self.load_review(filename='review.csv',
                         model_name='Отзывы', model=Review)
        self.load_comments(filename='comments.csv',
                           model_name='Комментарии', model=Comment)
        self.load_genre_title(filename='genre_title.csv')

    def process_csv(self, filename, process_row_callback, model_name):
        """Общий метод для обработки CSV файлов."""
        file_path = DIR_CSV_FILES / filename
        created_count = 0
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    process_row_callback(row)
                    created_count += 1
                except IntegrityError as e:
                    self.stdout.write(self.style.WARNING(
                        f'{model_name} с id={row.get("id")} уже'
                        f'существует или ошибка целостности: {e}'
                    ))
                except ValueError as e:
                    self.stdout.write(self.style.WARNING(
                        f'Некорректный формат данных для id={row.get("id")}:'
                        f'{e}'
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Ошибка при обработке строки: {row}. Ошибка: {e}'
                    ))
        self.stdout.write(self.style.SUCCESS('Успешно импортировано: '
                                             f'{created_count} {model_name}'))

    def load_categories_genre(self, filename, model_name, model):
        """Загрузка категорий и жанров."""
        def process_row(row):

            model.objects.update_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],)

        self.process_csv(filename, process_row, model_name)

    def load_titles(self, filename, model_name, model):
        """Загрузка произведений."""
        def process_row(row):

            category = Category.objects.get(id=row['category'])

            model.objects.update_or_create(
                id=int(row['id']),
                name=row['name'],
                year=int(row['year']),
                description=row.get('description', ''),
                category=category,
            )

        self.process_csv(filename, process_row, model_name)

    def load_users(self, filename, model_name, model):
        """Загрузка пользователей."""
        def process_row(row):
            user_obj, created = model.objects.update_or_create(
                id=int(row['id']),
                defaults={
                    'username': row['username'],
                    'email': row['email'],
                    'first_name': row.get('first_name', ''),
                    'last_name': row.get('last_name', ''),
                    'bio': row.get('bio', ''),
                }
            )

            group, _ = Group.objects.get_or_create(name=row.get('role', ''))
            user_obj.groups.clear()
            user_obj.groups.add(group)

        self.process_csv(filename, process_row, model_name)

    def load_review(self, filename, model_name, model):
        """Загрузка отзывов."""
        def process_row(row):
            # Получаем значения из строки
            review_id = int(row['id'])
            text = row['text']
            score = int(row['score'])
            author_id = int(row['author'])
            title_id = int(row['title_id'])
            pub_date_str = row.get('pub_date', '')

            # Получаем связанные объекты
            author_obj = get_user_model().objects.get(id=author_id)
            title_obj = Title.objects.get(id=title_id)

            if not author_obj:
                self.stdout.write(self.style.WARNING(
                    (f'Автор с id={author_id} не найден '
                     f'для отзыва id={review_id}.')
                ))
            if not title_obj:
                self.stdout.write(self.style.WARNING(
                    (f'Произведение с id={title_id}'
                     f'не найдено для отзыва id={review_id}.')
                ))

            # Обновляем или создаем отзыв
            model.objects.update_or_create(
                id=review_id,
                defaults={
                    'text': text,
                    'score': score,
                    'author': author_obj,
                    'title': title_obj,
                    'pub_date': datetime.strptime(pub_date_str,
                                                  CURRENT_FORMAT_DATE)
                }
            )
        self.process_csv(filename, process_row, model_name)

    def load_comments(self, filename, model_name, model):
        """Загрузка комментарие."""
        def process_row(row):
            comment_id = int(row['id'])
            text = row['text']
            author_id = int(row['author'])
            review_id = int(row['review_id'])
            pub_date_str = row.get('pub_date', '')

            author_obj = get_user_model().objects.get(id=author_id)
            review_obj = Review.objects.get(id=review_id)

            if not author_obj:
                self.stdout.write(self.style.WARNING(
                    (f'Автор с id={author_id} не'
                     f'найден для комментария id={comment_id}.')
                ))
            if not review_obj:
                self.stdout.write(self.style.WARNING(
                    (f'Отзыв с id={review_id} не найден'
                     f'для комментария id={comment_id}.')
                ))

            if author_obj and review_obj:
                model.objects.update_or_create(
                    id=comment_id,
                    defaults={
                        'text': text,
                        'author': author_obj,
                        'review': review_obj,
                        'pub_date': datetime.strptime(pub_date_str,
                                                      CURRENT_FORMAT_DATE)
                    }
                )
        self.process_csv(filename, process_row, model_name)

    def load_genre_title(self, filename):
        """Обработка связей через модель GenreTitle."""

        def process_row(row):
            title_id = int(row['id'])
            genre_id = int(row['genre_id'])

            try:
                title_obj = Title.objects.get(id=title_id)
            except Title.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f'Title с id={title_id} не найден.'
                ))
                return

            try:
                genre_obj = Genre.objects.get(id=genre_id)
            except Genre.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f'Genre с id={genre_id} не найден.'
                ))
                return

            title_obj.genre.add(genre_obj)

        self.process_csv(filename, process_row, 'Жанры произведений')
