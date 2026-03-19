Сервис для сокращения ссылок с веб-интерфейсом и REST API.

## ✨ Возможности

- **Сокращение ссылок** - создание коротких URL из длинных
- **Отслеживание переходов** - автоматический подсчет кликов по каждой ссылке
- **Статистика** - просмотр количества переходов и даты создания
- **REST API** - полный набор эндпоинтов для интеграции
- **Веб-интерфейс** - удобная HTML страница для использования

## 🚀 Быстрый старт

### Установка

```bash
# Клонировать репозиторий
git clone <your-repo-url>
cd link-shortcut-django

# Установить зависимости
pip install -r requirements.txt

# Применить миграции
python manage.py migrate

# Запустить сервер
python manage.py runserver
```

### Docker

```bash
# Собрать и запустить
docker-compose up --build

# Или запустить в фоне
docker-compose up -d
```

## 📚 API Эндпоинты

### 1. Создание короткой ссылки
```bash
POST /api/shorten
Content-Type: application/json

{
    "original_url": "https://example.com/very/long/url"
}
```

**Ответ:**
```json
{
    "id": 1,
    "original_url": "https://example.com/very/long/url",
    "short_code": "aB3xK9",
    "short_url": "http://localhost:8000/aB3xK9",
    "clicks": 0,
    "created_at": "2024-01-01T12:00:00Z"
}
```

### 2. Получение информации для редиректа
```bash
GET /api/{short_code}
```

**Ответ:**
```json
{
    "original_url": "https://example.com/very/long/url",
    "short_code": "aB3xK9",
    "clicks": 42
}
```

### 3. Статистика по ссылке
```bash
GET /api/stats/{short_code}
```

**Ответ:**
```json
{
    "original_url": "https://example.com/very/long/url",
    "short_code": "aB3xK9",
    "short_url": "http://localhost:8000/aB3xK9",
    "clicks": 42,
    "created_at": "2024-01-01T12:00:00Z"
}
```

## 💻 Веб-интерфейс

После запуска сервера откройте в браузере:
- **Главная страница**: http://localhost:8000
- **Все ссылки**: http://localhost:8000/all
- **Статистика**: http://localhost:8000/stats/{short_code}
- **Админка**: http://localhost:8000/admin

## 🧪 Тестирование

### Запуск всех тестов
```bash
python manage.py test api.tests -v 2
```

### Запуск конкретных тестов
```bash
# Тесты для эндпоинта создания ссылок
python manage.py test api.tests.test_shortcut_endpoint -v 2

# Тесты для редиректа
python manage.py test api.tests.test_redirect -v 2

# Тесты для статистики
python manage.py test api.tests.test_stats -v 2

# Граничные случаи
python manage.py test api.tests.test_edge -v 2
```

### Примеры запросов для тестирования

**PowerShell:**
```powershell
# Создать ссылку
$body = @{original_url = "https://google.com"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/shorten" -Method Post -Body $body -ContentType "application/json"

# Получить статистику
Invoke-RestMethod -Uri "http://localhost:8000/api/stats/abc123" -Method Get
```

**curl:**
```bash
# Создать ссылку
curl -X POST http://localhost:8000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://google.com"}'

# Получить информацию для редиректа
curl -X GET http://localhost:8000/api/abc123
```

## 🗄️ Модель данных

```python
class ShortURL:
    original_url = URLField(max_length=500)  # Оригинальная ссылка
    short_code = CharField(max_length=10)    # Короткий код
    clicks = BigIntegerField(default=0)       # Количество переходов
    created_at = DateTimeField(auto_now_add)  # Дата создания
    updated_at = DateTimeField(auto_now)      # Дата обновления
```

## 🔧 Настройки

### Переменные окружения
Создайте файл `.env`:
```env
DEBUG=True
DATABASE_URL=postgresql://user:pass@db:5432/dbname
ALLOWED_HOSTS=localhost,127.0.0.1
```

### База данных
Проект поддерживает:
- SQLite (для разработки)
- PostgreSQL (для продакшена)

## 📁 Структура проекта

```
link-shortcut-django/
├── api/                    # API приложение
│   ├── serializers.py      # Сериализаторы
│   ├── urls.py             # URL маршруты API
│   ├── views.py            # API представления
│   └── tests/               # Тесты API
│       ├── test_base.py
│       ├── test_edge.py
│       ├── test_redirect.py
│       ├── test_shortcut_endpoint.py
│       └── test_stats.py
├── main/                   # Основное приложение
│   ├── models.py           # Модель ShortURL
│   ├── views.py            # Веб-представления
│   ├── urls.py             # URL маршруты сайта
│   └── templates/          # HTML шаблоны
├── link_shortcut/          # Настройки проекта
│   ├── settings.py
│   └── urls.py
└── manage.py
```

## ✅ Текущий статус тестов

Все 27 тестов проходят успешно:
- ✅ Создание коротких ссылок
- ✅ Редиректы и подсчет переходов
- ✅ Статистика по ссылкам
- ✅ Граничные случаи (пустые URL, спецсимволы и т.д.)
- ✅ Обработка ошибок и невалидных данных

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Запушьте ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

MIT License