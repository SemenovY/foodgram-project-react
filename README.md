![Build Status](https://github.com/SemenovY/foodgram-project-react/actions/workflows/main.yml/badge.svg)

# Foodgram

«Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и
подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов,
которые нужно купить для приготовления выбранных блюд.

Проект доступен по адресу: http://fun-cook.ru/.

Панель администратора доступна по адресу: http://fun-cook.ru/admin.

Логин: admin

Пароль: admin

Документация API доступна по адресу: http://fun-cook.ru/api/docs/.

## Запуск проекта локально

1. Склонируйте репозиторий и прейдите в корневую директорию foodgram-project-react:

```bash
git clone SemenovY/foodgram-project-react.git
cd foodgram-project-react
```

2. В директории infra создайте файл с .env с переменными окружения:

```bash
cd infra
```

***Шаблон наполнения env файла прописан в файле .env.example.***

3. Соберите контейнер и запустите:

```bash
docker-compose up --build
```

4. Внутри контейнера backend выполните миграции, загрузите данные, соберите статику:

- выполнить миграции:

```bash
sudo docker-compose exec backend python manage.py migrate
```

- соберите статику:

```bash
sudo docker-compose exec backend python manage.py collectstatic --no-input
```

5. Создайте суперюзера:

```bash
sudo docker-compose exec backend python manage.py createsuperuser
```

6. При необходимости загрузите базу данными::

```bash
sudo docker-compose exec backend python manage.py load_ingredients
```

## Запуск проекта в автоматическом режиме

1. Со страницы репозитория https://github.com/SemenovY/foodgram-project-react.git создать fork проекта в свой GitHUB;

2. В разделе репозитория проекта Setting/Secrets:

- указать логин и пароль вашего DockerHUB с ключами

```bash
DOCKER_USERNAME, DOCKER_PASSWORD
```

- указать параметры сервера для разворачивания проекта (хост, логин, ssh-key, пароль ) с ключами:

```bash
HOST, USER, SSH_KEY, PASSPHRASE
```

- указать параметры базы данных с ключами:

```bash
DB_ENGINE, DB_NAME , POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT
```

- указать ID телеграм-канала и токен телеграм-бота для получения уведомлений с ключами:

```bash
TELEGRAM_TO, TELEGRAM_TOKEN
```

3. Подготовить ваш сервер:

- установить докер:

```bash
 sudo apt install docker.io
 ```

- установить docker-compose в соответствии с официальной документацией;
  https://docs.docker.com/compose/install/

- cкопировать файлы docker-compose.yaml и nginx.conf из проекта на сервер в home/<ваш_username>
  /foodgram/docker-compose.yaml и home/<ваш_username>/foodgram/nginx.conf соответственно.

4. На GitHUB выполнить любой commit, для запуска action workflow;

5. На вашем сервере, загрузить данные:

- При необходимости загрузите базу данными::

```bash
sudo docker-compose exec backend python manage.py load_ingredients
```

- создайте суперюзера:

```bash
sudo docker-compose exec backend python manage.py createsuperuser
```

В папке data подготовлен список ингредиентов с единицами измерения.
Список сохранён в форматах JSON и CSV: данные из списка будет необходимо загрузить в базу.

6. Ваш проект доступен по адресу вашего сервера:
   http://<ip_сервера>/

***Над проектом работал:***

* Семёнов Юрий | Github:https://github.com/SemenovY | very_junior разработчик.

## Технологии

- Python 3.10.10
- Django 3.2
- Django REST Framework 3.14.0
- Djoser 2.1.0
- Django filter 22.1
- Gunicorn 20.1.0
- Nginx 1.19.3
- Docker 20.10.22
- Postgres 13.0

## License

MIT

**Free Software, Not for commercial use!**
