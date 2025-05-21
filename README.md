Foodgram

Перед началом убедитесь, что на вашем компьютере установлен Docker и Docker Compose.

1. Клонируйте репозиторий
    git clone https://github.com/kernsedartes/foodgram-st.git
    cd foodgram-st/infra
2. Переименуйте .env.exmp в .env и добавьте свои данные в .env

3. Запустите проект в Docker
    docker-compose up --build
Это соберёт и поднимет все необходимые контейнеры: backend, frontend и базу данных.

4. Загрузите ингредиенты
После запуска контейнеров данные загружаются автоматически, но если будет ошибка, то
можно загрузить их этой командой:

    docker exec -it foodgram-back sh 
А затем уже в контейнере:

    python manage.py load_ingredients
Если потребуется удалить загруженные ингредиенты, используйте:

    docker exec -it foodgram-back sh
И опять в контейнере
    python manage.py delete_ingredients
