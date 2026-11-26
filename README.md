# Отчёты на Celery

В первом примере скрипт отправляет номер заявки через Redis. Исполнитель получает сообщение и сохраняет отчёт. В каталоге _web_ ту же работу заказывает пользователь через форму Django. Команды рассчитаны на Python 3.12 и терминал macOS или Linux.

## Подготовка

Из каталога репозитория создайте окружение и запустите Redis.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
docker run --rm -d --name celery-redis -p 127.0.0.1:6379:6379 redis:7-alpine
```

## Отчёт из скрипта

Запустите исполнитель в первом терминале.

```bash
celery -A tasks worker --loglevel=INFO --pool=solo
```

Во втором терминале откройте каталог репозитория, активируйте окружение и отправьте заявку.

```bash
source .venv/bin/activate
python -c 'from tasks import build_report; print(build_report.delay(42).id)'
```

Сверьте напечатанный идентификатор с записью об успешном выполнении в первом терминале и откройте _reports/42.txt_. Перед переходом к веб-приложению остановите исполнитель сочетанием Ctrl+C.

## Заявка через Django

В первом терминале перейдите в каталог _web_, создайте таблицу заявок и запустите исполнитель Django.

```bash
cd web
python manage.py migrate
celery -A config worker --loglevel=INFO --pool=solo
```

Во втором терминале запустите веб-сервер.

```bash
cd web
python manage.py runserver
```

Откройте [форму заявки](http://127.0.0.1:8000/) и нажмите «Подготовить отчёт». Браузер покажет номер заявки в поле `request_id`. После выполнения задачи откройте файл с этим номером в _web/output/reports/_.

Остановите сервер и исполнитель сочетанием Ctrl+C в каждом терминале. Завершите работу Redis командой `docker stop celery-redis`.
