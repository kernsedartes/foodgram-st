FROM python:3.13
WORKDIR /app
COPY ../requirements.txt .
COPY ../data .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"]


# FROM python:3.13
# WORKDIR /app

# # Установка зависимостей
# COPY ../requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Копируем нужные файлы
# COPY wait-for-postgres.sh ./wait-for-postgres.sh
# RUN chmod +x ./wait-for-postgres.sh

# COPY ../data ./data
# COPY . .

# # Команда запуска по умолчанию
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"]