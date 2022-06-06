# fastAPI_notes_and_tags

<h2>Описание</h2>

<p>API сервис, реализованный на фреймворке fastAPI.</p>
<br>
<p>В сервисе реализованы модели заметок (notes) тегов (tags) и общая модель заметок, отмеченных тегами</p>

<h2>Установка</h2>

<h3>Создайте контейер:</h3>

> sudo docker-compose up -d --build

<h3>Запустите миграции</h3>

> sudo docker-compose exec web alembic upgrade head

<h3>Запустите контейнер</h3>

> docker-compose up

<h3>Перейдите по адресу</h3>

http://0.0.0.0:8000/

<h3>Остановка контейнера</h3>

> docker-compose down

<h3>Запуск сервиса вне докера</h3>
<p>В виртуальное окружение установить все зависимости из requirements.txt</p>

> pip install -r requirements.txt

<p>Запустить сервис</p>

> python -m run

