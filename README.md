[![build, deploy, tests](https://github.com/mv-31/
foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/mv-31/
foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)

# Продуктовый помощник - foodgram
### Описание
Сайт, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Стек технологий:
- Python
- Django
- Django Rest Framework
- PostgreSQL
- Docker
- Workflow
- nginx
- Yandex.Cloud
---

# Порядок запуска
### Запуск проекта локально
Клонировать репозиторий и перейти в него:
```
git clone https://github.com/mv-31/foodgram-project-react.git
cd backend
```

Создать и активировать виртуальное окружение, обновить pip и установить зависимости:
```
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Перейти в папку infra и cоздать файл .env:
```
cd ..
cd infra
touch .env
```

Шаблон наполнения .env
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
```

Запустить сборку контейнеров:
```
docker-compose up -d --build
```

Применить миграции
```
docker-compose exec backend python manage.py migrate
```

Создать суперпользователя
```
docker-compose exec backend python manage.py createsuperuser
```

Собрать статические файлы:
```
docker-compose exec backend python manage.py collectstatic --no-input 
```

Заполнить базу ингридиентами и тегами:
```
docker-compose exec backend python manage.py loaddata recipes/data/ingredient.json
docker-compose exec backend python manage.py loaddata recipes/data/tag.json
```

### Запуск проекта на сервере

---
# Документация API Foodgram
Доступна на эндпойнте:
```
http://178.154.196.215/redoc/
```
