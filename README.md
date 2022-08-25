[![build, deploy, tests](https://github.com/mv-31/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/mv-31/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Продуктовый помощник - Foodgram
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
## Запуск проекта локально
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

## Запуск проекта на сервере
### Репозиторий
1. Клонировать репозиторий
2. В репозитории на гитхаб 
 ```Settings - Secrets - Actions```
добавите следующие ключи:

> DOCKER_USERNAME - имя пользователя docker;  
> DOCKER_PASSWORD - пароль docker;  
> HOST - ip-адрес сервера;  
> USER - имя пользователя для сервера;  
> SSH_KEY - приватный ключ с компьютера, имеющего доступ к боевому серверу ``` cat ~/.ssh/id_rsa ```;  
> PASSPHRASE - пароль для сервера;  
> DB_ENGINE=django.db.backends.postgresql - указываем, что работаем с postgresql;  
> DB_NAME=postgres - имя базы данных;  
> POSTGRES_USER - логин для подключения к базе данных;  
> POSTGRES_PASSWORD - пароль для подключения к БД;  
> DB_HOST=db - название сервиса (контейнера);  
> DB_PORT=5432 - порт для подключения к БД;  
> TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start);  
> TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота);

3. Измените имя пользователя DockerHub в docker-compose.yaml

### Подготовка сервера
- Запустить сервер и подключиться к нему:
``` ssh username@ip_address ```
- Установить обновления apt:
``` sudo apt upgrade -y ```
- Установить nginx:
``` sudo apt install nginx -y ```
- Остановить службу nginx:
``` sudo systemctl stop nginx ```
- Установить docker:
``` sudo apt install docker.io ```
- Установить стабильную версию docker-compose: 
``` sudo curl -SL https://github.com/docker/compose/releases/download/v2.6.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose ```
- Применить к файлу права доступа: 
``` sudo chmod +x /usr/local/bin/docker-compose	```
- Проверить версию docker-compose:
``` docker-compose --version ```  
- Создать на сервере три файла и скопировать в них код из проекта на GitHub:  
  - home/'username'/docker-compose.yml  
  ``` sudo nano docker-compose.yaml ```  
  - home/'username'/nginx.conf
  ``` sudo nano nginx.conf ```  
  - home/'username'/nginx/default.conf
  ``` mkdir nginx ```  
  ``` sudo nano nginx/default.conf ```

### Развертывание приложения на боевом сервере

Запушить репозиторий.
Статус работы отображается в Actions на GitHub.
---
# Сайт проекта Foodgram
```
http://158.160.9.118/
```
    
### Документация API Foodgram

```
http://158.160.9.118/redoc/
```

### Автор:

[mv-31](https://github.com/mv-31/ "mv-31")