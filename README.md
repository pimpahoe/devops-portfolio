# Todo API — DevOps Pet Project

> Flask REST API которое я деплою и усложняю каждый день, изучая DevOps практики.

## Стек

![Python](https://img.shields.io/badge/Python-3.11-blue)
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

---
