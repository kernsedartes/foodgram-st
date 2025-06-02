Foodgram

Перед началом убедитесь, что на вашем компьютере установлен Docker и Docker Compose.

1. Клонируйте репозиторий

        git clone https://github.com/kernsedartes/foodgram-st.git
        cd foodgram-st/infra

2. Переименуйте .env.exmp в .env и добавьте свои данные в .env

3. Запустите проект в Docker
        docker-compose up --build

Это соберёт и поднимет все необходимые контейнеры: backend, frontend и базу данных.

Если не запускается с первого раза, запустите еще раз команду

        docker-compose up

Если необходимо полностью очистить папки с данными, то используйте команду

        docker-compose down -v

Эта команда очистит все папки с данными и контейнеры

Если необходимо просто удалить контейнеры, используйте команду

        docker-compose down

Эти команды нкжно запускать строго из папки foodgram-st/infra

4. Загрузите ингредиенты

После запуска контейнеров ингредиенты загружаются автоматически, но если будет ошибка, то
можно загрузить их этой командой:

Переходим в контейнер:

        docker exec -it foodgram-back sh 

А затем уже в контейнере:

        python manage.py load_ingredients data/ingredients.json

Если потребуется удалить загруженные ингредиенты, используйте:

        docker exec -it foodgram-back sh

И опять в контейнере:

        python manage.py delete_ingredients
