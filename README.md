# api_yamdb
api_yamdb

Структура проекта и приложений
api/ - Центральное приложение API:
permissions.py - общие права доступа
urls.py - корневые маршруты API
categories/ - Управление произведениями, категориями, жанрами:
Полная реализация CRUD
Фильтрация и поиск
Импорт данных (отсутствует!)
reviews/ - Отзывы и комментарии:
Вложенные маршруты (/titles/{id}/reviews/)
Проверка уникальности отзывов
Рейтинг произведений
users/ - Аутентификация и пользователи:
JWT токены
Регистрация с email подтверждением
Роли пользователей
Добавить кастомные обработчики ошибок в api_yamdb/urls.py:
Проверить валидацию года, чет кажется хрень!

## Сравнение с документацией (redoc.yaml):
✅ Все endpoint'ы присутствуют
✅ Права доступа соответствуют
✅ Поля сериализаторов совпадают
✅ Валидация данных реализована
✅ Пагинация настроена
✅ Фильтрация работает

## Эндпоинты

# Админ-панель 
/admin/
# Документация
 API /redoc/
# Аутентификация (/api/v1/auth/)
GET, POST, PATCH, DELETE /api/v1/auth/signup/     # Регистрация пользователя
GET, POST, PATCH, DELETE /api/v1/auth/token/      # Получение JWT токена
# Пользователи (/api/v1/users/)
GET, POST           /api/v1/users/                # Список всех пользователей (admin only)
GET, PATCH, DELETE  /api/v1/users/{username}/     # Управление пользователем по username (admin only)
GET, PATCH          /api/v1/users/me/             # Управление своим профилем
# Категории (/api/v1/categories/)
GET, POST           /api/v1/categories/           # Список категорий + создание (admin)
DELETE              /api/v1/categories/{slug}/    # Удаление категории (admin)
# Произведения (/api/v1/titles/)
GET                 /api/v1/titles/               # Список произведений (с фильтрацией)
POST                /api/v1/titles/               # Создание произведения (admin)
GET, PATCH, DELETE  /api/v1/titles/{titles_id}/   # Управление произведением (admin)
# Отзывы (/api/v1/titles/{title_id}/reviews/)
GET, POST           /api/v1/titles/{title_id}/reviews/                  # Список отзывов + создание
GET, PATCH, DELETE  /api/v1/titles/{title_id}/reviews/{review_id}/      # Управление отзывом
# Комментарии (/api/v1/titles/{title_id}/reviews/{review_id}/comments/)
GET, POST           /api/v1/titles/{title_id}/reviews/{review_id}/comments/           # Список комментариев + создание
GET, PATCH, DELETE  /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/  # Управление комментарием
### Параметры запросов 
## Фильтрация для произведений (/api/v1/titles/)
?category={slug}    # Фильтр по категории
?genre={slug}       # Фильтр по жанру
?name={string}      # Поиск по названию (icontains)
?year={integer}     # Фильтр по году
# Поиск
/search?q=          # Для категорий, жанров, пользователей
Пагинация (вроде везде)
?page={number}      # Номер страницы
?limit={number}     # Количество элементов на странице (max 100)
### Подробная таблица эндпоинтов

Метод	Путь	Назначение	Права доступа
POST	/api/v1/auth/signup/	Регистрация	Все (без токена)
POST	/api/v1/auth/token/	Получение JWT токена	Все (без токена)
GET	/api/v1/users/	Список пользователей	Администратор
POST	/api/v1/users/	Создание пользователя	Администратор
GET	/api/v1/users/{username}/	Пользователь по username	Администратор
PATCH	/api/v1/users/{username}/	Изменение пользователя	Администратор
DELETE	/api/v1/users/{username}/	Удаление пользователя	Администратор
GET	/api/v1/users/me/	Получение своего профиля	Любой авторизованный
PATCH	/api/v1/users/me/	Изменение своего профиля	Любой авторизованный
GET	/api/v1/categories/	Список категорий	Все (без токена)
POST	/api/v1/categories/	Создание категории	Администратор
DELETE	/api/v1/categories/{slug}/	Удаление категории	Администратор
GET	/api/v1/genres/	Список жанров	Все (без токена)
POST	/api/v1/genres/	Создание жанра	Администратор
DELETE	/api/v1/genres/{slug}/	Удаление жанра	Администратор
GET	/api/v1/titles/	Список произведений	Все (без токена)
POST	/api/v1/titles/	Создание произведения	Администратор
GET	/api/v1/titles/{id}/	Получение произведения	Все (без токена)
PATCH	/api/v1/titles/{id}/	Изменение произведения	Администратор
DELETE	/api/v1/titles/{id}/	Удаление произведения	Администратор
GET	/api/v1/titles/{title_id}/reviews/	Список отзывов	Все (без токена)
POST	/api/v1/titles/{title_id}/reviews/	Создание отзыва	Авторизованный
GET	/api/v1/titles/{title_id}/reviews/{review_id}/	Получение отзыва	Все (без токена)
PATCH	/api/v1/titles/{title_id}/reviews/{review_id}/	Изменение отзыва	Автор/Модератор/Админ
DELETE	/api/v1/titles/{title_id}/reviews/{review_id}/	Удаление отзыва	Автор/Модератор/Админ
GET	/api/v1/titles/{title_id}/reviews/{review_id}/comments/	Список комментариев	Все (без токена)
POST	/api/v1/titles/{title_id}/reviews/{review_id}/comments/	Создание комментария	Авторизованный
GET	/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/	Получение комментария	Все (без токена)
PATCH	/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/	Изменение комментария	Автор/Модератор/Админ
DELETE	/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/	Удаление комментария	Автор/Модератор/Админ


### Примеры запросов
# Регистрация:
POST /api/v1/auth/signup/
{
  "email": "user@example.com",
  "username": "username"
}

# Получение токена:
POST /api/v1/auth/token/
{
  "username": "username",
  "confirmation_code": "123456"
}
# Создание произведения (с токеном администратора):
POST /api/v1/titles/
Authorization: Bearer {token}
{
  "name": "Название произведения",
  "year": 2023,
  "description": "Описание",
  "category": "films",
  "genre": ["action", "drama"]
}

# Добавление отзыва:
POST /api/v1/titles/1/reviews/
Authorization: Bearer {token}
{
  "text": "Отличный фильм!",
  "score": 9
}

# Фильтрация произведений:
GET /api/v1/titles/?category=films&genre=action&year=2023&name=война