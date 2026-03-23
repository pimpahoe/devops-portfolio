# Todo API — DevOps Pet Project

> Flask REST API которое я деплою и усложняю каждый день, изучая DevOps практики.

## Стек

![Python](https://img.shields.io/badge/Python-3.11-yellow)
![Flask](https://img.shields.io/badge/Flask-3.1-lightgrey)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-lightblue)
![Redis](https://img.shields.io/badge/Redis-7-red)
![Nginx](https://img.shields.io/badge/Nginx-1.29-green)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

## Быстрый старт

```bash
git clone https://github.com/username/todo-api
cd todo-api
cp .env.example .env      # заполни переменные
python deploy.py          # поднимает стек и проверяет здоровье
```

Или вручную:
```bash
docker compose up --build
```

UI доступен на `http://localhost`, API на `http://localhost/tasks`

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
├── app.py                  # Flask приложение + PostgreSQL + Redis кэш
├── requirements.txt        # Python зависимости
├── Dockerfile              # образ для Flask
├── docker-compose.yml      # оркестрация 5 контейнеров
├── nginx.conf              # reverse proxy + load balancing
├── index.html              # UI для задач
├── health_check.py         # проверка доступности сервисов
├── deploy.py               # автоматический деплой
├── generate_config.py      # генерация docker-compose с n инстансами
├── .env                    # переменные окружения (не в git)
└── README.md               # документация
```

## Архитектура

```
Браузер / curl
      ↓
  Nginx :80          ← reverse proxy, отдаёт статику
      ↓
  ┌─────────┐
  │  app1   │  ← Flask (round-robin)
  │  app2   │  ← Flask
  └─────────┘
      ↓           ↓
 PostgreSQL     Redis
  (данные)     (кэш GET /tasks, TTL 60s)
```

---

## Production Deployment

На реальном Linux сервере после запуска `docker compose up` нужно закрыть лишние порты через UFW:

```bash
# Установить UFW
sudo apt install ufw

# Политика по умолчанию — запретить всё входящее
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Открыть только нужные порты
sudo ufw allow 22     # SSH — обязательно, иначе потеряешь доступ к серверу
sudo ufw allow 80     # Nginx HTTP

# Включить файрвол
sudo ufw enable

# Проверить статус
sudo ufw status
```

После этого:
```bash
curl http://your-server:5000/tasks   # → Connection refused ✓
curl http://your-server/tasks        # → работает через Nginx ✓
```

### ✅ День 1 — Flask Todo API
Создал REST API на Flask с четырьмя эндпоинтами: получить список задач, добавить, обновить и удалить. Данные хранились в памяти — простой список в коде. Создал репозиторий на GitHub и сделал первый коммит.

### ✅ День 2 — Docker
Написал `Dockerfile` и упаковал Flask приложение в образ. Собрал образ через `docker build`, запустил контейнер через `docker run` и проверил что API отвечает так же как и без Docker.

### ✅ День 3 — Docker Compose + PostgreSQL
Поднял два контейнера одной командой `docker compose up --build`. Заменил хранение данных в памяти на PostgreSQL — переписал все эндпоинты с SQL запросами через `psycopg2`. Разобрался с сетью между контейнерами: Flask обращается к БД по имени сервиса `db`, а не по IP. Добавил `volume` чтобы данные не пропадали при перезапуске. Столкнулся с проблемой что Flask стартовал раньше чем PostgreSQL был готов — решил через retry логику в коде.

### ✅ День 4 — Nginx
Добавил Nginx как reverse proxy — теперь все запросы проходят через него, Flask напрямую снаружи недоступен. Написал `nginx.conf` с `upstream` блоком, обновил `docker-compose.yml` — теперь поднимается 3 контейнера: PostgreSQL, Flask и Nginx. Убрал проброс порта 5000 у Flask — снаружи торчит только Nginx на 80. Также добавил статичную HTML страницу для отображения задач — Nginx отдаёт её на `/`, а `/tasks` проксирует в Flask.

### ✅ День 5 — Load Balancing
Продублировал контейнер Flask — теперь запускается `app1` и `app2`. Добавил оба в `upstream` блок в `nginx.conf`. Nginx распределяет запросы между ними по алгоритму round-robin — каждый следующий запрос уходит на следующий инстанс по кругу. Проверил через логи что запросы реально чередуются между контейнерами.
### ✅ День 6 — Firewall
Разобрался с UFW и iptables — инструментами файрвола на уровне ОС. На нашем стеке Flask уже закрыт снаружи через Docker сеть (нет `ports` у `app1` и `app2`), но на реальном сервере нужно дополнительно закрывать порты через UFW. См. раздел Production Deployment ниже.

### ✅ День 7 — Повторение
Воспроизвёл весь стек с нуля без подсказок — вручную переписал все файлы: `app.py`, `Dockerfile`, `docker-compose.yml`, `nginx.conf`. Закрепил понимание как все части связаны между собой.

### ✅ День 8 — Мониторинг
Научился диагностировать состояние контейнеров — `docker stats` для CPU и памяти, `docker exec` чтобы зайти внутрь и покопаться, `ps aux` для просмотра процессов, `free -h` и `df -h` для памяти и диска. Запустил нагрузочный тест и посмотрел как ведут себя контейнеры — база данных оказалась самым нагруженным звеном. Также понял что пароли нельзя хардкодить в `docker-compose.yml` — нужно выносить в `.env` файл и добавлять его в `.gitignore`.

### ✅ День 9 — Сетевые инструменты
Повторил базовые команды для сетевой диагностики: `curl -v` для просмотра заголовков запроса и ответа, `netstat` для проверки открытых портов, `getent hosts` для резолвинга имён внутри Docker сети, `docker network inspect` для просмотра всей сетевой топологии проекта.

### ✅ День 10 — awk, sed, grep
Повторил команды для работы с текстом: `grep` для поиска строк в логах, `awk` для вытаскивания конкретных колонок (метод запроса, IP, статус код), `sed` для замены текста. Собрал pipe chain из нескольких команд — отфильтровал логи Nginx, вытащил методы запросов и посчитал статистику.

### ✅ День 11 — Python для DevOps
Написал два скрипта автоматизации. `health_check.py` — проверяет доступность всех контейнеров через `docker inspect` и делает HTTP запрос к API через Nginx. `deploy.py` — останавливает старые контейнеры, пересобирает образы, поднимает стек в фоне и автоматически запускает health check.

### ✅ День 12 — YAML/JSON конфиги
Разобрался с библиотеками `json` и `yaml` в Python. Написал скрипт `generate_config.py` который генерирует готовый `docker-compose.yml` — с инстансом БД, Nginx и n-ным количеством Flask инстансов которое можно регулировать одним параметром.

### ✅ День 13 — Redis
Добавил Redis как слой кэширования. `GET /tasks` теперь сначала проверяет кэш — если данные есть, возвращает их без обращения к PostgreSQL. При `POST`, `PUT`, `DELETE` кэш инвалидируется чтобы данные оставались актуальными. TTL кэша — 60 секунд. Также разобрался что Docker не показывает `print()` в логах по умолчанию — добавил `sys.stdout = sys.stderr`.

### ✅ День 14 — Финал
Полный стек работает. Прогнал структуру всех конфигов и питон файла с нуля — `Dockerfile`, `docker-compose.yml`, `nginx.conf`, `app.py`. Понял где пробелы и что нужно повторить.