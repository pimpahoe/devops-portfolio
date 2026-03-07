# Todo API — DevOps Pet Project

> Flask REST API которое я деплою и усложняю каждый день, изучая DevOps практики.

## Стек

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.1-lightgrey)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

## Быстрый старт

```bash
git clone https://github.com/username/todo-api
cd todo-api
docker compose up --build
```

API будет доступно на `http://localhost:5000`

## API

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/tasks` | Список всех задач |
| POST | `/tasks` | Создать задачу |
| PUT | `/tasks/<id>` | Обновить задачу |
| DELETE | `/tasks/<id>` | Удалить задачу |

**Пример:**
```bash
# Создать задачу
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn DevOps"}'

# Получить список
curl http://localhost:5000/tasks
```

## Структура проекта

```
todo-api/
├── app.py                  # Flask приложение
├── requirements.txt        # Python зависимости
├── Dockerfile              # образ для Flask
└── docker-compose.yml      # оркестрация контейнеров
```

# Дневник прогресса

### ✅ День 1 — Flask Todo API
Создал REST API на Flask с четырьмя эндпоинтами: получить список задач, добавить, обновить и удалить. Данные хранились в памяти — простой список в коде. Создал репозиторий на GitHub и сделал первый коммит.

### ✅ День 2 — Docker
Написал `Dockerfile` и упаковал Flask приложение в образ. Собрал образ через `docker build`, запустил контейнер через `docker run` и проверил что API отвечает так же как и без Docker.

### ✅ День 3 — Docker Compose + PostgreSQL
Поднял два контейнера одной командой `docker compose up --build`. Заменил хранение данных в памяти на PostgreSQL — переписал все эндпоинты с SQL запросами через `psycopg2`. Разобрался с сетью между контейнерами: Flask обращается к БД по имени сервиса `db`, а не по IP. Добавил `volume` чтобы данные не пропадали при перезапуске. Столкнулся с проблемой что Flask стартовал раньше чем PostgreSQL — решил через depends_on.

### ✅ День 4 — Nginx
Добавил Nginx как reverse proxy — теперь все запросы проходят через него, Flask напрямую снаружи недоступен. Написал `nginx.conf` с `upstream` блоком, обновил `docker-compose.yml` — теперь поднимается 3 контейнера: PostgreSQL, Flask и Nginx. Убрал проброс порта 5000 у Flask — снаружи торчит только Nginx на 80. Также добавил статичную HTML страницу для отображения задач — Nginx отдаёт её на `/`, а `/tasks` проксирует в Flask.

### ✅ День 5 — Load Balancing
Продублировал контейнер Flask — теперь запускается app1 и app2. Добавил оба в upstream блок в nginx.conf. Nginx распределяет запросы между ними по алгоритму round-robin — каждый следующий запрос уходит на следующий инстанс по кругу. Проверил через логи что запросы реально чередуются между контейнерами.
### ⬜ День 6 — Firewall
### ⬜ День 7 — Повторение
### ⬜ День 8 — Мониторинг
### ⬜ День 9 — Сетевые инструменты
### ⬜ День 10 — awk, sed, grep
### ⬜ День 11 — Python для DevOps
### ⬜ День 12 — YAML/JSON конфиги
### ⬜ День 13 — Redis
### ⬜ День 14 — Финал
---
