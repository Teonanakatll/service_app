# облегченный линукс с зависимостями python
FROM python:3.9-alpine3.16

# копируем файл в папку temp
COPY requirements.txt /temp/requirements.txt
# копируем папку с джанго приложением в контейнер

# установка зависимостей для подключения питона к postgres
RUN apk add postgresql-client build-base postgresql-dev

# установливаем зависимости
RUN pip install -r /temp/requirements.txt

# эта команда создаст нам юзера в операционной системе, без пароля
RUN adduser --disabled-password service-user

COPY service /service
# WORKDIR - следует указывать откуда будут запускаться команды (файл manage.py)
WORKDIR /service
# внури докера пробрасываем порт для доступа снаружи
EXPOSE 8000

# юзер под которым будут запускаться все команды
USER service-user

