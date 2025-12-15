# test_urls.py в папке с manage.py
# TODO: В таком виде тесты в репозитории оставлять не стоит.
# Для себя использовать можно, но давайте из репозитория удалим, т.к.
# тут код скорее для какой-то быстрой проверки на коленке, а не
# полноценные тесты.
import os
import sys
import django
from django.test import Client

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_yamdb.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

# Тестируем маршруты
client = Client()

urls_to_test = [
    '/api/v1/auth/signup/',
    '/api/v1/auth/token/',
    '/api/v1/users/',
]

print("Testing URLs:")
for url in urls_to_test:
    response = client.get(url)
    print(f"{url}: {response.status_code} - {response.reason_phrase}")
