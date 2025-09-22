# Cервис для операций со счетами

## Репозиторий

Клонируйте репозиторий в папку с проектом. 
```bush 
git clone https://github.com/romanulanov/wallet-service.git
```

## Важное ! Файл `.env`
Для работы сайта необходимо создать файл `.env`, вида

- `DEBUG` — дебаг-режим. Поставьте `False`.
- `POSTGRES_DB` — имя базы данных, которую будет использовать Django.
- `POSTGRES_USER` — пользователь PostgreSQL с правами на эту БД.
- `POSTGRES_PASSWORD` — пароль этого пользователя.
- `POSTGRES_HOST` — имя контейнера с БД в Docker Compose (обычно db).
- `POSTGRES_PORT` — порт PostgreSQL (по умолчанию 5432).
- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте.
- `DJANGO_SUPERUSER_USERNAME` — логин суперпользователя.
- `DJANGO_SUPERUSER_EMAIL` — почта суперпользователя.
- `DJANGO_SUPERUSER_PASSWORD` — пароль админки суперпользователя.

## Запуск сервиса

Соберите и запустите Docker-контейнеры:
```sh
docker-compose up --build
```
После сборки зайдите в админку `http://127.0.0.1:8000/admin/` и создайте счет. 
По его id получите баланс кошелька через API:
```
GET http://127.0.0.1:8000/api/v1/wallets/<WALLET_UUID>/
```
Проведение операций с кошельком через API: 
```
POST http://127.0.0.1:8000/api/v1/wallets/<WALLET_UUID>/operation/
```
Пример корректного JSON-запроса:
```json
{
  "operation_type": "DEPOSIT",
  "amount": 1000
}
```

## Тесты

Тесты проекта расположены в `wallet/tests.py`. Для их отдельного запуска используйте:

```sh
docker-compose run web pytest wallet/tests.py
```